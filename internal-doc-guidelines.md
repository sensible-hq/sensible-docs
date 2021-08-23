## Internal docs authoring notes



### Publishing the docs to readme

To publish the markdown docs in this repository to ReadMe.io at https://docs.sensible.so/docs:

1. Install  https://github.com/flowcommerce/readme-sync. this is an open source tool that uses the ReadMe API. 
2.  Install [ImageMagick](https://imagemagick.org/). We use this to apply drop shadows to new images (rather than customizing the CSS in ReadMe).
3. In your local clone of the readme-sync repo, install `direnv` and specify a README_API_KEY to your `.envrc`. To get the apiKey for ReadMe , navigate in the dash of  docs project to the Configuration pane.
4.  Run `make_docs.sh`.



### Directory and filename requirements

See https://github.com/flowcommerce/readme-sync. 



### Authoring requirements & limitations

You can author the docs in Github-flavored Markdown, with the following minor restrictions and caveats:

- **links** - The preferred linking method is to use Readme's syntax like this: `[some title](doc:some-doc-slug)`. or `[Some title](ref:some-api-endpoint-slug)`. (Not recommended: you can also use relative links, but  then you have to leave out the .md extension. Like this: `[syntax for relative link to a doc](./readme-sync/v0/some-file-name-no-textension)`. (Future improvement: should be easy to modify readme-sync code to strip out .md extensions if we want working relative links in the markdown stored in github)

- **images** - You can't use relative links  `[like this syntax](./images/some-image)`. We'll use hyperlinks instead to images stored on the master branch like this: `![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/some_image.png)` . 

- **be careful with heading markup** ReadMe gets confused if you use a code block snippet that indicates the language IN CONJUNCTION with headings that use hashtags (#). In this instance it erratically interprets #code comments as heading markdown syntax. 

  So avoid headings like this:

  `# Heading 1`

  and only use this syntax:

```
Heading 1
_____
```



- **no authoring in dash.readme** - the bottom line is: edit in Github or use readme's Suggested Edits mechanism! don't make direct edits in dash.readme

  - Why?  If someone doesn't know better, they could edit the docs in dash.readme... but those edits will be overwritten the next time someone runs the readme-sync. There's no mechanism in dash.readme to warn them not to edit.  Likewise, any suggested edits in ReadMe need to be manually merged to the Github docs rather than merged using ReadMe's mechanism. 

  



### Future improvements



- **automatic build** -  Let's use Travis or similar tool to automate calling the readme-sync tool so that on committ, the github markdown syncs to ReadMe.

  









