import type { ReactNode } from "react";
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Brandon Miner Portfolio",
    template: "%s | Brandon Miner",
  },
  description: "Portfolio of Brandon Miner",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  const year = new Date().getFullYear();

  return (
    <html lang="en">
      <body className="flex justify-center items-start p-4 sm:p-8 min-h-screen">
        <div className="w-full max-w-[900px] bg-(--card) p-6 rounded-xl shadow-[var(--card-shadow)]">
          {children}
          <footer className="mt-8 pt-4 border-t border-(--border)">
            <small className="text-(--muted)">© {year} Brandon Miner</small>
          </footer>
        </div>
      </body>
    </html>
  );
}
