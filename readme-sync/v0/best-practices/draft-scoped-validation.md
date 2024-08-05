---
title: scoped validation draft
hidden: true
---

| id                           | value                              | notes                                                        |
| ---------------------------- | ---------------------------------- | ------------------------------------------------------------ |
| *description (**required**)* | *string*                           | *A description of the test*                                  |
| *severity (**required**)*    | *`error`, `warning`, `skipped`*    | *The severity of the failing test.*                          |
| scope                        | array of section or subsection IDs | To create a validation for a field contained in [sections](doc:sections), specify the field's parent section ID in this parameter. For example, `["section_1"]`. <br/>To validate a field in nested sections, specify the scope in descending order. For example, to validate a `field_a` in a  `child_section_2`  that has parent `parent_section_1`, specify  `["parent_section_1", "child_section_2"]`  in this parameter. Sensible applies the validation to each instance of `field_a` in each instance of `child_section_2`.<br/>For an example, see  Validations 6. |

## Validations 6

The following example shows how to validate a field in sections.

- **Description**:  engine spec exists.
- **Severity**: warning
- **Condition**: `{"exists":[{"var":"engine"}]}`
- **Scope** `["car_models","trim_specs"]` 

**Config**

The following example uses the config from  [Table grid example](doc:sections-example-table-grid). 

**Example document**

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/vertical_section_table_grid_fail_scoped_validations.pdf) |
| ---------------- | ------------------------------------------------------------ |



**Validation output**

The output for this example returns nulls for the `engine` field for the `SV trim` and the `EX trim`:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/validation_scoped_1.png)

 The two nulls trigger two validation warnings. The validation reports the indexes of the null output:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/validation_scoped.png)

 For example, in the first failed validation, the `"car_models",0... "trim_specs, 1"`  indices indicate null output for the `engine` field in the `car_model[0]`   (Nissan) section's  `trim_spec[1]` (SV trim) subsection.  The second instance, `"car_models", 1..."trim_specs", 0` indicates a null `engine` output for the `EX trim` subsection.



