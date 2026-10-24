# Git Troubleshooting Guide

## Working Directory and Staging
git status shows modified, staged, and untracked files. Use git add to stage changes and git commit to save a snapshot. A commit only includes changes that have been staged.

## Merge Conflicts
A merge conflict occurs when Git cannot automatically combine changes. Open each conflicted file, review the conflict markers, keep the intended content, remove the markers, and run git add followed by git commit.

## Branches
Branches allow development work to happen independently. Use git switch -c feature-name to create and switch to a branch. Merge completed work into the target branch after reviewing and testing it.

## Ignoring Files
Use .gitignore to exclude generated files, virtual environments, secrets, and caches. If a file is already tracked, adding it to .gitignore does not automatically remove it from Git tracking.
