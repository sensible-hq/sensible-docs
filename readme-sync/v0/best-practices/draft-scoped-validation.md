---
title: scoped validation draft
hidden: true
---

| id                         | value                                      | notes                                                        |
| -------------------------- | ------------------------------------------ | ------------------------------------------------------------ |
| description (**required**) | string                                     | A description of the test                                    |
| severity (**required**)    | `error`, `warning`, `skipped`              | The severity of the failing test.                            |
| scope                      | array of nested section and subsection IDs | Specify the section(s) where this validation should be applied |

Example

- **Description**:  engine spec exists.
- **Severity**: warning
- **Condition**: `{"exists":[{"var":"engine"}]}`
- **Scope** `["car_models","trim_specs"]`



The following example uses the config from  sections-example-table-grid with an example where the Engine spec is missing:





vertical_section_table_grid_fail_scoped_validations







