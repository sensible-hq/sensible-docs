---
title: "Sections"
hidden: true

---




----

Vertical sections: sections and columns
----

To give a broad overview using vertical sections for columns, the following image shows capturing numbered sections and their columns with these steps:

1 define a section

2. define a nested vertical section 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/vertical_sections_col_sect.png)



The following config uses abbreviated YML notation to give an overview of the more complex SenseML JSON: 

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

With this approach, you can output something like the following, using abbreviated YML notation to give an overview of the more complex JSON API response:

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

Example details
----
The following elaborates on the preceding brief overview using JSON instead of YML

