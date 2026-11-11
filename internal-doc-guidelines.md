## Internal docs authoring notes



### Publishing the docs to readme

To publish the markdown docs in this repository to ReadMe.io at https://docs.sensible.so/docs, commit to v0. This triggers GitHub Actions that perform actions conditionally, such as checking links, and styling images. Readme takes care of the bidirecitonal sync. (Ignore suggestions to create pull requests from v0 into main from GH desktop client).



### Image directory conventions
In the Images dir: 
- Save all screenshots to /screenshots
- If you edit the screenshot with callouts/arrows/etc and you're worried it might be difficult to replicate the original, then you can save an unedited version of the image to /source
- the doc build process automatically applies styling such as drop shadows to images in screenshots/ and saves to final/




### Authoring requirements & limitations

You can author the docs in GitHub-flavored Markdown, with the following minor restrictions and caveats:

- **links** - The preferred linking method is to use Readme's syntax like this: `[some title](doc:some-doc-slug)`. or `[Some title](ref:some-api-endpoint-slug)`. (Not recommended: you can also use relative links, but  then you have to leave out the .md extension. Like this: `[syntax for relative link to a doc](./readme-sync/v0/some-file-name-no-textension)`. (Future improvement: should be easy to modify readme-sync code to strip out .md extensions if we want working relative links in the markdown stored in github)

- **images** - You can't use relative links,  `[like this syntax](./images/some-image)`. We'll use hyperlinks instead to images stored on GitHub like this: `![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/<path>/some_image.png)` . 




- **no authoring the API ref in dash.readme** -  to keep edits centralized and OpenAPI compliant, edit the openapi spec files in GitHub.













