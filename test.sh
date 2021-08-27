#!/bin/bash
if ! git diff-index --quiet HEAD --; then
    echo "Committing local changes to github"
    git add -A && git commit -m "style"
    git push
fi