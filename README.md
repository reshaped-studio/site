# Site

Public website for [reshaped.studio](https://reshaped.studio).

The Eleventy project in this repository is the pre-agency landing page, preserved so the rewrite has a starting point. It still describes an open-source studio. The agency rewrite replaces that copy before this site is published.

Deploy does not run on push. The GitHub Actions workflow is manual (`workflow_dispatch`) until that rewrite is ready.

```
npm ci
npm run build
npm run serve
```

Brand reviews and direction notes are in the private `studio` repository, under `brand/`.
