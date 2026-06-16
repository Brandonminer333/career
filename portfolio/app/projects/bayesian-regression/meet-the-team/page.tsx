import Image from "next/image";
import { FaLinkedin, FaGithub } from "react-icons/fa";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Meet the team — Bayesian Regression",
  description:
    "The team behind the Bayesian Regression exploration blog post.",
};

type Member = {
  name: string;
  image: string;
  linkedin: string;
  github: string;
};

const members: Member[] = [
  {
    name: "Ankit Jain",
    image: "/projects/bayesian-regression/images/ankit_jain.png",
    linkedin: "https://www.linkedin.com/in/ankitjain90/",
    github: "https://github.com/akjai",
  },
  {
    name: "Brandon Miner",
    image: "/projects/bayesian-regression/images/brandon_miner.jpg",
    linkedin: "https://www.linkedin.com/in/brandon-miner-3x3",
    github: "https://github.com/Brandonminer333/",
  },
  {
    name: "Nanda Kumar Gunalan",
    image: "/projects/bayesian-regression/images/nanda_kumar_gunalan.jpg",
    linkedin: "https://www.linkedin.com/in/gunalannandakumar/",
    github: "https://github.com/NandakumarGunalan",
  },
  {
    name: "William Spagnuolo",
    image: "/projects/bayesian-regression/images/william_spagnuolo.jpg",
    linkedin: "https://www.linkedin.com/in/william-spagnuolo-b36b48152/",
    github: "https://github.com/williamspagnuolo",
  },
];

export default function MeetTheTeamPage() {
  return (
    <section>
      <h1 className="text-2xl font-semibold mb-1">
        An Exploration into Bayesian Regression
      </h1>
      <p className="text-(--muted) mb-6">Meet the team that made this blog.</p>

      <h2 className="text-xl font-semibold mb-4">Meet the Team</h2>
      <div className="flex flex-wrap justify-around gap-6 mt-2">
        {members.map((member) => (
          <div
            key={member.name}
            className="text-center flex-1 min-w-[160px] max-w-[200px]"
          >
            <Image
              src={member.image}
              alt={member.name}
              width={150}
              height={150}
              className="w-[150px] h-[150px] object-cover rounded-lg shadow-md mx-auto"
            />
            <h3 className="mt-2 mb-1 text-base font-semibold">{member.name}</h3>
            <div className="flex justify-center gap-3 text-xl text-(--icon)">
              <a
                href={member.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`${member.name} on LinkedIn`}
                className="hover:text-[#0077b5] transition-colors"
              >
                <FaLinkedin />
              </a>
              <a
                href={member.github}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`${member.name} on GitHub`}
                className="hover:text-[#0077b5] transition-colors"
              >
                <FaGithub />
              </a>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
