# Do search engines and AI agents use the keywords meta tag? (researched 2026-10-19)

Legend: **[verified]** = I read the primary source or ran the test myself. **[secondary]** = reported
by a third party; primary not read. **[inference]** = my reasoning, not directly evidenced.

## Google

- **[verified]** Google Search Central blog, Sept 21, 2009, "Google does not use the keywords meta
  tag in web ranking": "Google doesn't use the keywords meta tag in our web search ranking." The
  post now carries a banner: "Some of the information may be outdated ... However Google still
  doesn't support the keywords meta tag."
  https://developers.google.com/search/blog/2009/09/google-does-not-use-keywords-meta-tag
- **[verified]** Google's current meta-tags doc (last updated 2025-12-10) lists it under unsupported
  tags: "The meta-keyword tag is not used by Google Search, and it has no effect on indexing and
  ranking at all." https://developers.google.com/search/docs/crawling-indexing/special-tags
- Note: the 2009 post scoped it to *ranking*; the 2025 doc goes further (*indexing* too).

## Bing

- **[secondary]** 2011: Duane Forrester (Bing webmaster outreach) said meta keywords "is a signal," then
  agreed with Danny Sullivan it's "more of a spam signal." Search Engine Land, "The Meta Keywords Tag
  Lives At Bing & Why Only Spammers Should Use It."
  https://searchengineland.com/the-meta-keywords-tag-lives-at-bing-why-only-spammers-should-use-it-96874
  (403 to my fetch; quotes via search results.)
- **[secondary]** 2014: Forrester on the Bing Webmaster Blog called the tag "pretty clear… dead in
  terms of SEO value."
- Uncertain: no current (2020s) official Bing statement found.

## AI crawlers and agents

1. **AI search features sit on top of search indexes.**
   - **[verified, title/summary]** Google's "AI features and your website" covers AI Overviews / AI
     Mode. **[secondary]** It reportedly says: "There are no additional requirements to appear in AI
     Overviews or AI Mode, nor other special optimizations necessary"; eligibility = indexed and
     snippet-eligible in normal Search. https://developers.google.com/search/docs/appearance/ai-features
   - **[inference]** So Google's AI features inherit Google Search's treatment: keywords tag ignored.
     Copilot sits on Bing (spam signal at most).
2. **Crawler docs mention only robots.txt, never meta keywords.**
   - **[secondary]** OpenAI (OAI-SearchBot for ChatGPT search, GPTBot for training, ChatGPT-User for
     user fetches): https://developers.openai.com/api/docs/bots
   - **[secondary]** Anthropic (ClaudeBot training, Claude-User user fetches, Claude-SearchBot search
     indexing): https://www.searchenginejournal.com/anthropics-claude-bots-make-robots-txt-decisions-more-granular/568253/
   - This is absence of evidence, not proof.
3. **Agent fetch tools strip `<head>`.**
   - **[verified, n=1]** Claude Code's WebFetch on https://developer.parseur.com/getting-started, a
     page whose HTML has `<meta name="keywords" ...>`: the model saw only converted body text and
     no meta tags. Many agent fetch tools convert HTML to Markdown the same way **[inference]**;
     I only tested this one.
4. **ReadMe's agent-facing outputs drop keywords.**
   - **[verified]** `https://docs.sensible.so/docs/draft-jsonlogic.md` (page has
     `keywords: [custom computation]`) has frontmatter with only `updatedAt` and `agentTools`. No
     keywords.
   - **[verified]** `https://docs.sensible.so/llms.txt` lists each page with its excerpt/description,
     no keywords.
   - **[verified]** The rendered HTML has no `<meta name="keywords">` (hidden page; recheck on a
     public page).
5. **GEO research doesn't support keyword tactics.**
   - **[secondary]** Princeton GEO study (~10k queries): adding citations, quotes, statistics raised
     generative-engine visibility up to ~40%; keyword stuffing (in content) had no significant
     effect. https://www.seerinteractive.com/insights/optimizing-content-for-generative-search-engines
   - **[secondary]** 2026 citation study (arXiv 2604.25707; ChatGPT, AI Overviews/Gemini, Perplexity):
     cited pages are longer, modular, semantically aligned, and contain definitions, numbers,
     comparisons, procedures. https://arxiv.org/html/2604.25707v2
   - No study found that tests the meta keywords tag specifically.
6. **Unknown:** whether training crawlers (GPTBot, ClaudeBot) keep `<head>` content when
   building training data. Even if they do, there's no mechanism by which a keywords tag would make
   a page more likely to be cited **[inference]**.

## Conclusion

No evidence that any search engine or AI agent uses the keywords tag to rank, retrieve, or cite
pages; strong structural reasons they never see it (Google ignores it; agent fetchers and ReadMe's
`.md`/`llms.txt` drop it). What they *do* read: title, meta description (= our `excerpt` via
`metadata.description`), body text, and `llms.txt` descriptions. Synonyms belong there.
