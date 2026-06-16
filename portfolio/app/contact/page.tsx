import SiteHeader from "@/components/SiteHeader";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact",
  description: "Contact Brandon Miner",
};

export default function ContactPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <h1 className="text-2xl font-semibold mb-2">Contact</h1>
        <p className="leading-relaxed">
          Connect with me through the links below.
        </p>
        <ul className="mt-4 ml-5 list-disc space-y-2">
          <li>
            <strong>Email:</strong>{" "}
            <a
              className="underline"
              href="mailto:brandonm333@outlook.com"
            >
              brandonm333@outlook.com
            </a>
          </li>
          <li>
            <strong>LinkedIn:</strong>{" "}
            <a
              className="underline"
              href="https://www.linkedin.com/in/brandon-miner-3x3/"
              target="_blank"
              rel="noopener noreferrer"
            >
              linkedin.com/in/brandon-miner-3x3
            </a>
          </li>
          <li>
            <strong>GitHub:</strong>{" "}
            <a
              className="underline"
              href="https://github.com/Brandonminer333/"
              target="_blank"
              rel="noopener noreferrer"
            >
              github.com/Brandonminer333
            </a>
          </li>
        </ul>
      </main>
    </>
  );
}
