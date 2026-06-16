import type { MDXComponents } from "mdx/types";
import type { ReactNode } from "react";
import Image, { type ImageProps } from "next/image";
import Link from "next/link";

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    wrapper: ({ children }: { children: ReactNode }) => (
      <article className="blog-prose">{children}</article>
    ),
    a: ({ href = "#", children, ...rest }) => {
      const isExternal = /^https?:\/\//.test(href);
      if (isExternal) {
        return (
          <a href={href} target="_blank" rel="noopener noreferrer" {...rest}>
            {children}
          </a>
        );
      }
      return (
        <Link href={href} {...rest}>
          {children}
        </Link>
      );
    },
    img: (props) => (
      <Image
        sizes="(max-width: 768px) 100vw, 600px"
        width={900}
        height={600}
        {...(props as ImageProps)}
        alt={props.alt ?? ""}
      />
    ),
  };
}
