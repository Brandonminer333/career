import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import YAML from "yaml";

function getArgValue(flag) {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return null;
  return process.argv[idx + 1] ?? null;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderBookRow({ rankText, rankClassName, title, author }) {
  const rankClass = ["rank", rankClassName].filter(Boolean).join(" ");
  return `
<div class="book">
  <div class="${rankClass}">${escapeHtml(rankText)}</div>
  <div class="info">
    <span class="title">${escapeHtml(title)}</span>
    <div class="author">${escapeHtml(author)}</div>
  </div>
</div>`.trim();
}

function renderSectionLabel(text) {
  return `<div class="section-label">${escapeHtml(text)}</div>`;
}

function renderDivider() {
  return `<hr class="divider">`;
}

function normalizeList(value) {
  if (!Array.isArray(value)) return [];
  return value
    .filter(Boolean)
    .map((b) => ({
      title: typeof b?.title === "string" ? b.title.trim() : "",
      author: typeof b?.author === "string" ? b.author.trim() : "",
    }))
    .filter((b) => b.title.length > 0 || b.author.length > 0);
}

const inPath = getArgValue("--in") ?? "data/books.yml";
const outPath = getArgValue("--out") ?? "public/reading_list.from-yaml.html";

const absIn = path.resolve(process.cwd(), inPath);
const absOut = path.resolve(process.cwd(), outPath);

const yamlText = await readFile(absIn, "utf8");
const books = YAML.parse(yamlText) ?? {};

const toRead = normalizeList(books.to_read);
const currentlyReading = normalizeList(books.currently_reading);
const finished = normalizeList(books.finished);

const toReadHtml = [
  renderSectionLabel("To read - ranked"),
  ...toRead.map((b, idx) =>
    renderBookRow({
      rankText: `#${idx + 1}`,
      rankClassName: "",
      title: b.title,
      author: b.author,
    })
  ),
].join("\n\n");

const currentlyReadingHtml = [
  renderDivider(),
  renderSectionLabel("Currently reading"),
  ...currentlyReading.map((b) =>
    renderBookRow({
      rankText: "—",
      rankClassName: "",
      title: b.title,
      author: b.author,
    })
  ),
].join("\n\n");

const finishedHtml = [
  renderDivider(),
  renderSectionLabel("Have read"),
  ...finished.map((b) =>
    renderBookRow({
      rankText: "✓",
      rankClassName: "done",
      title: b.title,
      author: b.author,
    })
  ),
].join("\n\n");

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<meta name="description" content="Brandon Miner reading list" />
<title>My Reading List</title>
<style>
  :root {
    --max-width: 900px;
    --gap: 1rem;
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;

    --bg: #f7f7f7;
    --text: #111;
    --card-bg: #fff;
    --muted: #888;
    --muted-2: #aaa;
    --border: #eee;
    --divider: #e8e8e8;
    --rank-color: #bbb;
  }
  html, body { height: 100%; margin: 0; }
  body { display: flex; align-items: flex-start; justify-content: center; padding: 2rem; background: var(--bg); color: var(--text); }
  .wrap { width: 100%; max-width: var(--max-width); background: var(--card-bg); padding: 1.5rem; border-radius: 12px; box-shadow: 0 6px 18px rgba(0,0,0,.06); }
  header, main, footer { display: block; margin-bottom: var(--gap); }
  nav a { margin-right: 0.75rem; text-decoration: none; color: inherit; opacity: .8; }
  h1 { margin: 0 0 .25rem 0; font-size: 1.5rem; }
  p { margin: .25rem 0; line-height: 1.5; }

  .subtitle { font-size: 13px; color: var(--muted); margin-bottom: 1rem; }
  .section-label { font-size: 11px; font-weight: 500; color: var(--muted-2); letter-spacing: 0.07em; text-transform: uppercase; margin: 1.75rem 0 0.5rem; }
  .book { display: flex; align-items: flex-start; gap: 12px; padding: 10px 0; border-bottom: 0.5px solid var(--border); }
  .book:last-child { border-bottom: none; }
  .rank { font-size: 13px; font-weight: 500; color: var(--rank-color); min-width: 22px; padding-top: 3px; }
  .rank.done { color: #1D9E75; }
  .info { flex: 1; }
  .title { font-size: 14px; font-weight: 500; color: var(--text); line-height: 1.4; text-decoration: none; display: block; }
  .author { font-size: 12px; color: var(--muted); margin-top: 2px; }
  hr.divider { border: none; border-top: 1.5px solid var(--divider); margin: 1.25rem 0 0; }

  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0b0f14;
      --text: #e8e8e8;
      --card-bg: #111824;
      --muted: #9aa4b2;
      --muted-2: #b3bdca;
      --border: #2a3442;
      --divider: #2a3442;
      --rank-color: #c7d0df;
    }

    .wrap { box-shadow: 0 10px 24px rgba(0,0,0,.45); }
  }
</style>
</head>
<body>
<div class="wrap" role="document">
  <header>
    <h1>My Reading List</h1>
    <nav aria-label="Main navigation">
      <a href="./index.html">Home</a>
      <a href="./reading_list.html">My Reading List</a>
      <a href="./contact.html">Contact</a>
      <a href="">About</a>
    </nav>
  </header>
  <main role="main">
    <p class="subtitle">Ranked by helpfulness to a data scientist / ML engineer</p>

${currentlyReadingHtml}

${toReadHtml}

${finishedHtml}

  </main>
  <footer>
    <small><span id="year"></span> Brandon Miner</small>
  </footer>
</div>
<script>
  document.getElementById('year').textContent = new Date().getFullYear();
</script>
</body>
</html>
`;

await writeFile(absOut, html, "utf8");
console.log(`Wrote ${path.relative(process.cwd(), absOut)}`);
