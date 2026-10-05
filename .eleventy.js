// Eleventy config for the ReShaped brand site.
//
// Source lives in src/, build output in _site/.
// pathPrefix is configurable via the PATH_PREFIX env var so that GitHub Pages
// project deploys (which serve under /<repo-name>/) work without code edits.
// For a custom-domain or user-page deploy, leave PATH_PREFIX unset.
//
// Use the `| url` filter on every internal href so that pathPrefix gets
// prepended automatically. Static asset references (e.g. /css/styles.css)
// also need `| url`.

module.exports = function (eleventyConfig) {
  // Static assets passed through verbatim.
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  eleventyConfig.addPassthroughCopy({ "src/img": "img" });
  // Brand-mark assets (favicon family) sit at the site root.
  eleventyConfig.addPassthroughCopy({ "src/favicon.svg": "favicon.svg" });
  eleventyConfig.addPassthroughCopy({ "src/apple-touch-icon.png": "apple-touch-icon.png" });

  // Make per-page nav-active checks easier in templates.
  eleventyConfig.addFilter("isCurrent", function (pageUrl, candidate) {
    return pageUrl === candidate;
  });

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
    // Pretty URLs by default: src/about.njk -> _site/about/index.html -> /about/
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
    templateFormats: ["njk", "md", "html"],
    pathPrefix: process.env.PATH_PREFIX || "/",
  };
};
