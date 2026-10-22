# Equilibrium · Liquid Glass Landing Page

A minimalist wellness-brand landing page visual prototype crafted with React 18, TypeScript, Vite, Tailwind CSS v3, and Lucide React.

## Features

- **Liquid Glass Aesthetic:** Custom CSS luminance-blend backdrop filter with dual-gradient border via `-webkit-mask-composite: xor` / `mask-composite: exclude`.
- **Typography:** Geist variable font family for clean modern presentation.
- **Cinematic Looping Background:** Seamless video backdrop with graceful failure and ambient dark contrast gradient.
- **Responsive Architecture:** Centered pill navigation for desktop, accessible mobile drawer with Escape-key close listener and `aria-expanded`/`aria-controls` states.
- **Strictly Decoupled:** Independent prototype workspace with zero connection to the BidSentry-E procurement copilot.

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run production build & TypeScript validation
npm run build

# Preview production build locally
npm run preview
```

## Deployment

Deployable instantly to static hosting platforms (Vercel, Netlify, Cloudflare Pages):
- **Framework Preset:** Vite
- **Root Directory:** `equilibrium-landing` (or repo root if isolated)
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
