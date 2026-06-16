import SiteHeader from "@/components/SiteHeader";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About",
  description: "About Brandon Miner",
};

export default function AboutPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <h1 className="text-2xl font-semibold mb-2">About</h1>
        <p className="leading-relaxed">Coming soon.</p>
      </main>
    </>
  );
}
