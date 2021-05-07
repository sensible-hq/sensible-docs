## Internal docs authoring notes



### Publishing the docs to readme

To publish the markdown docs in this repository to ReadMe, use https://github.com/flowcommerce/readme-sync. this is an open source tool that uses the ReadMe API. Follow the instructions in that tool to install it locally.

Then to publish using a local installation of the readme-sync tool:

1. Make sure the docs in your clone of this repository are up to date. 
2. In your local clone of the readme-sync repo, run something like the following command:

npx ts-node sync/index.ts --apiKey REDACTED --version v0 --docs ~/Github/sensible-docs/readme-sync/v0

To get the apiKey for ReadMe , navigate in the dash of  docs project to the Configuration pane.

### Directory and filename requirements

See https://github.com/flowcommerce/readme-sync. 



### Authoring requirements & limitations

You can author the docs in Github-flavored Markdown, with the following minor restrictions and caveats:

- **links** - You can use relative links, but you have to leave out the .md extension. Like this: [syntax for relative link to a doc](./readme-sync/v0/some-file-name-no-textension). (Future improvement: should be easy to modify readme-sync code to strip out .md extensions if we want working relative links in the markdown stored in github)
- **images** - You can't use relative links  [like this syntax](./images/some-image). We'll use hyperlinks instead to images stored on the master branch. 
- **no semantic code snippets / language highlighting** ReadMe gets confused if you use a code block snippet that indicates the language. It erratically interprets #code comments as heading markdown syntax. So if you have a bunch of headings, then avoid:

```python
# some python code here
```

and only use:

```
# some code in some unspecified language here  
```

- **no authoring in dash.readme** - the bottom line is: edit in Github or use readme's Suggested Edits mechanism! don't make direct edits in dash.readme

  - Why?  If someone doesn't know better, they could edit the docs in dash.readme... but those edits will be overwritten the next time someone runs the readme-sync. There's no mechanism in dash.readme to warn them not to edit.  Likewise, any suggested edits in ReadMe need to be manually merged to the Github docs rather than merged using ReadMe's mechanism. 

  



### Future improvements



- **automatic build** -  Let's use Travis or similar tool to automate calling the readme-sync tool so that on committ, the github markdown syncs to ReadMe.

  









