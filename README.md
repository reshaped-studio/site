# Site

Public website for ReShaped. Hosted at [reshaped-studio.github.io/site/](https://reshaped-studio.github.io/site/).

The Eleventy project includes the product-design landing page, its illustrated coffee-ordering timeline, and three illustrative Design Plan example pages. About and How we work describe the same Design Plan-first engagement. Contact links open an email to hello@reshaped.studio. Deployment metadata uses the GitHub Pages URL; a custom domain can be configured separately.

Pushes to `main` deploy through GitHub Actions after content, interaction, link, and asset checks. The workflow also supports manual deployment. Pages must use GitHub Actions as its publishing source. The build reads the host and path prefix from `actions/configure-pages`, so it supports both the project URL and a future custom domain.

```
npm ci
npm run build
npm run serve
```

Brand reviews and direction notes are in the private `studio` repository, under `brand/`.

This repo includes the shared [Many Hats](https://github.com/reshaped-studio/many-hats) team and the [Design Dash](https://github.com/reshaped-studio/design-dash) workflow as submodules. Clone with `--recurse-submodules`. `AGENTS.md` points at both.

## Design Plan examples

Edit `src/_data/designPlans.json` to maintain public project content. The shared template is `src/design-plans/example.njk`; wireframes are explicit SVG assets in `src/img/design-plans/`. Authoring notes are in `src/design-plans/README.md`. No private studio content is automatically included.

```
npm run test:design-plans
npm run build
python3 scripts/verify-plan-build.py _site
```

For a subdirectory build, set `PATH_PREFIX` and pass the same prefix as the second argument to the verifier. To create a preview whose links work directly from local files, run `python3 scripts/refresh-file-preview.py _site /absolute/preview/path`. The conversion touches generated output only.
