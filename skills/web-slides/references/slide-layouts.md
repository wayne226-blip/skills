# Slide Layout Templates

Each layout is a Tailwind HTML snippet for a 1920x1080 slide. Replace `{PLACEHOLDER}` tokens with actual content. All layouts use theme colours via `bg-primary`, `text-accent`, etc.

---

## 1. Title Slide

Centred headline with subtitle. Gradient background. First impression.

```html
<section class="slide flex flex-col items-center justify-center bg-linear-to-br from-surface via-primary to-surface text-center p-20" data-slide="N">
  <h1 class="font-heading text-8xl font-bold text-text mb-8 leading-tight">{TITLE}</h1>
  <p class="font-body text-3xl text-secondary max-w-4xl">{SUBTITLE}</p>
  <div class="mt-12 w-24 h-1 bg-accent rounded-full"></div>
  <p class="font-body text-xl text-secondary/60 mt-8">{AUTHOR_OR_DATE}</p>
</section>
```

---

## 2. Two Column

Left text, right content (could be a list, visual element, or code block).

```html
<section class="slide flex bg-surface p-20 gap-16" data-slide="N">
  <div class="flex-1 flex flex-col justify-center">
    <h2 class="font-heading text-6xl font-bold text-primary mb-8">{HEADING}</h2>
    <p class="font-body text-2xl text-text/80 leading-relaxed">{BODY_TEXT}</p>
  </div>
  <div class="flex-1 flex items-center justify-center">
    <div class="bg-primary/10 rounded-3xl p-12 w-full">
      {RIGHT_CONTENT}
    </div>
  </div>
</section>
```

---

## 3. Three Column

Three equal feature cards. Good for features, benefits, comparisons.

```html
<section class="slide flex flex-col bg-surface p-20" data-slide="N">
  <h2 class="font-heading text-6xl font-bold text-primary mb-16 text-center">{HEADING}</h2>
  <div class="flex-1 flex gap-12">
    <div class="flex-1 bg-primary/5 rounded-2xl p-10 flex flex-col">
      <div class="text-5xl mb-6">{ICON_1}</div>
      <h3 class="font-heading text-3xl font-bold text-primary mb-4">{CARD_1_TITLE}</h3>
      <p class="font-body text-xl text-text/70 leading-relaxed">{CARD_1_BODY}</p>
    </div>
    <div class="flex-1 bg-primary/5 rounded-2xl p-10 flex flex-col">
      <div class="text-5xl mb-6">{ICON_2}</div>
      <h3 class="font-heading text-3xl font-bold text-primary mb-4">{CARD_2_TITLE}</h3>
      <p class="font-body text-xl text-text/70 leading-relaxed">{CARD_2_BODY}</p>
    </div>
    <div class="flex-1 bg-primary/5 rounded-2xl p-10 flex flex-col">
      <div class="text-5xl mb-6">{ICON_3}</div>
      <h3 class="font-heading text-3xl font-bold text-primary mb-4">{CARD_3_TITLE}</h3>
      <p class="font-body text-xl text-text/70 leading-relaxed">{CARD_3_BODY}</p>
    </div>
  </div>
</section>
```

---

## 4. Stats / Big Numbers

3-4 large statistics with labels. High impact, data-driven.

```html
<section class="slide flex flex-col items-center justify-center bg-surface p-20" data-slide="N">
  <h2 class="font-heading text-5xl font-bold text-primary mb-20">{HEADING}</h2>
  <div class="flex gap-20">
    <div class="text-center">
      <div class="font-heading text-9xl font-black text-accent">{STAT_1}</div>
      <div class="font-body text-2xl text-text/60 mt-4">{LABEL_1}</div>
    </div>
    <div class="text-center">
      <div class="font-heading text-9xl font-black text-accent">{STAT_2}</div>
      <div class="font-body text-2xl text-text/60 mt-4">{LABEL_2}</div>
    </div>
    <div class="text-center">
      <div class="font-heading text-9xl font-black text-accent">{STAT_3}</div>
      <div class="font-body text-2xl text-text/60 mt-4">{LABEL_3}</div>
    </div>
  </div>
</section>
```

---

## 5. Quote

Large quote with attribution. Emotional, human, trust-building.

```html
<section class="slide flex flex-col items-center justify-center bg-linear-to-br from-primary to-surface p-24 text-center" data-slide="N">
  <div class="text-8xl text-accent/40 mb-8">"</div>
  <blockquote class="font-heading text-5xl font-medium text-text leading-snug max-w-5xl mb-12">
    {QUOTE_TEXT}
  </blockquote>
  <div class="w-16 h-1 bg-accent rounded-full mb-8"></div>
  <cite class="font-body text-2xl text-secondary not-italic">{ATTRIBUTION}</cite>
</section>
```

---

## 6. Section Divider

Bold section title with accent bar. Marks transitions between topics.

```html
<section class="slide flex items-center bg-primary p-24" data-slide="N">
  <div>
    <div class="w-20 h-2 bg-accent rounded-full mb-10"></div>
    <h2 class="font-heading text-8xl font-bold text-text mb-6">{SECTION_TITLE}</h2>
    <p class="font-body text-3xl text-text/60 max-w-3xl">{SECTION_SUBTITLE}</p>
  </div>
</section>
```

---

## 7. Image + Text (Split)

Half colour block with content. Bold and modern.

```html
<section class="slide flex bg-surface" data-slide="N">
  <div class="w-1/2 bg-linear-to-br from-primary to-accent flex items-center justify-center p-16">
    <div class="text-center text-text">
      {VISUAL_CONTENT_OR_LARGE_ICON}
    </div>
  </div>
  <div class="w-1/2 flex flex-col justify-center p-20">
    <h2 class="font-heading text-5xl font-bold text-primary mb-8">{HEADING}</h2>
    <p class="font-body text-2xl text-text/70 leading-relaxed">{BODY_TEXT}</p>
  </div>
</section>
```

---

## 8. Bullet Points (Styled)

Icon + text rows. Not boring plain bullets — each point has presence.

```html
<section class="slide flex flex-col bg-surface p-20" data-slide="N">
  <h2 class="font-heading text-6xl font-bold text-primary mb-16">{HEADING}</h2>
  <div class="flex-1 flex flex-col justify-center gap-8">
    <div class="flex items-start gap-6">
      <div class="w-12 h-12 bg-accent rounded-xl flex items-center justify-center flex-shrink-0 mt-1">
        <span class="text-white text-xl font-bold">1</span>
      </div>
      <div>
        <h3 class="font-heading text-3xl font-semibold text-primary">{POINT_1_TITLE}</h3>
        <p class="font-body text-xl text-text/60 mt-2">{POINT_1_DETAIL}</p>
      </div>
    </div>
    <div class="flex items-start gap-6">
      <div class="w-12 h-12 bg-accent rounded-xl flex items-center justify-center flex-shrink-0 mt-1">
        <span class="text-white text-xl font-bold">2</span>
      </div>
      <div>
        <h3 class="font-heading text-3xl font-semibold text-primary">{POINT_2_TITLE}</h3>
        <p class="font-body text-xl text-text/60 mt-2">{POINT_2_DETAIL}</p>
      </div>
    </div>
    <div class="flex items-start gap-6">
      <div class="w-12 h-12 bg-accent rounded-xl flex items-center justify-center flex-shrink-0 mt-1">
        <span class="text-white text-xl font-bold">3</span>
      </div>
      <div>
        <h3 class="font-heading text-3xl font-semibold text-primary">{POINT_3_TITLE}</h3>
        <p class="font-body text-xl text-text/60 mt-2">{POINT_3_DETAIL}</p>
      </div>
    </div>
  </div>
</section>
```

---

## 9. Comparison

Side-by-side. Before/after, us vs them, old vs new.

```html
<section class="slide flex flex-col bg-surface p-20" data-slide="N">
  <h2 class="font-heading text-6xl font-bold text-primary mb-16 text-center">{HEADING}</h2>
  <div class="flex-1 flex gap-8">
    <div class="flex-1 bg-primary/5 rounded-2xl p-12 border-2 border-primary/10">
      <h3 class="font-heading text-3xl font-bold text-primary/50 mb-8">{LEFT_LABEL}</h3>
      <ul class="space-y-4">
        <li class="font-body text-xl text-text/60 flex items-start gap-3">
          <span class="text-primary/40 mt-1">&#x2717;</span> {LEFT_POINT_1}
        </li>
        <li class="font-body text-xl text-text/60 flex items-start gap-3">
          <span class="text-primary/40 mt-1">&#x2717;</span> {LEFT_POINT_2}
        </li>
        <li class="font-body text-xl text-text/60 flex items-start gap-3">
          <span class="text-primary/40 mt-1">&#x2717;</span> {LEFT_POINT_3}
        </li>
      </ul>
    </div>
    <div class="flex-1 bg-accent/10 rounded-2xl p-12 border-2 border-accent/30 ring-2 ring-accent/20">
      <h3 class="font-heading text-3xl font-bold text-accent mb-8">{RIGHT_LABEL}</h3>
      <ul class="space-y-4">
        <li class="font-body text-xl text-text flex items-start gap-3">
          <span class="text-accent mt-1">&#x2713;</span> {RIGHT_POINT_1}
        </li>
        <li class="font-body text-xl text-text flex items-start gap-3">
          <span class="text-accent mt-1">&#x2713;</span> {RIGHT_POINT_2}
        </li>
        <li class="font-body text-xl text-text flex items-start gap-3">
          <span class="text-accent mt-1">&#x2713;</span> {RIGHT_POINT_3}
        </li>
      </ul>
    </div>
  </div>
</section>
```

---

## 10. Closing / CTA

Final slide. Call to action, contact info, next steps.

```html
<section class="slide flex flex-col items-center justify-center bg-linear-to-br from-primary via-accent to-primary text-center p-24" data-slide="N">
  <h2 class="font-heading text-7xl font-bold text-text mb-8">{CTA_HEADLINE}</h2>
  <p class="font-body text-3xl text-text/70 max-w-4xl mb-16">{CTA_BODY}</p>
  <div class="bg-text/10 backdrop-blur-sm rounded-2xl px-16 py-8">
    <p class="font-body text-2xl text-text">{CONTACT_OR_URL}</p>
  </div>
</section>
```
