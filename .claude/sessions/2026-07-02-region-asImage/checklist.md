# Checklist — region: asImage + percentOverlapX/Y

- [x] Investigate Vale style check failure: `style 'Google' does not exist on StylesPath` — fixed: Google package was never synced; ran `vale sync` to download it, added `asImage`/`percentOverlapX`/`percentOverlapY`/`includeImages`/`isAbsoluteOffset` to vocab accept list
- [x] Decide whether `asImage` needs a full example — no example needed (user decision)
