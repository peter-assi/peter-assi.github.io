import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { chromium } from "playwright";

const repoDir = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.join(repoDir, "dist");
const sourcePath = path.join(distDir, "index.html");
const outputPath = path.join(distDir, "resume.pdf");

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".pdf": "application/pdf",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
};

function contentTypeFor(filePath) {
  return mimeTypes[path.extname(filePath).toLowerCase()] ?? "application/octet-stream";
}

function safeJoin(root, requestPath) {
  const cleanedPath = requestPath.replace(/^\/+/, "") || "index.html";
  const resolved = path.resolve(root, cleanedPath);
  if (!resolved.startsWith(root)) {
    throw new Error("Path traversal blocked");
  }
  return resolved;
}

async function startServer(root) {
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://127.0.0.1");
      const filePath = safeJoin(root, url.pathname);
      const data = await readFile(filePath);
      res.writeHead(200, { "Content-Type": contentTypeFor(filePath) });
      res.end(data);
    } catch (error) {
      const statusCode = error.code === "ENOENT" ? 404 : 500;
      res.writeHead(statusCode, { "Content-Type": "text/plain; charset=utf-8" });
      res.end(statusCode === 404 ? "Not found" : "Server error");
    }
  });

  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  return {
    server,
    url: `http://127.0.0.1:${address.port}`,
  };
}

async function main() {
  await readFile(sourcePath);

  const { server, url } = await startServer(distDir);
  const browser = await chromium.launch();

  try {
    const page = await browser.newPage();
    await page.goto(`${url}/index.html`, { waitUntil: "networkidle" });
    await page.emulateMedia({ media: "print" });
    await page.pdf({
      path: outputPath,
      printBackground: true,
      preferCSSPageSize: true,
    });
  } finally {
    await browser.close();
    await new Promise((resolve, reject) => {
      server.close((error) => {
        if (error) {
          reject(error);
          return;
        }
        resolve();
      });
    });
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
