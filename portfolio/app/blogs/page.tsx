import SiteHeader from "@/components/SiteHeader";
import ProjectCard from "@/components/ProjectCard";
import { blogs } from "@/lib/projects";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Blogs",
  description:
    "Long-form posts on Bayesian regression, random forest voting, naive Bayes, and credit card fraud detection.",
};

export default function BlogsPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <h1 className="text-2xl font-semibold mb-4">Blogs</h1>
        <div className="flex flex-col gap-6 mt-4">
          {blogs.map((project) => (
            <ProjectCard key={project.title} project={project} />
          ))}
        </div>

        <section className="mt-10 rounded-2xl border border-(--border) bg-(--surface) p-6">
          <h2 className="text-xl font-semibold mb-3">PDF Resources</h2>
          <p className="text-sm leading-relaxed text-(--muted) mb-4">
            Open the ethics blog as a PDF.
          </p>
          <a
            href="/blogs/ethics-blog.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="text-(--text) underline opacity-90 hover:opacity-100"
          >
            ethics-blog.pdf
          </a>
        </section>
      </main>
    </>
  );
}
