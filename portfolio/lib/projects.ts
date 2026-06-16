import type { Project } from "@/components/ProjectCard";

export const apps: Project[] = [
  {
    title: "Semantic Personality Quiz",
    description:
      "An interactive web-based personality quiz that determines which Pokémon gym leader type best matches your personality using vector-based matching and semantic similarity algorithms.",
    image: "/images/quiz.jpg",
    href: "https://sematic-personality-quiz.vercel.app/",
    external: true,
    cta: "Take the Quiz",
  },
];

export const blogs: Project[] = [
  {
    title: "Exploration of Bayesian Regression",
    description:
      "Blog post that discusses the limitations of ordinary least squares (OLS) linear regression and motivates the use of Bayesian regression.",
    image: "/images/display_bayes_reg.png",
    href: "/projects/bayesian-regression",
    cta: "Read More",
  },
  {
    title: "Credit Card Fraud Prediction",
    description:
      "A step-by-step walkthrough of a credit card fraud detection project, covering exploratory data analysis, PCA for feature selection, and a logistic regression model optimized to minimize false negatives while maintaining accuracy.",
    image: "/images/ccf.png",
    href: "/projects/credit-card-fraud",
    cta: "Read More",
  },
  {
    title: "Random Forest Voting Methods",
    description:
      "A case study on different voting methods for aggregating predictions in a Random Forest classifier such as majority voting, weighted voting and ranked voting.",
    image: "/images/rf_image.png",
    href: "/projects/rf-voting",
    cta: "Read More",
  },
  {
    title: "Naive Bayes Questions & Answers",
    description:
      "A series of questions about Naive Bayes and discovery of their answers through synthetic data.",
    image: "/images/naive_bayes.png",
    href: "/projects/naive-bayes",
    cta: "Read More",
  },
];
