# 🔧 Git Cheatsheet

> A complete reference for everyday Git commands — from setup to advanced workflows.

---

## 📋 Table of Contents

1. [Configuration](#1-configuration)
2. [Starting a Repository](#2-starting-a-repository)
3. [Staging & Committing](#3-staging--committing)
4. [Viewing History & Differences](#4-viewing-history--differences)
5. [Undoing Changes](#5-undoing-changes)
6. [Branches](#6-branches)
7. [Merging & Rebasing](#7-merging--rebasing)
8. [Remote Repositories](#8-remote-repositories)
9. [Stashing](#9-stashing)
10. [Tags](#10-tags)
11. [Aliases](#11-aliases)
12. [Useful Tips & Shortcuts](#12-useful-tips--shortcuts)
13. [.gitignore Quick Reference](#13-gitignore-quick-reference)
14. [Everyday Workflow](#14-everyday-workflow)
15. [File System Commands](#15-file-system-commands)

---

## 1. Configuration

Set up your identity before your first commit.

```bash
git config --global user.name "Your Name"           # Set your name
git config --global user.email "you@example.com"    # Set your email
git config --global core.editor "code --wait"       # Set VS Code as default editor
git config --list                                    # View all config settings
```

---

## 2. Starting a Repository

```bash
git init                          # Initialise a new local repo in current folder
git init my-project               # Initialise a new repo in a new folder
git clone https://github.com/user/repo.git          # Clone a remote repo locally
git clone https://github.com/user/repo.git my-name  # Clone into a custom folder name
```

---

## 3. Staging & Committing

```bash
git status                        # Show working tree status (staged, unstaged, untracked)
git add file.txt                  # Stage a specific file
git add .                         # Stage all changes in current directory
git add -p                        # Interactively stage chunks of changes

git commit -m "Your message"      # Commit staged changes with a message
git commit -am "Your message"     # Stage all tracked files and commit in one step
git commit --amend -m "New msg"   # Edit the last commit message (before pushing)
```

---

## 4. Viewing History & Differences

```bash
git log                           # Full commit history
git log --oneline                 # Compact one-line history
git log --oneline --graph         # Visual branch/merge graph
git log --author="Name"           # Filter commits by author
git log -5                        # Show last 5 commits only

git diff                          # Show unstaged changes
git diff --staged                 # Show staged changes (ready to commit)
git diff branch1..branch2         # Compare two branches
git show abc1234                  # Show details of a specific commit
```

---

## 5. Undoing Changes

```bash
git restore file.txt              # Discard unstaged changes in a file
git restore --staged file.txt     # Unstage a file (keep changes in working dir)

git revert abc1234                # Create a new commit that undoes a specific commit
git reset --soft HEAD~1           # Undo last commit, keep changes staged
git reset --mixed HEAD~1          # Undo last commit, keep changes unstaged (default)
git reset --hard HEAD~1           # Undo last commit and DISCARD all changes ⚠️

git clean -fd                     # Remove all untracked files and directories ⚠️
```

> ⚠️ **Warning:** `--hard` reset and `clean -fd` are destructive. Avoid on shared or public branches.

---

## 6. Branches

```bash
git branch                        # List all local branches
git branch -a                     # List local and remote branches
git branch feature-login          # Create a new branch
git switch feature-login          # Switch to a branch
git switch -c feature-login       # Create and switch to a new branch in one step
git checkout -b feature-login     # Older equivalent of switch -c

git branch -d feature-login       # Delete a branch (safe — only if merged)
git branch -D feature-login       # Force delete a branch (even if not merged)
git branch -m old-name new-name   # Rename a branch
```

---

## 7. Merging & Rebasing

```bash
git merge feature-login           # Merge a branch into the current branch
git merge --no-ff feature-login   # Merge with a merge commit (no fast-forward)
git merge --abort                 # Abort a merge in progress

git rebase main                   # Rebase current branch onto main
git rebase --abort                # Abort a rebase in progress
git rebase --continue             # Continue rebase after resolving conflicts
```

> 💡 **Rule of thumb:** Use `merge` for shared/public branches. Use `rebase` for cleaning up local history.

---

## 8. Remote Repositories

```bash
git remote -v                                         # List remote connections
git remote add origin https://github.com/user/repo.git  # Add a remote
git remote remove origin                              # Remove a remote connection
git remote rename origin upstream                     # Rename a remote

git fetch origin                  # Download changes from remote (don't merge yet)
git pull origin main              # Fetch and merge remote main into current branch
git pull --rebase origin main     # Fetch and rebase instead of merge

git push origin main              # Push local main to remote
git push -u origin main           # Push and set upstream tracking (first time)
git push --force-with-lease       # Safer force push (checks remote hasn't changed)
git push origin --delete feature-login  # Delete a remote branch
```

---

## 9. Stashing

Temporarily save work without committing.

```bash
git stash                         # Stash current uncommitted changes
git stash push -m "my stash"      # Stash with a descriptive label
git stash list                    # View all stashes
git stash pop                     # Apply most recent stash and remove it
git stash apply stash@{1}         # Apply a specific stash (keep it in list)
git stash drop stash@{0}          # Delete a specific stash
git stash clear                   # Delete all stashes
```

---

## 10. Tags

Mark specific points in history such as releases.

```bash
git tag                           # List all tags
git tag v1.0.0                    # Create a lightweight tag
git tag -a v1.0.0 -m "Release"   # Create an annotated tag with a message
git push origin v1.0.0            # Push a specific tag to remote
git push origin --tags            # Push all tags to remote
git tag -d v1.0.0                 # Delete a local tag
git push origin --delete v1.0.0  # Delete a remote tag
```

---

## 11. Aliases

Create shortcuts for commonly used commands.

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --all"
```

| Alias | Expands To |
|-------|-----------|
| `git st` | `git status` |
| `git co` | `git checkout` |
| `git br` | `git branch` |
| `git lg` | `git log --oneline --graph --all` |

---

## 12. Useful Tips & Shortcuts

```bash
git shortlog -sn                  # Summary of commits per author
git blame file.txt                # Show who last changed each line of a file
git cherry-pick abc1234           # Apply a specific commit from another branch
git bisect start                  # Start binary search for a bug-introducing commit

# View a file as it was at a specific commit
git show abc1234:path/to/file.txt

# List files changed in the last commit
git diff --name-only HEAD~1 HEAD

# Unstage everything
git reset HEAD

# Export the repo as a zip file
git archive --format=zip HEAD > project.zip
```

---

## 13. .gitignore Quick Reference

Create a `.gitignore` file in your project root to exclude files from tracking.

```bash
# Common patterns
*.log               # Ignore all .log files
node_modules/       # Ignore the node_modules folder
.env                # Ignore environment variable files
dist/               # Ignore build output folder
*.DS_Store          # Ignore macOS system files
__pycache__/        # Ignore Python cache folder
```

To stop tracking a file that's already been committed:

```bash
git rm --cached file.txt          # Remove from tracking (won't delete it locally)
```

> 💡 Use [gitignore.io](https://www.toptal.com/developers/gitignore) to generate `.gitignore` templates for your stack.

---

## 14. Everyday Workflow

A typical day-to-day Git workflow:

```bash
# 1. Start new work on a feature branch
git switch -c my-feature

# 2. Make your changes, then stage and commit
git add .
git commit -m "feat: describe what you did"

# 3. Sync with the remote before pushing
git pull origin main

# 4. Push your branch to remote
git push origin my-feature

# 5. Merge into main when done
git switch main
git merge my-feature
git push origin main

# 6. Clean up the feature branch
git branch -d my-feature
git push origin --delete my-feature
```

---

### Commit Message Convention

Good commit messages make history easy to read. A common format is:

| Prefix | Use For |
|--------|---------|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `docs:` | Documentation changes |
| `style:` | Formatting, no logic change |
| `refactor:` | Code restructure, no feature/fix |
| `test:` | Adding or updating tests |
| `chore:` | Build process or tooling changes |

**Example:** `git commit -m "feat: add login form validation"`

---

> ✅ **Quick Reminder:** `add` → stages changes, `commit` → saves locally, `push` → sends to remote.  
> When in doubt, `git status` is always your best first command.

---

## 15. File System Commands

These are **Bash/Linux** commands used alongside Git to manage files and folders in your project. Git then tracks the changes they make.

### `touch` — Create Files

```bash
touch file.txt                  # Create a new empty file
touch file1.txt file2.txt       # Create multiple files at once
touch src/index.html            # Create a file inside an existing folder
```

### `rm` — Remove Files & Folders

```bash
rm file.txt                     # Delete a file
rm file1.txt file2.txt          # Delete multiple files
rm -r my-folder/                # Delete a folder and all its contents
rm -rf my-folder/               # Force delete (no confirmation) ⚠️
```

> ⚠️ **Warning:** `rm` is permanent — there is no trash or undo.

### `mkdir` — Create Directories

```bash
mkdir my-folder                 # Create a new folder
mkdir -p src/components/ui      # Create nested folders in one step
mkdir folder1 folder2           # Create multiple folders at once
```

### `mv` — Move or Rename

```bash
mv old-name.txt new-name.txt    # Rename a file
mv file.txt src/                # Move a file into a folder
mv folder/ new-location/        # Move a folder
mv *.txt archive/               # Move all .txt files into archive/
```

### `cp` — Copy Files & Folders

```bash
cp file.txt copy.txt            # Copy a file
cp file.txt src/                # Copy a file into a folder
cp -r my-folder/ backup/        # Copy a folder and all its contents
cp *.html templates/            # Copy all .html files into templates/
```

### `ls` — List Files & Directories

```bash
ls                              # List files in current directory
ls -l                           # Detailed list (permissions, size, date)
ls -a                           # Show hidden files (e.g. .gitignore, .env)
ls -la                          # Detailed list including hidden files
ls src/                         # List files inside a specific folder
```

### `cat` — View File Contents

```bash
cat file.txt                    # Print file contents to terminal
cat file1.txt file2.txt         # Print multiple files in sequence
cat -n file.txt                 # Print with line numbers
cat > file.txt                  # Write to a file (overwrites) — Ctrl+C to save
cat >> file.txt                 # Append to a file — Ctrl+C to save
```

---

### File System + Git: Common Combined Workflow

```bash
# Create a new file and immediately stage it
touch README.md
git add README.md
git commit -m "docs: add README"

# Rename a file and stage the change
mv old-name.txt new-name.txt
git add .
git commit -m "refactor: rename file"

# Delete a file and stage the removal
rm unwanted.txt
git add .
git commit -m "chore: remove unwanted file"

# Or use git rm to delete and stage in one step
git rm unwanted.txt
git commit -m "chore: remove unwanted file"
```

| Command | Git Equivalent | Notes |
|---------|---------------|-------|
| `rm file.txt` + `git add .` | `git rm file.txt` | Removes and stages deletion |
| `mv old new` + `git add .` | `git mv old new` | Renames and stages the change |