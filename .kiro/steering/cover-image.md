---
inclusion: fileMatch
fileMatchPattern: 'content/*.md'
---

# Cover Image Workflow

## Trigger phrases

Run this workflow when the user says any of the following (case-insensitive),
e.g. "CIM", "cim", "CIm":

- "CIM" — shorthand for "cover image making" (the process described here)
- "Use this image on the cover page"
- "Set the cover for this post"

When asked to set/use an image as the cover page (OG/social preview) for a post:

1. Find the source image referenced in the post's body, e.g.
   `![id](image/<post-folder>/<file>.png)`.

2. Optimize it with the repo script `optimize_image.py` (keeps images small
   enough for WhatsApp / Twitter / Open Graph crawlers to fetch and render):

   ```bash
   /opt/miniconda3/envs/test12/bin/python optimize_image.py content/image/<post-folder>/<file>.png
   ```

   This creates an optimized JPEG copy alongside the original with a `-opt`
   suffix, e.g. `<file>-opt.jpg` (default: max width 1200px, target under 300 KB).

3. Add (or update) a `Cover:` field in the post's front matter pointing to the
   optimized image. The path is relative to `content/` (no leading slash):

   ```
   Cover: image/<post-folder>/<file>-opt.jpg
   ```

## Why optimize

The theme's `og:image` tag comes from the `Cover:` field
(`theme/templates/partial/og_article.html`), falling back to `SITELOGO`
(the profile pic) when no cover is set. WhatsApp and similar crawlers skip
preview images that are too large (multi-MB), so covers must be compressed.

## Notes

- `optimize_image.py` accepts optional flags: `--output PATH`, `--max-width`,
  `--max-kb`, `--suffix`.
- `image` is in `STATIC_PATHS`, so `content/image/...` is served at
  `/image/...`; the built tag resolves to `SITEURL + '/' + Cover`.
- After changing a cover, rebuild and deploy. WhatsApp caches previews per URL,
  so bust the cache by sharing the link once with a query string (e.g. `?v=2`).
