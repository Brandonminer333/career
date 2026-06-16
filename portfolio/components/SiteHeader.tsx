import Link from "next/link";
import { FaLinkedin, FaGithub } from "react-icons/fa";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/blogs", label: "Blogs" },
  {
    href: "/reading_list.from-yaml.html",
    label: "My Reading List",
    external: true,
  },
  { href: "/resume/resume.pdf", label: "Resume", external: true, newTab: true },
  { href: "/contact", label: "Contact" },
  { href: "/about", label: "About" },
];

type Props = {
  showHero?: boolean;
};

export default function SiteHeader({ showHero = false }: Props) {
  return (
    <header className="mb-4">
      {showHero && (
        <div className="text-center mb-4">
          <h1 className="text-3xl font-semibold mb-1">Brandon Miner</h1>
          <h3 className="text-base text-(--muted) mb-2">
            Building End-to-End Data Systems & AI Solutions
          </h3>
          <div className="flex justify-center gap-3 text-2xl text-(--icon)">
            <a
              href="https://www.linkedin.com/in/brandon-miner-3x3/"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="LinkedIn"
              className="hover:text-[#0077b5] transition-colors"
            >
              <FaLinkedin />
            </a>
            <a
              href="https://github.com/Brandonminer333/"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="GitHub"
              className="hover:text-[#0077b5] transition-colors"
            >
              <FaGithub />
            </a>
          </div>
        </div>
      )}

      <nav aria-label="Main navigation" className="flex flex-wrap gap-3">
        {navItems.map((item) =>
          item.external ? (
            <a
              key={item.href}
              href={item.href}
              className="opacity-80 hover:opacity-100 no-underline"
              {...(item.newTab
                ? { target: "_blank", rel: "noopener noreferrer" }
                : {})}
            >
              {item.label}
            </a>
          ) : (
            <Link
              key={item.href}
              href={item.href}
              className="opacity-80 hover:opacity-100 no-underline"
            >
              {item.label}
            </Link>
          ),
        )}
      </nav>
    </header>
  );
}
