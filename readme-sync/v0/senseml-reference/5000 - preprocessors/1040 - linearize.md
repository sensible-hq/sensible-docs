---
title: "draft Linearize"
hidden: true
---



DRAFT

**Note:** This is advanced. for most use cases, see Multicolumn. TODO look up other wordings

Use this preprocessor for documents containing columns of text that the Multicolumn (TODO LINK) preprocessor can't recognize. 

Ensures that Sensible [sort lines](doc:lines#line-sorting) into the specified, coordinate-based blocks,  rather than the default behavior of sorting lines left to right across the page.

[**Parameters**](doc:linearize#parameters)
[**Examples**](doc:linearize#examples)
[**Notes**](doc:linearize#notes)

Parameters
====

| key                    | value                                                        | description                                                  |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| type (**required**)    | `linearize`                                                  | *Recognizes multi-column layouts in documents and sorts lines into blocks in whatever or you specify.* |
| match<br/>or<br/>range | [Match](doc:match) object or array of Match objects<br/>or<br/>Range object | Specifies the matching pages or page portions ("ranges") on which to run this preprocessor.<br/>`match`: TODO HOW TO FORMAT?<br/>or<br/>`range`:<br/> See following table |
| blocks                 | array of objects                                             | TODO: blocks specify BLAH BLAH. Each rectangular block object in the array has the following parameters: TODO which required? To visually determine the following coordinates, click a point in the document in the Sensible app, then drag to display inch dimensions.<br/>`minX`: default: 0 <br/>Specifies the left boundary of the block, in inches from the left edge of the page. <br/>`maxX`: default: 0<br/>Specifies the right boundary of the block, in inches from the left edge of the page. <br/> `minY`: default: page's width in inches<br/>Specifies the top boundary of the block, in inches from the top edge of the page.<br/>`maxY`: default: page's height in inches<br/>Specifies the bottom boundary of the block, in inches from the top edge of the page. |

### LINEARIZE Horizontal Section Range parameters



TODO: figure this out and define it better!!  WITH A NICE PICTURE?



Horizontal sections: repeating stacked blocks of text in a defined range, *which can be discontinous/interrupted by other igored text???*

Vertical sections: columns of text containing repeated text in a defined range, *which doesn't itself repeat and which can't be discontinious??*.

RANGE contains repeating sections (blocks)



See the following table for details about the Range object parameters:

| key                   | value                                              | description for horizontal sections                          | description for vertical sections                            |
| --------------------- | -------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| anchor (**required**) | [Anchor](anchor) object, or array of Match objects | Contains the following parameters:<br/><br/> **start**: Ignores anything in the document before this line. if undefined, Sensible starts the search for the Match parameter at the beginning of the document<br/><br/>**match** (**required**): <br/>&nbsp;&nbsp;&nbsp; Specifies both the start of the range and the repeated starting line of each section. For example, in the preceding image, specify `"Claim number"`. Each section starts at the top boundary of this starting line, and excludes text to the right of the line. If sections lack an easy-to-match line, use the Require Stop and Offset Y parameters to start each section above or below the line matched by this parameter. <br/>&nbsp;&nbsp; **end**: Ignores any anchor matches in the document after this line. For example, to extract solely September claims in the preceding image, specify `"October"`. | TODO REWORD: Same behavior as for horizontal sections, with the following exception:<br/>The Match parameter specifies the start of the range only, rather than the start of both the section group and the section. By default, Sensible recognizes columns as sections automatically. For more information, see [Section nuances](doc:section-nuances#vertical-sections).<br/> |
| direction             | `horizontal`, `vertical`. default: `horizontal`    | This parameter table describes horizonal sections. See the following table for information about vertical sections. | If set to `vertical`, Sensible searches for columns in a sections group. <br/>In detail, Sensible searches  left-to-right for columns in the first-found document area defined by the Range parameter, rather than the default behavior of continuing to search for matches for the Range parameter. For an illustration of this behavior, see [section nuances](doc:section-nuances). |
| externalRange         | object                                             | (Advanced) Enables anchoring on text that's external to the section group range in the sections' field anchors.  For example, use the external range with the [Intersection](doc:intersection) method when sections lack internal anchoring candidates.<br/>The external range defines a vertical range anywhere in the document. You can configure the external range to be static, or to repeat relative to each section.<br/>Contains the following parameters:<br/><br/>`anchor`  (**required**):  An [Anchor](https://docs.sensible.so/docs/anchor) object. The external range starts at the top boundary of this starting line, and the range's scope includes text to the left of this line. If the start of the range lacks an easy-to-match line, you can use the Offset Y parameter to start the range above or below the line matched by this parameter. <br/><br/>`anchorIsAbsolute`: (default: false).  If false, Sensible creates dynamic external ranges, each relative to a section start. For example, configure dynamic external ranges if you want to anchor each section's fields on variably positioned page headings. For more information, see [Dynamic external range example](doc:sections-example-external-range#example-dynamic). Sensible starts searching for dynamic external ranges in the lines succeeding the start of each section. To search for dynamic external ranges that precede each section, use  `"reverse":"true"`  on the external range's anchor. <br/>If the Anchor Is Absolute option is set to true, Sensible creates one static external range in the document, searching from the start of the document. For an example of a static dynamic range, see [Static external range example](doc:sections-example-external-range#example-static).<br/><br/>`stop`: (Match object) (**required**) A Match object defining the end of the external range. Sensible defines the Stop horizontal line by finding the top boundary of the stop line, then applies a default offset of 0.08" down the page.<br/><br/>`offsetY`: Specifies the number of inches to offset the range's top boundary from the anchor's Match parameter.<br/><br/>`stopOffsetY`: Specifies the number of inches to offset from the Stop parameter.<br/> | n/a, not supported for vertical sections.                    |
| stop                  | [Anchor](anchor) object, or array of Match objects | Specifies the repeated end of the section after its anchor. For example, if you specify `"Date of claim"`, then each section stops at a horizontal line below the bottom boundary of the stop line "Date of claim" (plus any offset you specify).<br/>Sensible defines the Stop horizontal line by finding the top boundary of the stop line if found, or the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively.<br/>If you don't specify this parameter, each section stops at the top boundary of the next section's starting line (plus any offset). In this case, the last section in the group continues to the end of the document. |                                                              |
| requireStop           | Boolean. default: false                            | If true, the Stop parameter is required, and the section ends when it matches the Stop parameter, instead of the default behavior of ending at the next starting line specified in the anchor's Match parameter.<br/>**Note:**  Configure this parameter for horizontal sections when the starting line repeats in the section, to avoid ending the section before it completes. You don't need to configure this parameter if multiple starting line matches lie on one *horizontal* line in the section. In such a case, Sensible ignores any zero-height sections generated by this horizontal line's matches. For more information, see [Multiple anchors in section](doc:section-nuances#multiple-anchors-in-section). |                                                              |
| offsetY               | number in inches                                   | Specifies an offset from the anchor Match parameter.  Positive values offset down the page, negative values offset up the page. <br/><br/>Specifies the number of inches to offset the section's top boundary from the anchor Match parameter. By default a section starts at the top boundary of the matched line. If you specify Offset Y, the section starts at that top boundary plus the offset. For example, configure this when the section lacks an easy-to-match first line. |                                                              |
| stopOffsetY           | number in inches                                   | Specifies the number of inches to offset from the Stop parameter. <br/><br/>In detail, offsets each section's stop from the Stop horizontal line. |                                                              |
| tolerance             | number in inches. default: 0.08                    | Configure this for your Stop parameter if the stop line and its immediately preceding and succeeding lines are an unusual font size.<br/> For example, if your font size is a tiny 1.44 pt (0.02 inches), set this parameter to 0.01.<br>In detail, Sensible by default defines the Stop horizontal line by finding the top boundary of the stop line if found, or the top boundary of the next section's starting line, then applies a default offset of 0.08" down or up the page, respectively. This parameter configures the default offset.<br/> |                                                              |
| ignoredColumns        | integer array.                                     | n/a, not supported                                           | Removes unwanted columns from both the output *and* from the SenseML search scope. For example, this is useful if the columns contain text that interferes with anchoring on other columns. |



### Range parameters for columns

Use `"direction":"vertical"` in the Range object to define a "vertical" sections group, where each section is a column-like layout. For example, use vertical sections to extract tables nested in tables, tables with row labels, or other complex text layouts. 

The following table shows Range parameters specific to vertical sections.

| key                   | value                                                        | description                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| anchor (**required**) | [Anchor](anchor) object, or array of Match objects           | TODO REWORD: Same behavior as for horizontal sections, with the following exception:<br/>The Match parameter specifies the start of the  section group only, rather than the start of both the section group and the section. By default, Sensible recognizes columns as sections automatically. For more information, see [Section nuances](doc:section-nuances#vertical-sections).<br/> |
| direction             | `horizontal`, `vertical`. default: `horizontal`              | If set to `vertical`, Sensible searches for columns in a sections group. <br/>In detail, Sensible searches  left-to-right for columns in the first-found document area defined by the Range parameter, rather than the default behavior of continuing to search for matches for the Range parameter. For an illustration of this behavior, see [section nuances](doc:section-nuances). |
| externalRange         | n/a                                                          | n/a, not supported for vertical sections.                    |
| stop                  | TODO                                                         | Specifies the end of the section *group*, and ignores lines that span multiple columns. If not specified, Sensible ends the section group at the first line that spans multiple columns. If the spanning lines occur mid-column, you can also configure the Line Filters parameter.<br/>For more information, see [Section nuances](doc:section-nuances#vertical-sections). |
| requireStop           | n/a                                                          | N/A, not supported for vertical sections.                    |
| offsetY               | number in inches                                             | Specifies the number of inches to offset the section *group's* top boundary from the anchor Match parameter. For example, configure this when when you want to exclude non-columnar text from a vertical section. |
| stopOffsetY           | number in inches                                             | Specifies the number of inches to offset from the Stop parameter. <br/>In detail, offsets the section *group's* stop from the Stop horizontal line. |
| tolerance             |                                                              | TODO: not sure if this actually applies?                     |
|                       | **Column-specific parameters**                               |                                                              |
| columnSelection       | array of index selections where each "index selection" can be:<br/>- a column index or comma-delimited indices<br/><br/>- an array with two comma-delimited indices, meaning all the columns in the indices range<br/><br/> default: capture all columns (`[]`) | Use to configure which columns to treat as sections. Sensible adds *unselected* columns to each section, for example so they can be used as anchor candidates. For an illustration, see [Section nuances](doc:section-nuances#column-selection).<br/> `[[0,5]]` selects 1st through 6th columns as sections. Sensible adds the lines from any other columns to each section. <br/>`[1,3,-1]`  selects 2nd, 4th, and the last columns. Use negative indices to offset from the last column. <br/> `[1,[3,7]]` selects the 2nd column and the 4th through 8th columns.<br/>  `[[0, -2]]` selects 1st through 2nd-to-last columns.<br/><br/> |
| ignoredColumns        | integer array.                                               | Removes unwanted columns from both the output *and* from the SenseML search scope. For example, this is useful if the columns contain text that interferes with anchoring on other columns. |
| minColumnGap          | number in inches. default: 0                                 | Configures column recognition by specifying the smallest allowed width of the gutters separating the columns. For an example, see [Table grid example](doc:sections-example-table-grid). Use when text in a column contains whitespace gaps such that Sensible can split one column into two. To avoid this split, set a minimum gap that's larger than the gaps inside the column. The default (0) means that zero-width vertical lines define the column boundaries. |
| lineFilters           | Match object, or array of Match objects                      | Use to ignore lines that span columns and break column recognition. For example, if the lines occur mid-column, use this parameter rather than a Stop parameter to exclude the lines. Sensible excludes the lines both from the output and from the SenseML search scope.<br/>You don't need to configure this parameter if you specify a Stop parameter. For more information, see [Section nuances](doc:section-nuances#vertical-sections). |



Examples
====

The following example shows TBD.

**Config**

```json
{
  "preprocessors": [
    {
      /* if columns are present, sort lines by columns */
      "type": "multicolumn"
    },
    {
      /*  OCR all pages containing 5 or fewer lines of text. 
          This ensures that Sensible OCRs page 2, which contains 
          images of text and charts */
      "type": "ocr",
      "pageLinesLimit": 5
    }
  ],
  "fields": [
    {
      /* extract the introduction as a page range
        between the headings "introduction" and "methodology".
        Without the Multicolumn preprocessor, the Document Range method
        would incorrectly extract a top portion of the first page.*/
      "id": "introduction",
      "anchor": {
        "match": {
          "pattern": "introduction$",
          "type": "regex",
          "flags": "i"
        }
      },
      "method": {
        "id": "documentRange",
        "includeAnchor": true,
        "stop": {
          "pattern": "(?:\\d+\\.\\s*)?(methodology||related work)",
          "type": "regex",
          "flags": "i",
          "minimumHeight": 0.16
        }
      }
    },
    {
      "method": {
        /* extracts the methodology text using an LLM prompt.
          Since this is an excerpted paper, the LLM
          accurately reports
          that the answer is incomplete. */
        "id": "queryGroup",
        /* to find context, segment the document by its outline and summarize each segment */
        "searchBySummarization": "outline",
        "queries": [
          {
            "id": "methodology",
            "type": "string",
            "description": "What is the complete methodology?"
          }
        ]
      }
    },
    {
      /* chain prompts by asking an LLM to answer questions about the
         extracted methodology field */
      "method": {
        "id": "queryGroup",
        /* use the  */
        "source_ids": [
          /* restrict queries to data in methodology field */
          "methodology"
        ],
        "queries": [
          {
            "id": "data_set_size",
            "type": "number",
            "description": "What is the size of the data set?"
          },
          {
            "id": "data_set_type",
            "description": "Is the data set real or simulated? Answer 'real' or 'simulated'"
          }
        ]
      }
    },
    {
      "anchor": {
        "match": {
          "type": "includes",
          "text": "Proportions of fraudulent"
        }
      },
      "method": {
        "id": "queryGroup",
        /* use a multimodal LLM to extract visual/non-text information from 
        a pie chart */
        "multimodalEngine": {
          "region": {
            "start": "above",
            "width": 2,
            "height": 3,
            "offsetX": -1,
            "offsetY": -2.5
          }
        },
        "queries": [
          {
            "id": "cash_out_pie_chart",
            "type": "string",
            "description": "in the pie chart, approximately what proportion of fraudulent transactions by type are cash_out?"
          },
          {
            "id": "transfer_pie_chart",
            "type": "string",
            "description": "in the pie chart, approximately what proportion of fraudulent transactions by type are transfer?"
          }
        ]
      }
    }
  ]
}

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/multicolumn.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/multicolumn.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "introduction": {
    "type": "string",
    "value": "1 INTRODUCTION Credit cards make up an annual $100 Billion global market. As credit cards become more and more popular in the digital age, they also come with their inherent risks. Credit card fraud is the act of a fraudulent credit card transaction in order for criminals to acquire money or goods and services not belonging to them. Criminals committing credit card fraud are rarely apprehended and therefore, automatic credit card fraud detection can be of great significance. The task of automation credit card fraud classification is not easy, since the data-sets for credit card transactions are severely imbalanced. An imbalanced data-set is one where the proportion of one class is significantly higher than the rest of the classes. Classification tasks on imbalanced data-sets are difficult since it tends to be possible to gain a high level of accuracy despite misclassifying most of the data points from the minority class. A plausible way of attempting to classify on an imbalanced data-set is to apply class weights such that each data point from the minority class is given more importance and each data point from the majority class is given less importance. This study will attempt to see how class weights can help tackle the task of credit card fraud classification. This will be done by comparing Binary Logistic Regression model and Random Forest Classifier model without weights to those with class weights. This study will aim to find if a weighted classification will be able to improve upon the unweighted classification of credit card fraud detection. 2 METHODOLOGY 2.1 Data Credit Card transactions data tend to contain confidential information and therefore, they are scarcely available to the public. Hence, the data-set for this study is one created from a simulator, PaySim, that simulates credit card transactions. The simulator utilizes a private data-set to generate a simulated data-set that mimics ordinary credit card transactions along with fraudulent activity. The data-set contains 3,223,223 synthetic transactions. Table 1. Fields of the Data-set Field Data Type Description type of transaction STRING type amount of the transaction DOUBLE amount account balance before the transaction oldbalanceOrg DOUBLE account balance after the transaction newbalanceOrig DOUBLE account balance of recipient before the transaction. oldbalanceDest DOUBLE account balance of recipient after the transaction. newbalanceDest DOUBLE if the transaction is fraudulent or not isFraud Binary Table 2. Frequency and average amount of Valid and Fraudulent Transactions Number of Transactions Category Average Amount Valid $ 156,675.40 3,220,396 Fraudulent 2,827 $ 1,309,250.00 TRANSFER CASH IN TRANSFER CASH_OUT DEBIT PAYMENT CASH_OUT (b) Proportions of fraudulent (a) Proportions of transaction by type transaction by type Fig. 1. Breakdown of proportion of all and fraudulent transactions by type 2.1.1 Exploratory Data Analysis. From table 2 we can see the imbalanced nature of data-set and how on average fraudulent transactions amount is more than 8 times the amount of valid transactions. Figure 1 also demonstrates that how fraudulent transactions are only of type ʼTRANSFERʼ and ʼCASH OUTʼ. Finally, Figure 2 illustrates how the distribution of fraudulent transactions tend to have amount higher than those of valid transactions. 2.2 Pre-processing The data needs to be pre-processed because it contains categorical variables and Machine Learning algorithms use quantitative variables to discriminate between classes. The categorical variable in this data-set that will be used is type. The first transformation applied to the field type is the StringIndexer. The StringIndexer maps the string variable to indices belonging to the set 0, . . . , 𝑛𝑢𝑚𝑏𝑒𝑟𝑂 𝑓 𝑈 𝑛𝑖𝑞𝑢𝑒𝑉 𝑎𝑙𝑢𝑒𝑠 - 1. The order of the index assignment is ordered by frequency of that value in the data-set. Furthermore, the string-indexed variable is now transformed into a one-hot vector using the OneHotEncoder. This creates a vector of length 𝑛 - 1 (where 𝑛 is the number of unique categorical values) where all values are 0.0 except for at the index location which has a value of 1.0. Finally, all the feature variables are placed into one vector which represents the features for the respective transaction. Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. © 2021 Association for Computing Machinery. Manuscript submitted to ACM"
  },
  "methodology": {
    "value": "2 METHODOLOGY\n2.1 Data\nCredit Card transactions\ndata tend to contain\nconfidential information\nand therefore, they are\nscarcely available to the\npublic. Hence, the data-set\nfor this study is one created\nfrom a simulator, PaySim,\nthat simulates credit card\ntransactions. The simulator\nutilizes a private data-set to\ngenerate a simulated\ndata-set that mimics\nordinary credit card\ntransactions along with\nfraudulent activity. The\ndata-set contains\n3,223,223 synthetic\ntransactions.\n\n2.1.1 Exploratory Data Analysis.\nFrom table 2 we can see the imbalanced\nnature of data-set and how on average\nfraudulent transactions amount is more than\n8 times the amount of valid transactions.\nFigure 1 also demonstrates that how\nfraudulent transactions are only of type\nʼTRANSFERʼ and ʼCASH OUTʼ. Finally, Figure\n2 illustrates how the distribution of fraudulent\ntransactions tend to have amount higher than\nthose of valid transactions. 2.2\n\nPre-processing The data needs to be\npre-processed because it contains\ncategorical variables and Machine Learning\nalgorithms use quantitative variables to\ndiscriminate between classes. The\ncategorical variable in this data-set that will\nbe used is type. The first transformation\napplied to the field type is the StringIndexer.\nThe StringIndexer maps the string variable to\nindices belonging to the set 0, . . . , 𝑛𝑢𝑚𝑏𝑒𝑟𝑂\n𝑓 𝑈 𝑛𝑖𝑞𝑢𝑒𝑉 𝑎𝑙𝑢𝑒𝑠 - 1. The order of the index\nassignment is ordered by frequency of that\nvalue in the data-set. Furthermore, the\nstring-indexed variable is now transformed\ninto a one-hot vector using the\nOneHotEncoder. This creates a vector of\nlength 𝑛 - 1 (where 𝑛 is the number of unique\ncategorical values) where all values are 0.0\nexcept for at the index location which has a\nvalue of 1.0. Finally, all the feature variables\nare placed into one vector which represents\nthe features for the respective transaction.",
    "type": "string",
    "confidenceSignal": "answer_may_be_incomplete"
  },
  "data_set_size": {
    "source": "3,223,223",
    "value": 3223223,
    "type": "number",
    "confidenceSignal": "not_supported"
  },
  "data_set_type": {
    "value": "simulated",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "cash_out_pie_chart": {
    "value": "50%",
    "type": "string",
    "confidenceSignal": "not_supported"
  },
  "transfer_pie_chart": {
    "value": "50%",
    "type": "string",
    "confidenceSignal": "not_supported"
  }
}
```
