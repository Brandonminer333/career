# Brandon Miner — Portfolio

Personal portfolio site, built with [Next.js 16](https://nextjs.org/) (App Router), TypeScript, [Tailwind CSS v4](https://tailwindcss.com/), and [MDX](https://mdxjs.com/) for blog-style project posts. Deployed on [Vercel](https://vercel.com/).

## Tech stack

- **Framework**: Next.js (App Router) + React 19 + TypeScript
- **Styling**: Tailwind CSS v4
- **Content**: MDX with `remark-math` + `rehype-katex` for LaTeX, `remark-gfm` for GitHub-flavored markdown
- **Icons**: `react-icons` (FontAwesome set)
- **Hosting**: Vercel

## Local development

```bash
npm install
npm run dev
```

Open <http://localhost:3000>.

## Project structure

```plaintext
app/
├── layout.tsx                # Root layout (the white card, footer)
├── page.tsx                  # Home (project grid)
├── globals.css               # Theme + blog typography
├── about/page.tsx
├── contact/page.tsx
└── projects/
    ├── layout.tsx            # Shared header for all project pages
    ├── bayesian-regression/
    │   ├── page.mdx          # Blog post (MDX + KaTeX + iframes)
    │   └── meet-the-team/page.tsx
    ├── credit-card-fraud/page.mdx
    ├── naive-bayes/page.mdx
    └── rf-voting/page.mdx
components/
├── SiteHeader.tsx
└── ProjectCard.tsx
public/
├── images/                   # Project thumbnails
├── reading_list.html         # Static reading list (link target)
└── projects/                 # Per-project images & Plotly iframes
mdx-components.tsx            # MDX wrapper + image/link overrides
next.config.mjs
postcss.config.mjs
tailwind.config (none — Tailwind v4 reads from globals.css)
tsconfig.json
```

## Adding a new blog post

1. Create `app/projects/<slug>/page.mdx`.
2. Export a `metadata` object with `title` and `description` at the top.
3. Drop images into `public/projects/<slug>/images/` and reference them with `![alt](/projects/<slug>/images/foo.png)`.
4. Add a card for it in the `projects` array in `app/page.tsx`.

LaTeX works inline (`$\beta$`) and as blocks (`$$...$$`).

## Deploying to Vercel

Push to GitHub, import the repo in the Vercel dashboard, accept the defaults. No env vars needed.
