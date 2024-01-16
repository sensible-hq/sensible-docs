---
title: "draft replace"
hidden: true
---

`{"replace":[source_field_value, regex_destination, regex_to_search_for "regexFlags in comma-delimited list(?)"]}`, where `regex` is a Javascript-flavored regular expression.<br/>Double escape special characters, since the regex is in a JSON object (for example, `\\s`, not `\s` , to represent a whitespace character). This operation supports regular expression flags such as `i` for case insensitive. <br>