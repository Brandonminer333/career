import SiteHeader from "@/components/SiteHeader";
import ProjectCard from "@/components/ProjectCard";
import { apps } from "@/lib/projects";

export default function HomePage() {
  return (
    <>
      <SiteHeader showHero />
      <main>
        <h2 className="text-2xl font-semibold mb-4">Projects</h2>
        <div className="flex flex-col gap-6 mt-4">
          {apps.map((project) => (
            <ProjectCard key={project.title} project={project} />
          ))}
        </div>
      </main>
    </>
  );
}
