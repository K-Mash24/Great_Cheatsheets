#!/bin/bash 
# Git Configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Configuring a new folder
mkdir my-repo               # Create a new directory "my-repo"
cd my-repo                 # Change into the directory

# Initialize & Clone a git repository
git init                          # Initialize a new repository locally
git clone <url>                   # Clone a repository from GitHub or other remote URL

# File Operations
ls                               # List files in the directory
touch <file>                     # Create a new file
echo "Some content" > <file>     # Add content to a file
cat <file>                       # Display file content
rm <file>                        # Remove a file

# Git operations
git status                        # Check the status of the repository
pwd                              # Print/ Show the working directory

> Keep track of untracked files and tracked files
- Untracked files: Files that are not being tracked by Git (new files).
- Tracked files: Files that are being tracked by Git (modified, staged, or committed).

# Staging and Committing Changes
git status                        # Check status of repository/ Look for changes
git add <file>                    # Stage changes
git add .                         # Stage all changes
git commit -m "message"           # Commit changes
git push                          # Push to remote
git pull                          # Fetch and merge remote changes
git restore .                     # Discard all local changes in working directory
git restore --staged .            # Unstage all files
got restore --staged <file>       # Unstage specific file

# Branching
git branch                        # List branches
git branch <branch-name>          # Create new branch
git checkout <branch-name>        # Switch branch
git checkout -b <branch-name>     # Create and switch to new branch
git merge <branch-name>           # Merge branch

# Commits
git commit -m "message"             # Commit staged changes with saved message
git commit --amend -m "new message" # Amend last commit message
git commit -a -m "message"          # Stage and commit all changes 
git commit -a                       #Commit all changes without message prompt

# Viewing History
git log                           # View commit history
git log --oneline                 # Compact log view
git diff                          # Show unstaged changes
git diff --cached                 # Show staged changes

# Undoing Changes
git restore <file>                # Discard changes in file
git restore --staged <file>       # Unstage file
git reset HEAD~1                  # Undo last commit
git revert <commit-hash>          # Create new commit that undoes changes

# Remote
git remote -v                     # List remote repositories
git remote add origin <url>       # Add remote repository
git fetch                         # Download remote changes

# Stashing
git stash                         # Stash changes
git stash pop                     # Apply stashed changes

# Tagging
git tag <tag-name>                # Create a tag
git push origin <tag-name>        # Push tag to remote