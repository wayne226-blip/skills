#!/usr/bin/env node
/**
 * Generate a branded PPTX reference template.
 *
 * This creates a .pptx file with slide masters that carry Wayne's brand
 * colors, fonts, and layouts. Use it with Pandoc's --reference flag or
 * PptxGenJS's masterName to get consistent branded output every time.
 *
 * Usage:
 *   node create_pptx_template.js [output.pptx] [--palette NAME]
 *
 * Palettes: midnight (default), forest, coral, ocean, charcoal
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

const PALETTES = {
  midnight: {
    primary: "1E2761", secondary: "2B6CB0", accent: "38A169",
    bg_dark: "1E2761", bg_light: "F7FAFC", text_light: "FFFFFF",
    text_dark: "2D3748", muted: "718096", border: "E2E8F0",
    headerFont: "Georgia", bodyFont: "Calibri",
  },
  forest: {
    primary: "2C5F2D", secondary: "97BC62", accent: "F5F5F5",
    bg_dark: "2C5F2D", bg_light: "F5F5F5", text_light: "FFFFFF",
    text_dark: "1A202C", muted: "6B7280", border: "D1D5DB",
    headerFont: "Georgia", bodyFont: "Calibri",
  },
  coral: {
    primary: "2F3C7E", secondary: "F96167", accent: "F9E795",
    bg_dark: "2F3C7E", bg_light: "FFF5F5", text_light: "FFFFFF",
    text_dark: "2D3748", muted: "718096", border: "E2E8F0",
    headerFont: "Georgia", bodyFont: "Calibri",
  },
  ocean: {
    primary: "065A82", secondary: "1C7293", accent: "21295C",
    bg_dark: "065A82", bg_light: "EBF8FF", text_light: "FFFFFF",
    text_dark: "1A202C", muted: "64748B", border: "CBD5E0",
    headerFont: "Georgia", bodyFont: "Calibri",
  },
  charcoal: {
    primary: "36454F", secondary: "F2F2F2", accent: "212121",
    bg_dark: "36454F", bg_light: "F2F2F2", text_light: "FFFFFF",
    text_dark: "212121", muted: "6B7280", border: "D1D5DB",
    headerFont: "Arial Black", bodyFont: "Arial",
  },
};

function createTemplate(outputPath, paletteName) {
  const p = PALETTES[paletteName] || PALETTES.midnight;
  const pres = new pptxgen();

  pres.layout = "LAYOUT_16x9";
  pres.author = "Wayne Pearce";
  pres.title = "Branded Template";

  // ── MASTER: Title Slide ──────────────────────────────
  pres.defineSlideMaster({
    title: "TITLE_SLIDE",
    background: { color: p.bg_dark },
    objects: [
      // Bottom accent bar
      { rect: { x: 0, y: 4.8, w: 10, h: 0.825, fill: { color: p.secondary } } },
      // Title placeholder
      {
        placeholder: {
          options: {
            name: "title", type: "title",
            x: 0.8, y: 1.2, w: 8.4, h: 1.8,
            fontFace: p.headerFont, fontSize: 40, color: p.text_light,
            bold: true, align: "left", valign: "middle",
          },
        },
      },
      // Subtitle placeholder
      {
        placeholder: {
          options: {
            name: "subtitle", type: "body",
            x: 0.8, y: 3.1, w: 8.4, h: 0.8,
            fontFace: p.bodyFont, fontSize: 18, color: p.text_light,
            align: "left", valign: "top",
          },
        },
      },
    ],
  });

  // ── MASTER: Content Slide ────────────────────────────
  pres.defineSlideMaster({
    title: "CONTENT_SLIDE",
    background: { color: p.bg_light },
    objects: [
      // Top accent bar
      { rect: { x: 0, y: 0, w: 10, h: 0.06, fill: { color: p.secondary } } },
      // Slide title placeholder
      {
        placeholder: {
          options: {
            name: "title", type: "title",
            x: 0.6, y: 0.25, w: 8.8, h: 0.65,
            fontFace: p.headerFont, fontSize: 26, color: p.primary,
            bold: true, align: "left", valign: "middle",
          },
        },
      },
      // Body placeholder
      {
        placeholder: {
          options: {
            name: "body", type: "body",
            x: 0.6, y: 1.1, w: 8.8, h: 4.0,
            fontFace: p.bodyFont, fontSize: 16, color: p.text_dark,
            align: "left", valign: "top",
          },
        },
      },
      // Footer
      {
        text: {
          text: "Wayne Pearce",
          options: {
            x: 0.6, y: 5.25, w: 4, h: 0.3,
            fontFace: p.bodyFont, fontSize: 8, color: p.muted,
            italic: true,
          },
        },
      },
    ],
  });

  // ── MASTER: Section Break ────────────────────────────
  pres.defineSlideMaster({
    title: "SECTION_BREAK",
    background: { color: p.primary },
    objects: [
      { rect: { x: 0.6, y: 2.9, w: 2, h: 0.05, fill: { color: p.secondary } } },
      {
        placeholder: {
          options: {
            name: "title", type: "title",
            x: 0.6, y: 1.5, w: 8.8, h: 1.3,
            fontFace: p.headerFont, fontSize: 36, color: p.text_light,
            bold: true, align: "left", valign: "bottom",
          },
        },
      },
      {
        placeholder: {
          options: {
            name: "body", type: "body",
            x: 0.6, y: 3.2, w: 8.8, h: 1.2,
            fontFace: p.bodyFont, fontSize: 16, color: p.text_light,
            align: "left", valign: "top",
          },
        },
      },
    ],
  });

  // ── MASTER: Two-Column ───────────────────────────────
  pres.defineSlideMaster({
    title: "TWO_COLUMN",
    background: { color: p.bg_light },
    objects: [
      { rect: { x: 0, y: 0, w: 10, h: 0.06, fill: { color: p.secondary } } },
      {
        placeholder: {
          options: {
            name: "title", type: "title",
            x: 0.6, y: 0.25, w: 8.8, h: 0.65,
            fontFace: p.headerFont, fontSize: 26, color: p.primary,
            bold: true, align: "left",
          },
        },
      },
      // Left column
      {
        placeholder: {
          options: {
            name: "left", type: "body",
            x: 0.6, y: 1.1, w: 4.1, h: 4.0,
            fontFace: p.bodyFont, fontSize: 14, color: p.text_dark,
            align: "left", valign: "top",
          },
        },
      },
      // Right column
      {
        placeholder: {
          options: {
            name: "right", type: "body",
            x: 5.3, y: 1.1, w: 4.1, h: 4.0,
            fontFace: p.bodyFont, fontSize: 14, color: p.text_dark,
            align: "left", valign: "top",
          },
        },
      },
    ],
  });

  // ── MASTER: Closing Slide ────────────────────────────
  pres.defineSlideMaster({
    title: "CLOSING_SLIDE",
    background: { color: p.bg_dark },
    objects: [
      { rect: { x: 0, y: 4.8, w: 10, h: 0.825, fill: { color: p.secondary } } },
      {
        placeholder: {
          options: {
            name: "title", type: "title",
            x: 0.8, y: 1.5, w: 8.4, h: 1.5,
            fontFace: p.headerFont, fontSize: 36, color: p.text_light,
            bold: true, align: "center", valign: "middle",
          },
        },
      },
      {
        placeholder: {
          options: {
            name: "body", type: "body",
            x: 0.8, y: 3.2, w: 8.4, h: 1.0,
            fontFace: p.bodyFont, fontSize: 16, color: p.text_light,
            align: "center", valign: "top",
          },
        },
      },
    ],
  });

  // ── Generate sample slides so Pandoc can pick up the masters ──
  const titleSlide = pres.addSlide({ masterName: "TITLE_SLIDE" });
  titleSlide.addText("Presentation Title", { placeholder: "title" });
  titleSlide.addText("Subtitle goes here", { placeholder: "subtitle" });

  const contentSlide = pres.addSlide({ masterName: "CONTENT_SLIDE" });
  contentSlide.addText("Content Slide", { placeholder: "title" });
  contentSlide.addText("Body text placeholder", { placeholder: "body" });

  const sectionSlide = pres.addSlide({ masterName: "SECTION_BREAK" });
  sectionSlide.addText("Section Title", { placeholder: "title" });
  sectionSlide.addText("Section description", { placeholder: "body" });

  const twoColSlide = pres.addSlide({ masterName: "TWO_COLUMN" });
  twoColSlide.addText("Two Columns", { placeholder: "title" });

  const closingSlide = pres.addSlide({ masterName: "CLOSING_SLIDE" });
  closingSlide.addText("Thank You", { placeholder: "title" });
  closingSlide.addText("Questions?", { placeholder: "body" });

  pres.writeFile({ fileName: outputPath }).then(() => {
    console.log(`Template created: ${outputPath} (palette: ${paletteName})`);
    console.log(`Masters: TITLE_SLIDE, CONTENT_SLIDE, SECTION_BREAK, TWO_COLUMN, CLOSING_SLIDE`);
  });
}

// CLI
const args = process.argv.slice(2);
let output = "wayne_brand_template.pptx";
let palette = "midnight";

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--palette" && args[i + 1]) {
    palette = args[i + 1];
    i++;
  } else if (!args[i].startsWith("--")) {
    output = args[i];
  }
}

createTemplate(output, palette);
