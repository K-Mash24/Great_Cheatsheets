# 🌐 HTML Reference Cheatsheet

> A complete reference guide for HTML tags and elements. Use this to quickly remind yourself of syntax, attributes, and usage.

---

## 📋 Table of Contents

1. [Page Structure](#1-page-structure)
2. [Text & Headings](#2-text--headings)
3. [Links & Navigation](#3-links--navigation)
4. [Images & Media](#4-images--media)
5. [Lists](#5-lists)
6. [Tables](#6-tables)
7. [Forms & Inputs](#7-forms--inputs)
8. [Semantic Elements](#8-semantic-elements)
9. [Div, Span & Grouping](#9-div-span--grouping)
10. [Meta & Head Tags](#10-meta--head-tags)
11. [Inline Text Formatting](#11-inline-text-formatting)
12. [Miscellaneous](#12-miscellaneous)

---

## 1. Page Structure

Every HTML page follows this base structure:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page Title</title>
  </head>
  <body>
    <!-- Your content goes here -->
  </body>
</html>
```

| Tag | Purpose |
|-----|---------|
| `<!DOCTYPE html>` | Declares the document as HTML5 |
| `<html>` | Root element of the page |
| `<head>` | Contains metadata (not visible on page) |
| `<body>` | Contains all visible content |
| `<title>` | Sets the browser tab title |

---

## 2. Text & Headings

```html
<h1>Heading 1 — Main Title</h1>
<h2>Heading 2 — Section Title</h2>
<h3>Heading 3 — Sub-section</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6 — Smallest</h6>

<p>This is a paragraph of text.</p>

<br />        <!-- Line break (self-closing) -->
<hr />        <!-- Horizontal rule / divider -->

<blockquote cite="https://source.com">
  A quoted block of text from another source.
</blockquote>

<pre>
  Preformatted text — preserves spaces and line breaks.
</pre>

<code>inline code snippet</code>
```

> 💡 Only use **one `<h1>`** per page — it's the main heading and important for SEO.

---

## 3. Links & Navigation

```html
<!-- Basic link -->
<a href="https://example.com">Visit Example</a>

<!-- Open in new tab -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">Open in new tab</a>

<!-- Link to a section on the same page -->
<a href="#section-id">Jump to section</a>

<!-- Email link -->
<a href="mailto:hello@example.com">Send Email</a>

<!-- Phone link -->
<a href="tel:+1234567890">Call Us</a>

<!-- Download link -->
<a href="file.pdf" download>Download PDF</a>
```

| Attribute | Purpose |
|-----------|---------|
| `href` | URL or destination |
| `target="_blank"` | Opens in a new tab |
| `rel="noopener noreferrer"` | Security best practice for `_blank` |
| `download` | Triggers file download instead of navigation |

---

## 4. Images & Media

```html
<!-- Basic image -->
<img src="image.jpg" alt="Description of image" />

<!-- Image with size -->
<img src="photo.png" alt="Photo" width="300" height="200" />

<!-- Responsive image -->
<img src="banner.jpg" alt="Banner" style="max-width: 100%; height: auto;" />

<!-- Video -->
<video src="video.mp4" controls width="600">
  Your browser does not support the video tag.
</video>

<!-- Video with multiple sources -->
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <source src="video.ogg" type="video/ogg" />
</video>

<!-- Audio -->
<audio controls>
  <source src="audio.mp3" type="audio/mpeg" />
</audio>

<!-- Embed external content (e.g. YouTube) -->
<iframe
  src="https://www.youtube.com/embed/VIDEO_ID"
  width="560"
  height="315"
  allowfullscreen>
</iframe>
```

> 💡 Always include `alt` on images — it's required for accessibility and SEO.

---

## 5. Lists

```html
<!-- Unordered list (bullet points) -->
<ul>
  <li>Item One</li>
  <li>Item Two</li>
  <li>Item Three</li>
</ul>

<!-- Ordered list (numbered) -->
<ol>
  <li>First step</li>
  <li>Second step</li>
  <li>Third step</li>
</ol>

<!-- Ordered list starting at a different number -->
<ol start="5">
  <li>Fifth item</li>
  <li>Sixth item</li>
</ol>

<!-- Nested list -->
<ul>
  <li>Fruits
    <ul>
      <li>Apple</li>
      <li>Banana</li>
    </ul>
  </li>
  <li>Vegetables</li>
</ul>

<!-- Description list -->
<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language — the structure of web pages.</dd>
  <dt>CSS</dt>
  <dd>Cascading Style Sheets — the styling of web pages.</dd>
</dl>
```

---

## 6. Tables

```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Age</th>
      <th>Country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Alice</td>
      <td>25</td>
      <td>Kenya</td>
    </tr>
    <tr>
      <td>Bob</td>
      <td>30</td>
      <td>Ghana</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="3">End of table</td>
    </tr>
  </tfoot>
</table>
```

| Tag | Purpose |
|-----|---------|
| `<table>` | Creates the table |
| `<thead>` | Table header group |
| `<tbody>` | Table body group |
| `<tfoot>` | Table footer group |
| `<tr>` | Table row |
| `<th>` | Header cell (bold & centered by default) |
| `<td>` | Data cell |
| `colspan="2"` | Cell spans 2 columns |
| `rowspan="2"` | Cell spans 2 rows |

---

## 7. Forms & Inputs

```html
<form action="/submit" method="POST">

  <!-- Text input -->
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" placeholder="Enter your name" required />

  <!-- Email input -->
  <input type="email" name="email" placeholder="you@example.com" />

  <!-- Password input -->
  <input type="password" name="password" />

  <!-- Number input -->
  <input type="number" name="age" min="1" max="120" />

  <!-- Checkbox -->
  <input type="checkbox" id="agree" name="agree" />
  <label for="agree">I agree to the terms</label>

  <!-- Radio buttons -->
  <input type="radio" id="male" name="gender" value="male" />
  <label for="male">Male</label>
  <input type="radio" id="female" name="gender" value="female" />
  <label for="female">Female</label>

  <!-- Dropdown / Select -->
  <select name="country">
    <option value="">-- Select Country --</option>
    <option value="ke">Kenya</option>
    <option value="ug">Uganda</option>
    <option value="tz">Tanzania</option>
  </select>

  <!-- Textarea -->
  <textarea name="message" rows="5" cols="40" placeholder="Your message..."></textarea>

  <!-- File upload -->
  <input type="file" name="upload" accept=".pdf,.jpg,.png" />

  <!-- Hidden input -->
  <input type="hidden" name="user_id" value="42" />

  <!-- Submit button -->
  <button type="submit">Submit</button>

  <!-- Reset button -->
  <button type="reset">Reset</button>

</form>
```

### Common Input Types

| Type | Usage |
|------|-------|
| `text` | Single-line text |
| `email` | Email address with validation |
| `password` | Masked password field |
| `number` | Numeric input |
| `checkbox` | On/off toggle |
| `radio` | Select one from a group |
| `file` | File upload |
| `date` | Date picker |
| `range` | Slider input |
| `hidden` | Invisible data passed in form |
| `submit` | Submits the form |

---

## 8. Semantic Elements

Semantic tags describe the **meaning** of content, not just its appearance. They improve accessibility and SEO.

```html
<header>
  <!-- Site logo, nav, and top-level content -->
</header>

<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>

<main>
  <!-- Primary content of the page (only one per page) -->

  <article>
    <!-- Self-contained content like a blog post or news article -->
    <h2>Article Title</h2>
    <p>Article content...</p>
  </article>

  <section>
    <!-- Thematic grouping of content with a heading -->
    <h2>Section Title</h2>
    <p>Section content...</p>
  </section>

  <aside>
    <!-- Secondary content: sidebars, related links, ads -->
  </aside>

</main>

<footer>
  <!-- Copyright, links, contact info -->
  <p>&copy; 2026 My Website</p>
</footer>
```

| Tag | Purpose |
|-----|---------|
| `<header>` | Top section of page or section |
| `<nav>` | Navigation links |
| `<main>` | Main unique content of the page |
| `<article>` | Standalone, reusable content |
| `<section>` | Thematic content grouping |
| `<aside>` | Supplementary content |
| `<footer>` | Bottom section of page or section |
| `<figure>` | Image or diagram with caption |
| `<figcaption>` | Caption for a `<figure>` |
| `<time>` | Machine-readable date/time |

---

## 9. Div, Span & Grouping

```html
<!-- div: block-level container for grouping -->
<div class="card">
  <h3>Card Title</h3>
  <p>Card content here.</p>
</div>

<!-- span: inline container for styling part of text -->
<p>My favourite colour is <span style="color: red;">red</span>.</p>
```

| Tag | Type | Use |
|-----|------|-----|
| `<div>` | Block | Group and layout large sections |
| `<span>` | Inline | Style or target part of text |

> 💡 Prefer semantic tags over `<div>` where meaning applies — use `<section>` instead of `<div class="section">`.

---

## 10. Meta & Head Tags

```html
<head>
  <!-- Character encoding -->
  <meta charset="UTF-8" />

  <!-- Responsive viewport -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Page description (shown in search results) -->
  <meta name="description" content="A great HTML cheatsheet for beginners." />

  <!-- Author -->
  <meta name="author" content="Your Name" />

  <!-- Page title (browser tab + SEO) -->
  <title>My Website</title>

  <!-- Link to external CSS -->
  <link rel="stylesheet" href="styles.css" />

  <!-- Favicon -->
  <link rel="icon" href="favicon.ico" type="image/x-icon" />

  <!-- Link to external font (e.g. Google Fonts) -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet" />

  <!-- Internal CSS -->
  <style>
    body { font-family: sans-serif; }
  </style>

  <!-- JavaScript (at end of body is best practice) -->
  <script src="script.js" defer></script>
</head>
```

---

## 11. Inline Text Formatting

```html
<strong>Bold / important text</strong>
<em>Italic / emphasized text</em>
<u>Underlined text</u>
<s>Strikethrough text</s>
<mark>Highlighted text</mark>
<small>Small/fine print text</small>
<sub>Subscript</sub> e.g. H<sub>2</sub>O
<sup>Superscript</sup> e.g. x<sup>2</sup>
<abbr title="HyperText Markup Language">HTML</abbr>
<q>Short inline quotation</q>
<cite>Title of a work</cite>
<kbd>Ctrl + C</kbd>   <!-- Keyboard input -->
<var>x = y + z</var>  <!-- Variable in code/math -->
```

| Tag | Output |
|-----|--------|
| `<strong>` | **Bold** |
| `<em>` | *Italic* |
| `<mark>` | Highlighted |
| `<s>` | ~~Strikethrough~~ |
| `<sub>` | H₂O |
| `<sup>` | x² |
| `<kbd>` | Keyboard key style |
| `<abbr>` | Tooltip on hover |

---

## 12. Miscellaneous

```html
<!-- HTML Comment (not visible in browser) -->
<!-- This is a comment -->

<!-- Non-breaking space (prevents line break) -->
&nbsp;

<!-- Special characters -->
&lt;    <!-- < -->
&gt;    <!-- > -->
&amp;   <!-- & -->
&copy;  <!-- © -->
&reg;   <!-- ® -->
&trade; <!-- ™ -->
&euro;  <!-- € -->

<!-- Details / accordion -->
<details>
  <summary>Click to expand</summary>
  <p>Hidden content revealed on click.</p>
</details>

<!-- Progress bar -->
<progress value="70" max="100">70%</progress>

<!-- Tooltip via title attribute -->
<p title="This is a tooltip">Hover over me</p>
```

---

> ✅ **Quick Reminder:** HTML = **structure**, CSS = **style**, JavaScript = **behaviour**.  
> Always write valid, semantic HTML and test in a browser as you build.
