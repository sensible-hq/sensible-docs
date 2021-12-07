---
title: "Document generation introduction"
hidden: true
---

 You can programmatically fill in templated forms with structured data using Sensible. If you create a PDF or HTML template and add unique identifier to fillable elements, like this: 

![image-20211207095306851](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20211207095306851.png)

Then you can use Sensible's generation API to feed in data to the fillable elements and return a completed document, like this:

```json
{
    mappings: [
        {
  birthday_customer: "customer.birthdate",
  first_name_customer: "customer.first.name",
  last_name_customer: "customer.last.name"  
  full_name_customer: [
    "customer.name",
    {
      method: "concat",
      sources: ["customer_first_name", "customer_last_name"],
    },
}
  ],

describe("mapper", () => {
  it("simple mapping", () => {
    expect(
      mapper(config1, { customer: { id: 520, name: "John Doe" } })
    ).toEqual({
      CustomerId: 520,
      CustomerName: "John Doe",
    });
  });
  it("alternatives", () => {
    expect(
      mapper(config1, {
        customer: { id: 520 },
        customerFirstName: "John",
        customerLastName: "Doe",
        addresses: [{ street: "221B Baker Street", city: "London" }],
      })
    ).toEqual({
      CustomerId: 520,
      CustomerName: "John Doe",
      address: "221B Baker Street",
    });



}
```





