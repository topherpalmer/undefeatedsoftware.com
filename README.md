# undefeatedsoftware.com

The Undefeated Software website: plain HTML and CSS, served by GitHub Pages from `docs/`.

- `src/pages/*.html` holds each page's content, with its title and description in the first line.
- `src/site.css` and `src/site.js` are shared by every page.
- `python3 src/build.py docs` wraps each page in the shared header and footer and writes the site to
  `docs/`. Commit `docs/` with the change; Pages publishes it on push.

`docs/CNAME` names the custom domain. No framework and no build server: any static host works.
