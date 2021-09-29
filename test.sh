#!/bin/bash
direnv allow .


if ! git diff-index --quiet HEAD --; then
    echo "Committing local changes to github"
    echo "adding untracked files"
    git add -A 
    echo "git status:"
    git status
    git commit -m "updating local style changes to images"
    git push
fi