import { NextResponse } from "next/server";
import { z } from "zod";
import { prisma } from "@/lib/prisma";
import { comparePassword, issueAccessToken } from "@/lib/auth";
import { getSupabaseServerClient } from "@/lib/supabase-server";


const loginSchema = z.object({
  username: z.string().trim().min(3),
  password: z.string().min(8),
});

export async function POST(request: Request) {
  const payload = loginSchema.parse(await request.json());

  const identifier = payload.username.trim().toLowerCase();
  let email = identifier;

  if (!identifier.includes("@")) {
    const existing = await prisma.user.findUnique({
      where: { username: identifier },
      select: { email: true },
    });

    if (!existing?.email) {
      return NextResponse.json({ detail: "Invalid username/email or password." }, { status: 401 });
    }

    email = existing.email;
  }

  let data: { user: { id: string; email?: string | null; user_metadata?: Record<string, unknown> } | null };
  let error: { message?: string } | null = null;

  try {
    const supabase = getSupabaseServerClient();
    const result = await supabase.auth.signInWithPassword({
      email,
      password: payload.password,
    });
    data = result.data;
    error = result.error;
  } catch (clientError) {
    return NextResponse.json(
      { detail: clientError instanceof Error ? clientError.message : "Supabase Auth is not configured." },
      { status: 503 },
    );
  }

  if (error || !data.user?.email) {
    const localUser = await prisma.user.findFirst({
      where: identifier.includes("@")
        ? { email: identifier }
        : { username: identifier },
      select: {
        id: true,
        username: true,
        email: true,
        role: true,
        tokens: true,
        walletAddress: true,
        emailVerified: true,
        passwordHash: true,
        freelancerProfile: { select: { id: true } },
        clientProfile: { select: { id: true } },
      },
    });

    if (localUser?.passwordHash) {
      const matches = await comparePassword(payload.password, localUser.passwordHash);
      if (matches) {
        if (!localUser.emailVerified) {
          return NextResponse.json({ detail: "Please verify your email before signing in." }, { status: 403 });
        }

        return NextResponse.json({
          accessToken: issueAccessToken(localUser.id),
          user: {
            id: String(localUser.id),
            username: localUser.username,
            email: localUser.email,
            role: localUser.role,
            tokens: localUser.tokens,
            walletAddress: localUser.walletAddress,
            hasFreelancerProfile: !!localUser.freelancerProfile,
            hasClientProfile: !!localUser.clientProfile,
          },
        });
      }
    }

    const detail = (error?.message || "").toLowerCase().includes("email not confirmed")
      ? "Please verify your email before signing in."
      : "Invalid username/email or password.";
    const status = detail.includes("verify your email") ? 403 : 401;
    return NextResponse.json({ detail }, { status });
  }

  const supaEmail = data.user.email;
  const metadata = (data.user.user_metadata || {}) as { username?: string; role?: string };
  const existingUser = await prisma.user.findUnique({
    where: { email: supaEmail },
    select: {
      username: true,
      role: true,
      freelancerProfile: { select: { id: true } },
      clientProfile: { select: { id: true } },
    },
  });

  const fallbackUsername = metadata.username || existingUser?.username || supaEmail.split("@")[0] || `user_${data.user.id.slice(0, 8)}`;
  const metadataRole = metadata.role === "CLIENT" || metadata.role === "FREELANCER" || metadata.role === "ADMIN" ? metadata.role : null;
  let profileInferredRole: "CLIENT" | "FREELANCER" | null = null;
  if (existingUser?.freelancerProfile && !existingUser?.clientProfile) {
    profileInferredRole = "FREELANCER";
  } else if (existingUser?.clientProfile && !existingUser?.freelancerProfile) {
    profileInferredRole = "CLIENT";
  }
  const nextRole = metadataRole || profileInferredRole || existingUser?.role || "CLIENT";

  const synced = await prisma.user.upsert({
    where: { email: supaEmail },
    update: {
      emailVerified: true,
      username: fallbackUsername,
      name: fallbackUsername,
      role: nextRole,
    },
    create: {
      email: supaEmail,
      username: fallbackUsername,
      name: fallbackUsername,
      role: nextRole,
      tokens: nextRole === "CLIENT" ? 100 : 50,
      emailVerified: true,
    },
    select: {
      id: true,
      username: true,
      email: true,
      role: true,
      tokens: true,
      walletAddress: true,
      freelancerProfile: {
        select: {
          id: true,
        },
      },
      clientProfile: {
        select: {
          id: true,
        },
      },
    },
  });

  return NextResponse.json({
    accessToken: issueAccessToken(synced.id),
    user: {
      id: String(synced.id),
      username: synced.username,
      email: synced.email,
      role: synced.role,
      tokens: synced.tokens,
      walletAddress: synced.walletAddress,
      hasFreelancerProfile: !!synced.freelancerProfile,
      hasClientProfile: !!synced.clientProfile,
    },
  });
}
