import createMDX from "@next/mdx";

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ["ts", "tsx", "js", "jsx", "md", "mdx"],
};

const withMDX = createMDX({
  options: {
    remarkPlugins: [["remark-gfm", {}], ["remark-math", {}]],
    rehypePlugins: [["rehype-katex", {}]],
  },
});

export default withMDX(nextConfig);
