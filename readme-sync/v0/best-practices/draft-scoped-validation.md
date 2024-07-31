---
title: scoped validation draft
hidden: true
---

| id                         | value                         | notes                                                        |
| -------------------------- | ----------------------------- | ------------------------------------------------------------ |
| description (**required**) | string                        | A description of the test                                    |
| severity (**required**)    | `error`, `warning`, `skipped` | The severity of the failing test.                            |
| scope                      | a section or subsection ID    | Specify the section(s) where this validation should be applied. Applies the validation to each field in the specified section or subsection. To specify a subsection, use array syntax. For example, to validate a field in a  `childSection2` , specify its parent or parents as an array, for example,  `["parentSection1", "childSection2"]` |

Example

- **Description**:  engine spec exists.
- **Severity**: warning
- **Condition**: `{"exists":[{"var":"engine"}]}`
- **Scope** `["car_models","trim_specs"]` 



The following example uses the config from  [Table grid example](doc:sections-example-table-grid) with an example where the Engine spec is missing from the following example document:

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_section_table_grid_fail_scoped_validations.pdf) |
| ---------------- | ------------------------------------------------------------ |

The output for this example returns nulls for the engine specs for the `SV trim` and the `EX trim`:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/validation_scoped_1.png)

The validation reports these nulls using indices. For example, in the first instance of the failed validation, `"car_models",0` indicates the `2016 Nissan Altima` section and `"trim_specs", 1` indicates a null engine spec for the SV trim. The second instance, `"car_models", 1..."trim_specs", 0` indicates a null engine spec for the EX trim.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/validation_scoped.png)

