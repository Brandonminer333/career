import type { ReactNode } from "react";
import SiteHeader from "@/components/SiteHeader";

export default function ProjectsLayout({ children }: { children: ReactNode }) {
  return (
    <>
      <SiteHeader />
      <main>{children}</main>
    </>
  );
}
