# Cenow / B365 Advisors - Interview Preparation

## Project summary

Cenow / B365 Advisors is a full-stack corporate consulting website. It presents business services, captures contact and partnership enquiries, accepts job and internship applications, provides an interactive office-location globe, and includes an admin dashboard for job listings.

## Architecture

```text
Users / Admin
      |
      v
Next.js 15 + React 19 frontend
(App Router, TypeScript, Tailwind CSS)
      |
      +-- Public pages: Home, About, Services, Career, Contact
      +-- Interactive UI: Framer Motion / GSAP and Three.js globe
      +-- Admin dashboard: create, view, and delete job listings
      |
      v
Next.js Route Handlers and Server Actions
      |
      +-- /api/Jobs        -> fetch and delete job data
      +-- Server Action     -> create a job listing
      +-- /api/ContactUs   -> contact-email workflow
      +-- /api/Partnership -> partnership-email workflow
      +-- /api/Jobs/apply  -> job application with attachments
      |
      +------------------> PostgreSQL through Prisma ORM
      |                      `-- Jobs model
      |
      `------------------> Nodemailer + Gmail SMTP
                             `-- internal alerts and user confirmations
```

## Technology stack

- **Next.js 15 and React 19:** App Router pages, APIs, and Server Actions.
- **TypeScript:** typed components and application logic.
- **Tailwind CSS, Radix UI, Lucide:** responsive UI and reusable interface elements.
- **Framer Motion and GSAP:** animations and user feedback.
- **Three.js, React Three Fiber, Drei:** interactive 3D office-location globe.
- **Zustand:** globe state, including active location, auto-rotation, selected view, and markers.
- **Prisma and PostgreSQL:** persistent job-listing data.
- **Nodemailer:** contact, partnership, job, and internship email workflows.
- **Vercel Analytics, Meta Pixel, structured data, chatbot:** analytics, SEO, and engagement.

## Key flows

### Job management

1. An administrator signs in to the dashboard.
2. The dashboard creates, fetches, or deletes job records.
3. Prisma reads or writes the `Jobs` table in PostgreSQL.
4. The public career pages fetch job data and display current openings.

### Job or internship application

1. An applicant fills in the form and uploads documents.
2. The browser sends the data as `FormData` to a Next.js route handler.
3. The server processes resume and cover-letter files as buffers.
4. Nodemailer sends an internal notification with attachments and an acknowledgement email to the applicant.
5. The UI shows submission feedback.

### Contact and partnership enquiry

1. The user enters validated form details.
2. The frontend sends a JSON request to the corresponding route handler.
3. Nodemailer sends the business notification and the user confirmation email.

## Separate contribution narratives

> Use the following split only if it reflects your actual work. Update ownership before the interview if required.

### Candidate 1 - Frontend and user experience

**Interview answer**

> I primarily worked on the frontend and user experience. I built reusable React components and integrated them into Next.js App Router pages for the home, services, career, contact, and navigation experiences. I used Tailwind CSS to make layouts responsive for desktop and mobile users.
>
> I also worked on interactive elements such as animations with Framer Motion and GSAP, client-side form validation with loading and success states, and the interactive office-location globe. For the globe, I used React Three Fiber and Three.js, with Zustand to manage active locations, auto-rotation, display mode, and selected markers.

**What I learned**

- Component-based design with React and TypeScript.
- Responsive UI development with Tailwind CSS.
- State management with Zustand.
- Animation, API integration, and user feedback states.
- Turning business requirements into clear user journeys.

### Candidate 2 - Backend and data workflows

**Interview answer**

> My main contribution was backend integration and business workflows. I used Prisma ORM to connect the Next.js application to PostgreSQL and worked on the Jobs data model. I implemented the admin job-management flow so administrators can create, view, and delete job listings, with data reflected on the public career section.
>
> I also worked with Next.js Route Handlers for contact, partnership, job-application, and internship-application flows. These APIs process input, support multipart FormData and document attachments where needed, and use Nodemailer with environment variables to send internal alerts and automatic confirmations.

**What I learned**

- API design with Next.js Route Handlers and Server Actions.
- Prisma ORM and PostgreSQL CRUD operations.
- FormData, file handling, and email attachments.
- Environment variables, error handling, and backend integration.
- Backend security fundamentals.

## Shared internship learning

> The biggest learning was working as a team on a real business-oriented product. We learned to split work into modules, integrate frontend and backend changes, test responsive layouts and form workflows, use Git for collaboration, and think about performance, usability, reliability, and security - not only UI design.

## 30-second project introduction

> During our internship, we developed a full-stack consulting-company website using Next.js, React, TypeScript, Tailwind CSS, Prisma, and PostgreSQL. The platform includes service pages, an interactive global-office globe, contact and partnership forms, job and internship applications with automated email confirmation, and an admin dashboard for job management. The project gave us practical experience in frontend-backend integration, database operations, API development, responsive design, and team delivery.

## Likely interview questions

### What challenge did you solve?

> A key challenge was keeping career data dynamic while preserving a polished public UI. We separated responsibilities: the admin dashboard manages jobs, Prisma handles persistence, APIs expose the data, and the public career pages display it dynamically.

### Why did you use Prisma?

> Prisma gave us a typed and structured way to work with PostgreSQL. The schema keeps the data model clear, while Prisma simplifies CRUD operations and reduces database-query errors.

### What would you improve for production?

> The current admin authentication is prototype-level because it relies on client-side state. For production, we would implement server-side authentication with HTTP-only cookies, hashed passwords, role-based authorization, protected APIs, input and file validation, rate limiting, and a managed email provider.
