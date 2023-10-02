---
title: "SDK introduction"
hidden: true
---

This topic gives an overview and links to the Sensible Typescript SDK.



This reference guide describes how to use the Sensible Typescript SDK.

### Version

For the current version number of this SDK, see SDK compatibility matric

### Quickstart

To get up and running quickly, see the Quickstart

### Reference

For reference docs, see the left-hand navigation, or start off with Install SDK TODO link

### Source files

- Typescript SDK repo
- changelog in repo



```
declare class Sensible {`
`  constructor(apikey: string);``  extract(`
`    options: ({ url: string } | { file: Blob }) &`
`      (`
`        | { documentType: string; configurationName?: string }` 
`        | { documentTypes: string[] }`
`      ) & {`
`        webhook?: Webhook;`
`      }`
`  ): Promise<ExtractionResult>;``  
```

```
classify(options: { file: Blob }): Promise<ClassificationResult>;`
`}``type Webhook = {`
`  url: string;`
`  payload?:`
`    | Record<string, unknown>`
`    | string`
`    | number`
`    | boolean`
`    | Array<unknown>;`
`};
```

