# 🛠️ Web Development Directory

A comprehensive collection of web development fundamentals covering version control and markup.

**Last Updated:** May 2026 | **Status:** ✅ Complete

---

## 📁 Contents

### Git Subdirectory
| File | Type | Size | Description |
|------|------|------|-------------|
| [`git.md`](#-git-markdown-reference) | Markdown | 12.7 KB | Complete Git command reference with explanations |
| [`git.sh`](#-git-shell-reference) | Shell | 12.2 KB | Same commands in shell format (comments only) |

### HTML Subdirectory
| File | Type | Size | Description |
|------|------|------|-------------|
| [`html.md`](#-html-markup-reference) | Markdown | 11.4 KB | Complete HTML tag reference and examples |

---

## 🎯 Quick Navigation

### By Purpose

| I Need To... | File |
|-------------|------|
| Learn Git commands | `Git/git.md` |
| Quick Git reference | `Git/git.sh` (comments) |
| Learn HTML tags | `HTML/html.md` |
| Practice web basics | Read all files in order |

### By Skill Level

**Beginner:**
1. Start with `HTML/html.md` → basics of web structure
2. Then `Git/git.md` → version control fundamentals
3. Practice with small projects

**Intermediate:**
1. Master Git workflows in `Git/git.md`
2. Learn semantic HTML from `HTML/html.md`
3. Combine both in real projects

**Advanced:**
1. Advanced Git workflows (rebasing, stashing, cherry-pick)
2. Semantic HTML best practices
3. Git + HTML collaboration patterns

---

## 🔧 Git Subdirectory

### Git Markdown Reference

**File:** `Git/git.md`  
**Format:** Markdown with syntax highlighting  
**Best For:** Learning, studying, detailed reference  
**Size:** 12.7 KB

**Covers 15 Major Sections:**

| Section | Topics |
|---------|--------|
| 1. Configuration | User identity, editor setup |
| 2. Starting Repository | init, clone |
| 3. Staging & Committing | add, commit, amend |
| 4. Viewing History | log, diff, show |
| 5. Undoing Changes | restore, revert, reset |
| 6. Branches | create, switch, delete, rename |
| 7. Merging & Rebasing | merge, rebase, conflicts |
| 8. Remote Repositories | push, pull, fetch, remote |
| 9. Stashing | stash save/pop/apply |
| 10. Tags | create, push, delete tags |
| 11. Aliases | create shortcuts |
| 12. Tips & Shortcuts | advanced commands |
| 13. .gitignore | ignore patterns |
| 14. Everyday Workflow | typical day-to-day git |
| 15. File System Commands | bash commands (touch, rm, mkdir, etc.) |

**Key Content:**

**Configuration:**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**Core Workflow:**
```bash
git add .                    # Stage changes
git commit -m "message"      # Save locally
git push origin main         # Send to remote
```

**Branching:**
```bash
git switch -c feature-name   # Create & switch branch
git merge feature-name       # Merge into current branch
```

**File System Commands (Section 15):**
- **touch** — create files
- **rm** — delete files/folders
- **mkdir** — create directories
- **mv** — move/rename
- **cp** — copy files
- **ls** — list files
- **cat** — view file contents

---

### Git Shell Reference

**File:** `Git/git.sh`  
**Format:** Shell script with bash comments  
**Best For:** Quick lookup, copying commands directly  
**Size:** 12.2 KB

**Structure:**
- Same 15 sections as git.md
- Commands with inline comment explanations
- No execution (all comments)
- Copy-paste friendly format

**Usage:**
```bash
# View the file
cat git.sh

# Search for a command
grep "branch" git.sh

# Copy a section into your terminal
```

---

## 🌐 HTML Subdirectory

### HTML Markup Reference

**File:** `HTML/html.md`  
**Format:** Markdown with code examples  
**Best For:** Learning HTML, quick tag lookup  
**Size:** 11.4 KB

**Covers 12 Major Sections:**

| Section | Topics |
|---------|--------|
| 1. Page Structure | DOCTYPE, html, head, body, title |
| 2. Text & Headings | h1–h6, p, br, hr, blockquote, pre, code |
| 3. Links & Navigation | a href, target, download, mailto, tel |
| 4. Images & Media | img, video, audio, iframe |
| 5. Lists | ul, ol, dl, nested lists |
| 6. Tables | table, thead, tbody, tfoot, colspan, rowspan |
| 7. Forms & Inputs | form, input types, textarea, select, button |
| 8. Semantic Elements | header, nav, main, article, section, aside, footer |
| 9. Div, Span & Grouping | block vs inline, when to use each |
| 10. Meta & Head Tags | meta, link, style, script, charset, viewport |
| 11. Inline Text Formatting | strong, em, mark, sub, sup, abbr, kbd |
| 12. Miscellaneous | comments, special characters, details, progress |

**Key Content:**

**Page Structure (HTML5 Boilerplate):**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page Title</title>
  </head>
  <body>
    <!-- Your content -->
  </body>
</html>
```

**Semantic Structure:**
```html
<header>Navigation & logo</header>
<nav>Links</nav>
<main>
  <article>Blog post</article>
  <section>Content group</section>
  <aside>Sidebar</aside>
</main>
<footer>Copyright & info</footer>
```

**Forms:**
```html
<form action="/submit" method="POST">
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" required />
  <button type="submit">Submit</button>
</form>
```

**Tables:**
```html
<table>
  <thead><tr><th>Header</th></tr></thead>
  <tbody><tr><td>Data</td></tr></tbody>
</table>
```

---

## 🎓 Learning Paths

### Path 1: Git First (Recommended for Developers)
1. **Day 1:** Read Git Configuration + Starting Repository
2. **Day 2:** Learn Staging, Committing, Viewing History
3. **Day 3:** Master Branches
4. **Day 4:** Learn Merging & Remotes
5. **Day 5:** Practice everyday workflow

**Why:** You'll use Git immediately to version control your projects.

---

### Path 2: HTML First (Recommended for Front-End)
1. **Day 1:** Read Page Structure + Text & Headings
2. **Day 2:** Learn Links, Images, Lists
3. **Day 3:** Master Tables + Forms
4. **Day 4:** Study Semantic Elements
5. **Day 5:** Review Meta Tags + Accessibility

**Why:** You need to write HTML before you can effectively use Git with it.

---

### Path 3: Integrated (Balanced Approach)
**Week 1:**
- Day 1–2: HTML basics (structure, text, links)
- Day 3–4: Git basics (config, init, commit)
- Day 5: Combine — write HTML, commit with Git

**Week 2:**
- Day 1–2: HTML forms & tables
- Day 3–4: Git branching & merging
- Day 5: Create a project repo with HTML files

**Week 3:**
- Day 1–2: HTML semantics & accessibility
- Day 3–4: Git workflows & remotes
- Day 5: Push HTML project to GitHub

---

## 📋 Git Quick Reference

### Essential Commands

**Setup:**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**Start:**
```bash
git init                                    # Create repo
git clone https://github.com/user/repo.git # Copy repo
```

**Daily Work:**
```bash
git status                    # Check what changed
git add .                     # Stage all changes
git commit -m "message"       # Save locally
git pull origin main          # Get latest from remote
git push origin main          # Send your changes
```

**Branches:**
```bash
git switch -c feature-name    # Create & switch
git merge feature-name        # Merge into current
```

**Undo:**
```bash
git restore file.txt          # Discard unstaged changes
git reset --soft HEAD~1       # Undo last commit, keep changes
```

---

## 📋 HTML Quick Reference

### Essential Tags

**Structure:**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Page Title</title>
  </head>
  <body>
    <!-- Content here -->
  </body>
</html>
```

**Text:**
```html
<h1>Main Heading</h1>
<h2>Subheading</h2>
<p>Paragraph text</p>
<strong>Bold/important</strong>
<em>Italic/emphasized</em>
```

**Navigation:**
```html
<header>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</header>
```

**Content:**
```html
<main>
  <article>
    <h2>Article Title</h2>
    <p>Content...</p>
  </article>
  
  <section>
    <h3>Section Title</h3>
    <p>More content...</p>
  </section>
</main>
```

**Forms:**
```html
<form action="/submit" method="POST">
  <input type="text" name="username" required />
  <input type="email" name="email" />
  <button type="submit">Submit</button>
</form>
```

---

## 🔑 Key Concepts

### Git Concepts to Master

1. **Commits** — snapshots of your code
2. **Branches** — parallel development lines
3. **Merging** — combining branches
4. **Remotes** — external repositories
5. **Staging** — preparing changes for commit
6. **History** — viewing past commits

**Golden Rule:** Commit early, commit often, with clear messages.

---

### HTML Concepts to Master

1. **Semantics** — using meaningful tags (`<article>` vs `<div>`)
2. **Accessibility** — alt text, labels, proper heading hierarchy
3. **Structure** — proper nesting and organization
4. **Forms** — user input and validation
5. **Metadata** — title, description, viewport, charset
6. **Responsiveness** — mobile-friendly design considerations

**Golden Rule:** Write semantic, accessible HTML that works without CSS or JavaScript.

---

## ✅ Best Practices Checklists

### Git Best Practices

- ✅ Always pull before pushing
- ✅ Commit frequently with clear messages
- ✅ Use branches for features
- ✅ Write meaningful commit messages (use prefixes like `feat:`, `fix:`, `docs:`)
- ✅ Never force push on shared branches
- ✅ Keep `.gitignore` up to date
- ✅ Review changes before committing (`git diff`)

### HTML Best Practices

- ✅ Use semantic elements (`<section>`, `<article>`, not just `<div>`)
- ✅ Always include `alt` text on images
- ✅ One `<h1>` per page
- ✅ Proper heading hierarchy (h1 → h2 → h3, not h1 → h3)
- ✅ Use `<label>` with form inputs
- ✅ Include `<meta charset="UTF-8">` and viewport
- ✅ Validate HTML with W3C validator
- ✅ Use semantic HTML for better SEO and accessibility

---

## 🔗 Commit Message Prefixes

For clear, scannable history:

| Prefix | Use For |
|--------|---------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `style:` | Formatting only |
| `refactor:` | Code restructuring |
| `test:` | Tests |
| `chore:` | Build/tooling |

**Example:** `git commit -m "feat: add user authentication"`

---

## 🎯 Project Ideas to Practice

### Beginner Project
**Task:** Create a simple HTML website, version it with Git

1. Create HTML files: `index.html`, `about.html`, `contact.html`
2. Initialize Git repo: `git init`
3. Make commits as you add content
4. Push to GitHub

**Commands Used:**
```bash
git init
git add .
git commit -m "feat: initial project structure"
git remote add origin https://github.com/user/project.git
git push -u origin main
```

---

### Intermediate Project
**Task:** Create a multi-branch website, merge features

1. Create `main` branch with home page
2. Create `feature/about` branch, add about page
3. Create `feature/contact` branch, add contact form
4. Merge features back to main

**Git Workflow:**
```bash
git switch -c feature/about
# Make changes
git commit -m "feat: add about page"
git switch main
git merge feature/about
git push origin main
```

---

## 📞 Troubleshooting

### Common Git Issues

**"I committed to the wrong branch"**
```bash
git reset --soft HEAD~1  # Undo commit, keep changes
git switch correct-branch
git commit -m "message"
```

**"I want to undo my last commit"**
```bash
git reset --soft HEAD~1  # Keep changes
# OR
git reset --hard HEAD~1  # Discard changes
```

**"I need to see what changed in a commit"**
```bash
git show abc1234  # Replace with commit hash
```

---

### Common HTML Issues

**"Why isn't my form submitting?"**
- Check `<form action="/submit" method="POST">`
- Ensure `<button type="submit">` is present
- All inputs should have `name` attribute

**"My page isn't responsive"**
- Add `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Use CSS media queries or flexible layouts

**"My images aren't showing"**
- Check file path: relative vs absolute
- Always include `alt="description"`
- Verify image file exists

---

## 📚 Next Topics to Learn

After mastering Git & HTML:

1. **CSS** — styling your HTML
2. **JavaScript** — interactivity
3. **Git Collaboration** — working with teams
4. **GitHub Pages** — hosting static sites
5. **CSS Flexbox & Grid** — modern layouts
6. **Responsive Design** — mobile-first development

---

## 🎯 Key Takeaways

### Git
- **What:** Version control system for tracking code changes
- **Why:** Backup, history, collaboration, branching
- **When:** Every project you create
- **Master:** Commits, branches, merging, remote push/pull

### HTML
- **What:** Markup language that structures web content
- **Why:** Foundation of all websites
- **When:** Every web project starts with HTML
- **Master:** Semantics, forms, accessibility, structure

---

> **Remember:** Git protects your code. HTML structures your content. Together, they're the foundation of web development.

---

**Status:** ✅ Complete & Ready to Use  
**Last Updated:** May 2026  
**Difficulty:** Beginner to Intermediate  
**Target Audience:** Web developers, version control learners, HTML learners
