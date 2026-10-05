// Site-wide data exposed to every template as `site.*`.
//
// v3 (Metro direction) — replaces the v2 Rubik version.
// New: per-page period color mapping per identity-system-v3.md section 2.2.

module.exports = {
  brandmark: "reshaped",

  // Canonical site URL — used in OG/Twitter meta tags and canonical link.
  // Update when the deploy domain is finalized (currently a placeholder
  // for the GH Pages project page).
  url: "https://reshaped.example",

  // Default OG/Twitter description used when a page doesn't override it.
  description: "End-to-end design and build for complex, ambiguous, or overgrown products. Public services. Internal tools. Legacy systems.",

  // Default OG image (1200x630). Per-page overrides via front-matter.
  ogImage: "/img/og-image.png",

  // Theme color hint (some browsers tint the address bar with this).
  themeColor: "#E6007E",


  // Canonical nav. `key` matches a page's front-matter `navKey`.
  // `period` is the wordmark-period color per the Part 2.2 mapping.
  // The two anchor items (work, contact) never become page-active and have
  // no period color; they are in-page anchors on the landing.
  nav: [
    { label: "landing",      url: "/",              key: "landing",      period: "magenta" },
    { label: "how we work",  url: "/how-we-work/",  key: "how-we-work",  period: "cyan"    },
    { label: "about",        url: "/about/",        key: "about",        period: "lime"    },
    { label: "work",         url: "/#section-c",    key: "work-anchor"   },
    { label: "contact",      url: "/#section-d",    key: "contact-anchor"},
  ],

  // Used by the CTA bar in the footer.
  contactAnchor: "/#section-d",

  // The four canonical manifesto lines eligible for pull-quotes.
  // See identity-system-v3.md section 3.5. Pick from this list; never
  // freshly author a pull-quote per page.
  manifesto: [
    "Boring is a compliment.",
    "Slower than a coat of paint.",
    "Truth before taste.",
    "Structure before surface.",
  ],

  // Total page count used in sheet stamps ("01 / 04").
  publicPageCount: 4,

  // Build date for footer/colophon if needed.
  buildDate: new Date().toISOString().slice(0, 10),
};
