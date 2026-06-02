# peter-assi.github.io

Static resume site for GitHub Pages.

## Source

- `index.html` is the source document and default homepage.
- `build-theme-variants.py` copies the single source document into `dist/index.html`.
- `build-pdf.mjs` generates `dist/resume.pdf` from `dist/index.html`.

## Local Build

```bash
npm ci
npx playwright install chromium
npm run build
```

Generated output lands in `dist/`:

- `dist/index.html`
- `dist/resume.pdf`

## GitHub Pages

GitHub Actions builds the site and deploys the `dist/` artifact to Pages.

- Workflow: `.github/workflows/deploy-pages.yml`
- Keep the Pages source in GitHub set to `GitHub Actions`
