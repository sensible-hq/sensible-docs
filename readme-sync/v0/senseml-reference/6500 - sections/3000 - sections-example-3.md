---
title: "Sections"
hidden: true

---




----

Vertical sections: sections and columns
----

To give a broad overview using vertical sections for columns:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_col_sect.png)





In the preceding image, to capture both the Sections and their Columns, 1 define a section then 2.  define a nested vertical section.  Using abbreviated YML notation to give a brief idea of the more complex SenseML JSON: 

```yml
sections:
  - id: parentSections
    range:
      anchor: Section
    fields:
      - id: sectionTitle
        anchor: Section
        method:
          id: passthrough
   sections:
     - id: nestedColumns
       range:
         direction: vertical
         anchor: column
       fields:
         - id: columnTitle
           anchor: column
           method:
             id: passthrough    
      
```

With this approach, you can output something like the following, using abbreviated YML notation to give a brief idea of the more complex JSON API response:

```yml
parentSections:
  - sectionTitle: Section 1
    nestedColumns:
      columnTitle: Column A
      columnTitle: Column B
      columnTitle: Column C
 - sectionTitle: Section 2
    nestedColumns:
      columnTitle: Column A
      columnTitle: Column B
      columnTitle: Column C  
   
```

Vertical sections: table grid
-----

To give a broad overview of using vertical sections for a grid of tables with repeated format:

```json
sections:
  - id: carModel
    range:
      anchor: Section
    fields:
      - id: sectionTitle
        anchor: Section
        method:
          id: passthrough
   sections:
     - id: nestedColumns
       range:
         direction: vertical
         anchor: column
       fields:
         - id: columnTitle
           anchor: column
           method:
             id: passthrough    
```



Notes
===

To better understand vertical sections, see sectio
