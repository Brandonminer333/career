import Image from "next/image";
import Link from "next/link";

export type Project = {
  title: string;
  description: string;
  image: string;
  href: string;
  external?: boolean;
  cta: string;
};

export default function ProjectCard({ project }: { project: Project }) {
  const link = project.external ? (
    <a
      href={project.href}
      target="_blank"
      rel="noopener noreferrer"
      className="text-(--text) underline opacity-90 hover:opacity-100"
    >
      {project.cta}
    </a>
  ) : (
    <Link
      href={project.href}
      className="text-(--text) underline opacity-90 hover:opacity-100"
    >
      {project.cta}
    </Link>
  );

  return (
    <article className="flex flex-col sm:flex-row items-center gap-4">
      <Image
        src={project.image}
        alt={project.title}
        width={300}
        height={200}
        className="w-full sm:w-[300px] h-[200px] object-cover rounded-lg shadow-md shrink-0"
      />
      <div>
        <h3 className="text-lg font-semibold mb-1">{project.title}</h3>
        <p className="leading-relaxed text-sm sm:text-base mb-2">
          {project.description}
        </p>
        {link}
      </div>
    </article>
  );
}
