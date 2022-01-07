---
title: "Pick values"
hidden: true

---

Extract values from a group of fields. For example, extract the selected boxes from a checkbox group, or extract all "yes" answers from a group of fields with a yes/no/maybe dropdowns.

Parameters
====

The following parameters are in the computed field's [global Method](doc:computed-field-methods#parameters) parameter: 

| key                       | value                                    | description                                                  |
| :------------------------ | :--------------------------------------- | :----------------------------------------------------------- |
| id (**required**)         | `pickValues`                             |                                                              |
| source_ids (**required**) | array of field ids in the current config | The id of the fields from which to pick. Returns those fields whose value matches that specified in the Value parameter. |
| match                     | `one`, `all`                             | Specifies to return either the first source field with the value specified in the Value parameter, or all fields with the matching value. TODO: verify enums, verify in Types.ts, and add to index.md (also...add screenshots?) https://sensiblehq.slack.com/archives/C0215T9K86P/p1641413717020300 |
| value                     | null, boolean, string, or string array   | The value to pick. Sensible converts checkbox and radio button selection marks to true and false. For example, to pick selected checkboxes, specify `true`. As another example, to return dropdown questions set to "maybe" in a list of fields, specify `"maybe"`. |

It will be “one” and “all” (may need to update the configs)

![img](https://ca.slack-edge.com/T017UPRAE94-U01U55EFU86-5a71df1991bd-48)

**[Frances Elliott](https://app.slack.com/team/U01U55EFU86)**[1 minute ago](https://sensiblehq.slack.com/archives/C0215T9K86P/p1641417897022300?thread_ts=1641413717.020300&cid=C0215T9K86P)

thanks. What's the meaning of 'one' then? ("first" i understood to be 'return the 1st field found in the group with the specified value)

![img](https://ca.slack-edge.com/T017UPRAE94-U0181MWQ8BV-0140373d7470-48)

**[Josh Lewis](https://app.slack.com/team/U0181MWQ8BV)**[1 minute ago](https://sensiblehq.slack.com/archives/C0215T9K86P/p1641417900022500?thread_ts=1641413717.020300&cid=C0215T9K86P)

For the values — `null` would give you back the list of source IDs that are null, like in the case where we aren’t able to find a checkbox or other field

![img](https://ca.slack-edge.com/T017UPRAE94-U0181MWQ8BV-0140373d7470-48)

**[Josh Lewis](https://app.slack.com/team/U0181MWQ8BV)**[< 1 minute ago](https://sensiblehq.slack.com/archives/C0215T9K86P/p1641417913022700?thread_ts=1641413717.020300&cid=C0215T9K86P)

One means one and only one

![img](https://ca.slack-edge.com/T017UPRAE94-U0181MWQ8BV-0140373d7470-48)

**[Josh Lewis](https://app.slack.com/team/U0181MWQ8BV)**[< 1 minute ago](https://sensiblehq.slack.com/archives/C0215T9K86P/p1641417934022900?thread_ts=1641413717.020300&cid=C0215T9K86P)

So for a radio button-style use case where we only expect one item to be checked (think corporate entity type)

![:+1::skin-tone-2:](https://a.slack-edge.com/production-standard-emoji-assets/13.0/google-small/1f44d-1f3fb.png)**1**

![img](https://ca.slack-edge.com/T017UPRAE94-U0181MWQ8BV-0140373d7470-48)

**[Josh Lewis](https://app.slack.com/team/U0181MWQ8BV)**[< 1 minute ago](https://sensiblehq.slack.com/archives/C0215T9K86P/p1641417943023200?thread_ts=1641413717.020300&cid=C0215T9K86P)

It returns null if none are check or more than one is checked



The following example shows TBD

**Config**

```json

```



**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/pick_values.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/pick_values.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json

```

