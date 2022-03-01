---
title: Extraction v0.0.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="extraction">Extraction v0.0.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

Extract structured data from documents with the Sensible API.

Base URLs:

* <a href="https://api.sensible.so/v0">https://api.sensible.so/v0</a>

License: <a href="https://www.TBD.org/licenses/LICENSE-2.0.html">Sensible API</a>

# Authentication

- HTTP Authentication, scheme: bearer Sensible uses API keys to authenticate requests. You should have received a key as a part of onboarding, 
but if you're having trouble with your current key, please reach out to support@sensible.so. 
Keep your API keys secure and do not share them publicly accessible areas such as GitHub, client-side code, etc.
Authentication to the API is performed via Bearer Authentication. Provide your API key as the bearer auth value.

<h1 id="extraction-document">Document</h1>

## extract-data-from-a-document

<a id="opIdextract-data-from-a-document"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.sensible.so/v0/extract/{type} \
  -H 'Content-Type: application/pdf' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer {access-token}'

```

```http
POST https://api.sensible.so/v0/extract/{type} HTTP/1.1
Host: api.sensible.so
Content-Type: application/pdf
Accept: application/json

```

```javascript
const inputBody = 'string';
const headers = {
  'Content-Type':'application/pdf',
  'Accept':'application/json',
  'Authorization':'Bearer {access-token}'
};

fetch('https://api.sensible.so/v0/extract/{type}',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Content-Type' => 'application/pdf',
  'Accept' => 'application/json',
  'Authorization' => 'Bearer {access-token}'
}

result = RestClient.post 'https://api.sensible.so/v0/extract/{type}',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Content-Type': 'application/pdf',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('https://api.sensible.so/v0/extract/{type}', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Content-Type' => 'application/pdf',
    'Accept' => 'application/json',
    'Authorization' => 'Bearer {access-token}',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('POST','https://api.sensible.so/v0/extract/{type}', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.sensible.so/v0/extract/{type}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Content-Type": []string{"application/pdf"},
        "Accept": []string{"application/json"},
        "Authorization": []string{"Bearer {access-token}"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("POST", "https://api.sensible.so/v0/extract/{type}", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`POST /extract/{type}`

*Extract data from a document*

Extract data from a local document synchronously. 
For a step-by-step tutorial on calling this endpoint, 
see [Try synchronous extraction](doc:api-tutorial-sync).

There are two options for posting the document bytes.
  1. (often preferred) specify the non-encoded document bytes as the entire request body, 
  and specify the content-type as one of "application/pdf", "image/jpeg", or "image/png", as appropriate.
  2. Base64 encode the document bytes, specify them in a body "document" field, and specify application/json for the content type. 

> Body parameter

<h3 id="extract-data-from-a-document-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|type|path|string|true|The type of document to extract from. |
|environment|query|string|false|If you specify `development`, extracts preferentially using config versions |
|body|body|string(binary)|true|There are two options for posting the document bytes. 1. (often preferred) specify the non-encoded document bytes as the entire request body, and specify the content-type as one of "application/pdf", "image/jpeg", or "image/png", as appropriate. 2. Base64 encode the document bytes, specify them in a body "document" field, and specify application/json for the content type.|

#### Detailed descriptions

**type**: The type of document to extract from. 
Create the type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`). 
As a convenience, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type. 
For example, if you create an `auto_insurance_quotes` type, you can add `carrier 1`, `carrier 2`, and 
`carrier 3` configs to the type in the Sensible app so that you can extract data from all these carriers using the same 
`type`, without specifying the carrier in the API request.

**environment**: If you specify `development`, extracts preferentially using config versions 
published to the development environment in the Sensible app. The extraction runs all configs in the doc type before 
picking the best fit. For each config, falls back to production version if no development version of the config exists.

#### Enumerated Values

|Parameter|Value|
|---|---|
|environment|production|
|environment|development|

> Example responses

> 200 Response

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "configuration": "anyco_rate_confirmation",
  "status": "COMPLETE",
  "parsed_document": {
    "weight": {
      "source": "0.0lbs",
      "value": 0,
      "unit": "pounds",
      "type": "weight"
    },
    "distance": {
      "source": "193mi",
      "value": 193,
      "unit": "miles",
      "type": "distance"
    },
    "load_number": {
      "type": "string",
      "value": "Wk91242"
    },
    "carrier_email": null,
    "price": {
      "source": "$695.00",
      "value": 695,
      "unit": "$",
      "type": "currency"
    },
    "pickup_date": null
  },
  "validations": [
    {
      "description": "load weight should be over 1 ton",
      "severity": "warning"
    },
    {
      "description": "carrier email must be in format string@string",
      "severity": "skipped",
      "message": "Missing prerequisites - carrier_email"
    }
  ],
  "validations_summary": {
    "fields": 6,
    "fields_present": 4,
    "errors": 0,
    "warnings": 1,
    "skipped": 1
  },
  "classification_summary": [
    {
      "configuration": "anyco_rate_confirmation",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 3,
        "fields_present": 4,
        "penalities": 0.5
      }
    },
    {
      "configuration": "acme_co",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 0,
        "fields_present": 2,
        "penalities": 1.5
      }
    }
  ]
}
```

> 400 Response

```
"Either a specific set of messages about fields in the request, or error messages like the following examples -\nNot available to logged in users\nTo use the asynchronous flow you must have persistence enabled\nSpecified document type does not exist\nSpecified document type ${named type} does not exist\nNo published configurations found for environment ${environment}\nSpecified golden does not exist\nSpecified configuration/version does not exist\nSpecified configuration/version is not valid\nMust provide the Content-Type header when request body is present\nContent-Type must be application/json\nMissing request body or body.document\nCould not determine the content type of the document\nCould not determine the content type of the document. Please check that the document was correctly encoded as Base64\nThis PDF is invalid. If you submitted this PDF using Base64 encoding, please check that the encoding is correct\nThis PDF is password protected. Please resubmit with password protection disabled\nThis PDF is empty\nThis PDF exceeds the maximum dimensions for OCR of 17 x 17 inches\nThis PDF exceeds the maximum size for OCR of 50MB\nNo fingerprints match for this PDF and fingerprint_mode is set to strict\nContent type of ${found} does not match declared type of ${expected}\nDocument is not present\n"
```

<h3 id="extract-data-from-a-document-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|the structured data extracted from the document and metadata|[Extraction](#schemaextraction)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|string|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Not authorized|string|
|415|[Unsupported Media Type](https://tools.ietf.org/html/rfc7231#section-6.5.13)|Unsupported Media Type|string|
|429|[Too Many Requests](https://tools.ietf.org/html/rfc6585#section-4)|Too Many Requests|string|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|string|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
bearerAuth
</aside>

## generate-an-upload-url

<a id="opIdgenerate-an-upload-url"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.sensible.so/v0/generate_upload_url/{type} \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer {access-token}'

```

```http
POST https://api.sensible.so/v0/generate_upload_url/{type} HTTP/1.1
Host: api.sensible.so
Content-Type: application/json
Accept: application/json

```

```javascript
const inputBody = '{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "content_type": "application/pdf"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json',
  'Authorization':'Bearer {access-token}'
};

fetch('https://api.sensible.so/v0/generate_upload_url/{type}',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Content-Type' => 'application/json',
  'Accept' => 'application/json',
  'Authorization' => 'Bearer {access-token}'
}

result = RestClient.post 'https://api.sensible.so/v0/generate_upload_url/{type}',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('https://api.sensible.so/v0/generate_upload_url/{type}', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Content-Type' => 'application/json',
    'Accept' => 'application/json',
    'Authorization' => 'Bearer {access-token}',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('POST','https://api.sensible.so/v0/generate_upload_url/{type}', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.sensible.so/v0/generate_upload_url/{type}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Content-Type": []string{"application/json"},
        "Accept": []string{"application/json"},
        "Authorization": []string{"Bearer {access-token}"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("POST", "https://api.sensible.so/v0/generate_upload_url/{type}", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`POST /generate_upload_url/{type}`

*Extract doc at a Sensible URL*

Extract data asynchronously from a document with the following steps. You must use this or other asynchronous endpoints for documents that are over 4.5MB in size or require over 30 seconds to process. 
  1. Use this endpoint to generate a Sensible URL.
  2. PUT the document you want to extract data from at the URL, where `SENSIBLE_UPLOAD_URL` is the URL you received 
from this endpoint's response.
For example, `curl -T ./sample.pdf "SENSIBLE_UPLOAD_URL"`. 
Note: the pre-signed upload_url does not support Base64 encoded documents. You PUT the document bytes directly to the endpoint, 
and you must match the "Content-Type" header to that specified in the POST that creates the URL. If you omit the parameter, you
must omit the header, and if you specify the parameter, you must include the exact header in the PUT.
  3.  To retrieve the extraction or poll its status, use the extraction `id` returned in the response to call the 
GET documents/{id} endpoint.

For a step-by-step tutorial on calling this endpoint, see 
[Try asynchronous extraction from a Sensible URL](https://docs.sensible.so/docs/api-tutorial-async-2).

> Body parameter

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "content_type": "application/pdf"
}
```

<h3 id="generate-an-upload-url-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|type|path|string|true|The type of document to extract from. |
|environment|query|string|false|If you specify `development`, extracts preferentially using config versions |
|body|body|[GenerateUrlRequest](#schemagenerateurlrequest)|false|none|

#### Detailed descriptions

**type**: The type of document to extract from. 
Create the type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`). 
As a convenience, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type. 
For example, if you create an `auto_insurance_quotes` type, you can add `carrier 1`, `carrier 2`, and 
`carrier 3` configs to the type in the Sensible app so that you can extract data from all these carriers using the same 
`type`, without specifying the carrier in the API request.

**environment**: If you specify `development`, extracts preferentially using config versions 
published to the development environment in the Sensible app. The extraction runs all configs in the doc type before 
picking the best fit. For each config, falls back to production version if no development version of the config exists.

#### Enumerated Values

|Parameter|Value|
|---|---|
|environment|production|
|environment|development|

> Example responses

> 200 Response

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "status": "COMPLETE",
  "upload_url": "https://sensible-so-utility-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=REDACTED&Expires=1623861476&Signature=REDACTED&x-amz-security-token=REDACTED"
}
```

> 400 Response

```
"Either a specific set of messages about fields in the request, or error messages like the following examples -\nNot available to logged in users\nTo use the asynchronous flow you must have persistence enabled\nSpecified document type does not exist\nSpecified document type ${named type} does not exist\nNo published configurations found for environment ${environment}\nSpecified golden does not exist\nSpecified configuration/version does not exist\nSpecified configuration/version is not valid\nMust provide the Content-Type header when request body is present\nContent-Type must be application/json\nMissing request body or body.document\nCould not determine the content type of the document\nCould not determine the content type of the document. Please check that the document was correctly encoded as Base64\nThis PDF is invalid. If you submitted this PDF using Base64 encoding, please check that the encoding is correct\nThis PDF is password protected. Please resubmit with password protection disabled\nThis PDF is empty\nThis PDF exceeds the maximum dimensions for OCR of 17 x 17 inches\nThis PDF exceeds the maximum size for OCR of 50MB\nNo fingerprints match for this PDF and fingerprint_mode is set to strict\nContent type of ${found} does not match declared type of ${expected}\nDocument is not present\n"
```

<h3 id="generate-an-upload-url-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|returns the upload_url at which to PUT the document for extraction|[AsyncUploadResponse](#schemaasyncuploadresponse)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|string|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Not authorized|string|
|415|[Unsupported Media Type](https://tools.ietf.org/html/rfc7231#section-6.5.13)|Unsupported Media Type|string|
|429|[Too Many Requests](https://tools.ietf.org/html/rfc6585#section-4)|Too Many Requests|string|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|string|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
bearerAuth
</aside>

## provide-a-download-url

<a id="opIdprovide-a-download-url"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.sensible.so/v0/extract_from_url/{type} \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer {access-token}'

```

```http
POST https://api.sensible.so/v0/extract_from_url/{type} HTTP/1.1
Host: api.sensible.so
Content-Type: application/json
Accept: application/json

```

```javascript
const inputBody = '{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "document_url": "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
  "content_type": "application/pdf"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json',
  'Authorization':'Bearer {access-token}'
};

fetch('https://api.sensible.so/v0/extract_from_url/{type}',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Content-Type' => 'application/json',
  'Accept' => 'application/json',
  'Authorization' => 'Bearer {access-token}'
}

result = RestClient.post 'https://api.sensible.so/v0/extract_from_url/{type}',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('https://api.sensible.so/v0/extract_from_url/{type}', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Content-Type' => 'application/json',
    'Accept' => 'application/json',
    'Authorization' => 'Bearer {access-token}',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('POST','https://api.sensible.so/v0/extract_from_url/{type}', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.sensible.so/v0/extract_from_url/{type}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Content-Type": []string{"application/json"},
        "Accept": []string{"application/json"},
        "Authorization": []string{"Bearer {access-token}"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("POST", "https://api.sensible.so/v0/extract_from_url/{type}", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`POST /extract_from_url/{type}`

*Extract doc at your URL*

Extract data asynchronously from a document at the specified `document_url`.<br/> 
You must use this or other asynchronous endpoints for documents that are over 4.5MB in size or require over 30 seconds to process.
Take the following steps. 
1. Run this endpoint.
2. To retrieve the extraction or poll its status, use the extraction `id` returned in the response to call the GET documents/{id} endpoint.
For a step-by-step tutorial on calling this endpoint, 
see [Try asynchronous extraction from your URL](doc:api-tutorial-async-1).

> Body parameter

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "document_url": "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
  "content_type": "application/pdf"
}
```

<h3 id="provide-a-download-url-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|type|path|string|true|The type of document to extract from. |
|environment|query|string|false|If you specify `development`, extracts preferentially using config versions |
|body|body|[ExtractFromUrlRequest](#schemaextractfromurlrequest)|false|none|

#### Detailed descriptions

**type**: The type of document to extract from. 
Create the type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`). 
As a convenience, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type. 
For example, if you create an `auto_insurance_quotes` type, you can add `carrier 1`, `carrier 2`, and 
`carrier 3` configs to the type in the Sensible app so that you can extract data from all these carriers using the same 
`type`, without specifying the carrier in the API request.

**environment**: If you specify `development`, extracts preferentially using config versions 
published to the development environment in the Sensible app. The extraction runs all configs in the doc type before 
picking the best fit. For each config, falls back to production version if no development version of the config exists.

#### Enumerated Values

|Parameter|Value|
|---|---|
|environment|production|
|environment|development|

> Example responses

> 200 Response

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "status": "COMPLETE"
}
```

> 400 Response

```
"Either a specific set of messages about fields in the request, or error messages like the following examples -\nNot available to logged in users\nTo use the asynchronous flow you must have persistence enabled\nSpecified document type does not exist\nSpecified document type ${named type} does not exist\nNo published configurations found for environment ${environment}\nSpecified golden does not exist\nSpecified configuration/version does not exist\nSpecified configuration/version is not valid\nMust provide the Content-Type header when request body is present\nContent-Type must be application/json\nMissing request body or body.document\nCould not determine the content type of the document\nCould not determine the content type of the document. Please check that the document was correctly encoded as Base64\nThis PDF is invalid. If you submitted this PDF using Base64 encoding, please check that the encoding is correct\nThis PDF is password protected. Please resubmit with password protection disabled\nThis PDF is empty\nThis PDF exceeds the maximum dimensions for OCR of 17 x 17 inches\nThis PDF exceeds the maximum size for OCR of 50MB\nNo fingerprints match for this PDF and fingerprint_mode is set to strict\nContent type of ${found} does not match declared type of ${expected}\nDocument is not present\n"
```

<h3 id="provide-a-download-url-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|returns the ID to use to retrieve the extraction|[AsyncResponse](#schemaasyncresponse)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|string|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Not authorized|string|
|415|[Unsupported Media Type](https://tools.ietf.org/html/rfc7231#section-6.5.13)|Unsupported Media Type|string|
|429|[Too Many Requests](https://tools.ietf.org/html/rfc6585#section-4)|Too Many Requests|string|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|string|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
bearerAuth
</aside>

## retrieving-results

<a id="opIdretrieving-results"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.sensible.so/v0/documents/{id} \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer {access-token}'

```

```http
POST https://api.sensible.so/v0/documents/{id} HTTP/1.1
Host: api.sensible.so
Content-Type: application/json
Accept: application/json

```

```javascript
const inputBody = '{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "document_url": "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
  "content_type": "application/pdf"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json',
  'Authorization':'Bearer {access-token}'
};

fetch('https://api.sensible.so/v0/documents/{id}',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Content-Type' => 'application/json',
  'Accept' => 'application/json',
  'Authorization' => 'Bearer {access-token}'
}

result = RestClient.post 'https://api.sensible.so/v0/documents/{id}',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('https://api.sensible.so/v0/documents/{id}', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Content-Type' => 'application/json',
    'Accept' => 'application/json',
    'Authorization' => 'Bearer {access-token}',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('POST','https://api.sensible.so/v0/documents/{id}', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.sensible.so/v0/documents/{id}");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Content-Type": []string{"application/json"},
        "Accept": []string{"application/json"},
        "Authorization": []string{"Bearer {access-token}"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("POST", "https://api.sensible.so/v0/documents/{id}", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`POST /documents/{id}`

*Retrieve extraction*

Use this endpoint in conjunction with asynchronous extraction requests to retrieve your results. 
You can also use this endpoint to retrieve the results for documents extractions from the synchronous /extract endpoint.
To poll extraction status, check the `status` field in this endpoint's response. 
When the extraction completes, the returned status is `COMPLETE` and the response includes results in the 
`parsed_document` field.  For fields in the extraction for which Sensible couldn't find a value, Sensible returns null.

> Body parameter

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "document_url": "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
  "content_type": "application/pdf"
}
```

<h3 id="retrieving-results-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|[ExtractionId](#schemaextractionid)|true|unique ID for the extraction, used to retreive the extraction|
|environment|query|string|false|If you specify `development`, extracts preferentially using config versions |
|body|body|[ExtractFromUrlRequest](#schemaextractfromurlrequest)|false|none|

#### Detailed descriptions

**environment**: If you specify `development`, extracts preferentially using config versions 
published to the development environment in the Sensible app. The extraction runs all configs in the doc type before 
picking the best fit. For each config, falls back to production version if no development version of the config exists.

#### Enumerated Values

|Parameter|Value|
|---|---|
|environment|production|
|environment|development|

> Example responses

> 200 Response

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "configuration": "anyco_rate_confirmation",
  "status": "COMPLETE",
  "parsed_document": {
    "weight": {
      "source": "0.0lbs",
      "value": 0,
      "unit": "pounds",
      "type": "weight"
    },
    "distance": {
      "source": "193mi",
      "value": 193,
      "unit": "miles",
      "type": "distance"
    },
    "load_number": {
      "type": "string",
      "value": "Wk91242"
    },
    "carrier_email": null,
    "price": {
      "source": "$695.00",
      "value": 695,
      "unit": "$",
      "type": "currency"
    },
    "pickup_date": null
  },
  "validations": [
    {
      "description": "load weight should be over 1 ton",
      "severity": "warning"
    },
    {
      "description": "carrier email must be in format string@string",
      "severity": "skipped",
      "message": "Missing prerequisites - carrier_email"
    }
  ],
  "validations_summary": {
    "fields": 6,
    "fields_present": 4,
    "errors": 0,
    "warnings": 1,
    "skipped": 1
  },
  "classification_summary": [
    {
      "configuration": "anyco_rate_confirmation",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 3,
        "fields_present": 4,
        "penalities": 0.5
      }
    },
    {
      "configuration": "acme_co",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 0,
        "fields_present": 2,
        "penalities": 1.5
      }
    }
  ],
  "download_url": "https://sensible-so-document-type-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/246a6f60-0e5b-11eb-b720-295a6fba723e.pdf?AWSAccessKeyId=REDACTED"
}
```

> 400 Response

```
"Either a specific set of messages about fields in the request, or error messages like the following examples -\nNot available to logged in users\nTo use the asynchronous flow you must have persistence enabled\nSpecified document type does not exist\nSpecified document type ${named type} does not exist\nNo published configurations found for environment ${environment}\nSpecified golden does not exist\nSpecified configuration/version does not exist\nSpecified configuration/version is not valid\nMust provide the Content-Type header when request body is present\nContent-Type must be application/json\nMissing request body or body.document\nCould not determine the content type of the document\nCould not determine the content type of the document. Please check that the document was correctly encoded as Base64\nThis PDF is invalid. If you submitted this PDF using Base64 encoding, please check that the encoding is correct\nThis PDF is password protected. Please resubmit with password protection disabled\nThis PDF is empty\nThis PDF exceeds the maximum dimensions for OCR of 17 x 17 inches\nThis PDF exceeds the maximum size for OCR of 50MB\nNo fingerprints match for this PDF and fingerprint_mode is set to strict\nContent type of ${found} does not match declared type of ${expected}\nDocument is not present\n"
```

<h3 id="retrieving-results-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|returns the extraction|[ExtractionAsyncResult](#schemaextractionasyncresult)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|string|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Not authorized|string|
|415|[Unsupported Media Type](https://tools.ietf.org/html/rfc7231#section-6.5.13)|Unsupported Media Type|string|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|string|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
bearerAuth
</aside>

<h1 id="extraction-portfolio">Portfolio</h1>

## generate-an-upload-url-for-a-pdf-portfolio

<a id="opIdgenerate-an-upload-url-for-a-pdf-portfolio"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.sensible.so/v0/generate_upload_url \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer {access-token}'

```

```http
POST https://api.sensible.so/v0/generate_upload_url HTTP/1.1
Host: api.sensible.so
Content-Type: application/json
Accept: application/json

```

```javascript
const inputBody = '{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "types": [
    "tax_returns",
    "bank_statements",
    "credit_reports"
  ]
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json',
  'Authorization':'Bearer {access-token}'
};

fetch('https://api.sensible.so/v0/generate_upload_url',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Content-Type' => 'application/json',
  'Accept' => 'application/json',
  'Authorization' => 'Bearer {access-token}'
}

result = RestClient.post 'https://api.sensible.so/v0/generate_upload_url',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('https://api.sensible.so/v0/generate_upload_url', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Content-Type' => 'application/json',
    'Accept' => 'application/json',
    'Authorization' => 'Bearer {access-token}',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('POST','https://api.sensible.so/v0/generate_upload_url', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.sensible.so/v0/generate_upload_url");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Content-Type": []string{"application/json"},
        "Accept": []string{"application/json"},
        "Authorization": []string{"Bearer {access-token}"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("POST", "https://api.sensible.so/v0/generate_upload_url", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`POST /generate_upload_url`

*Extract portfolio at a Sensible URL*

Use this endpoint with multiple documents that are packaged into one PDF file (a PDF "portfolio"). 
Segments a PDF at the specified `document_url` into the specified document types (for example, 1099, w2, and bank_statement) 
and then runs extractions asynchronously for each document Sensible finds in the PDF portfolio. Take the following steps.
1. Run this endpoint.
2. To retrieve the extraction results or poll status, use the extraction `id` returned in the response to call 
the GET documents/{id} endpoint.
For more about extracting from PDF portfolios, see [Extracting from document portfolios](doc:portfolio).

> Body parameter

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "types": [
    "tax_returns",
    "bank_statements",
    "credit_reports"
  ]
}
```

<h3 id="generate-an-upload-url-for-a-pdf-portfolio-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|environment|query|string|false|If you specify `development`, extracts preferentially using config versions |
|body|body|[PortfolioRequest](#schemaportfoliorequest)|false|none|

#### Detailed descriptions

**environment**: If you specify `development`, extracts preferentially using config versions 
published to the development environment in the Sensible app. The extraction runs all configs in the doc type before 
picking the best fit. For each config, falls back to production version if no development version of the config exists.

#### Enumerated Values

|Parameter|Value|
|---|---|
|environment|production|
|environment|development|

> Example responses

> 200 Response

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "status": "COMPLETE",
  "upload_url": "https://sensible-so-utility-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=REDACTED&Expires=1623861476&Signature=REDACTED&x-amz-security-token=REDACTED"
}
```

> 400 Response

```
"Either a specific set of messages about fields in the request, or error messages like the following examples -\nNot available to logged in users\nTo use the asynchronous flow you must have persistence enabled\nSpecified document type does not exist\nSpecified document type ${named type} does not exist\nNo published configurations found for environment ${environment}\nSpecified golden does not exist\nSpecified configuration/version does not exist\nSpecified configuration/version is not valid\nMust provide the Content-Type header when request body is present\nContent-Type must be application/json\nMissing request body or body.document\nCould not determine the content type of the document\nCould not determine the content type of the document. Please check that the document was correctly encoded as Base64\nThis PDF is invalid. If you submitted this PDF using Base64 encoding, please check that the encoding is correct\nThis PDF is password protected. Please resubmit with password protection disabled\nThis PDF is empty\nThis PDF exceeds the maximum dimensions for OCR of 17 x 17 inches\nThis PDF exceeds the maximum size for OCR of 50MB\nNo fingerprints match for this PDF and fingerprint_mode is set to strict\nContent type of ${found} does not match declared type of ${expected}\nDocument is not present\n"
```

<h3 id="generate-an-upload-url-for-a-pdf-portfolio-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|returns the upload_url at which to PUT the document for extraction|[AsyncUploadResponse](#schemaasyncuploadresponse)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|string|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Not authorized|string|
|415|[Unsupported Media Type](https://tools.ietf.org/html/rfc7231#section-6.5.13)|Unsupported Media Type|string|
|429|[Too Many Requests](https://tools.ietf.org/html/rfc6585#section-4)|Too Many Requests|string|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|string|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
bearerAuth
</aside>

## provide-a-download-url-for-a-pdf-portfolio

<a id="opIdprovide-a-download-url-for-a-pdf-portfolio"></a>

> Code samples

```shell
# You can also use wget
curl -X POST https://api.sensible.so/v0/extract_from_url \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer {access-token}'

```

```http
POST https://api.sensible.so/v0/extract_from_url HTTP/1.1
Host: api.sensible.so
Content-Type: application/json
Accept: application/json

```

```javascript
const inputBody = '{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "document_url": "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
  "content_type": "application/pdf"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json',
  'Authorization':'Bearer {access-token}'
};

fetch('https://api.sensible.so/v0/extract_from_url',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```ruby
require 'rest-client'
require 'json'

headers = {
  'Content-Type' => 'application/json',
  'Accept' => 'application/json',
  'Authorization' => 'Bearer {access-token}'
}

result = RestClient.post 'https://api.sensible.so/v0/extract_from_url',
  params: {
  }, headers: headers

p JSON.parse(result)

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('https://api.sensible.so/v0/extract_from_url', headers = headers)

print(r.json())

```

```php
<?php

require 'vendor/autoload.php';

$headers = array(
    'Content-Type' => 'application/json',
    'Accept' => 'application/json',
    'Authorization' => 'Bearer {access-token}',
);

$client = new \GuzzleHttp\Client();

// Define array of request body.
$request_body = array();

try {
    $response = $client->request('POST','https://api.sensible.so/v0/extract_from_url', array(
        'headers' => $headers,
        'json' => $request_body,
       )
    );
    print_r($response->getBody()->getContents());
 }
 catch (\GuzzleHttp\Exception\BadResponseException $e) {
    // handle exception or api errors.
    print_r($e->getMessage());
 }

 // ...

```

```java
URL obj = new URL("https://api.sensible.so/v0/extract_from_url");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Content-Type": []string{"application/json"},
        "Accept": []string{"application/json"},
        "Authorization": []string{"Bearer {access-token}"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("POST", "https://api.sensible.so/v0/extract_from_url", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

`POST /extract_from_url`

*Extract portfolio at your URL*

Use this endpoint with multiple documents that are packaged into one PDF file (a PDF "portfolio").
Segments a PDF into the specified document types (for example, 1099, w2, and bank_statement) and then runs extractions 
asynchronously for each document Sensible finds in the PDF portfolio.  Take the following steps -  
1. Use this endpoint to generate a Sensible URL.
2. PUT the PDF you want to extract data from at the URL, where `SENSIBLE_UPLOAD_URL` is the URL you received 
from this endpoint's response. For example, `curl -T ./sample.pdf "SENSIBLE_UPLOAD_URL"`
Note - the pre-signed upload_url does not support Base64 encoded PDFs. 
You PUT the PDF bytes directly to the endpoint and must omit the content-type header.  
3. To retrieve the extraction or poll its status, use the extraction `id` returned in 
the response to call the GET documents/{id} endpoint.
For more about extracting from PDF portfolios, see [Extracting from document portfolios](doc:portfolio).

> Body parameter

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "document_url": "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
  "content_type": "application/pdf"
}
```

<h3 id="provide-a-download-url-for-a-pdf-portfolio-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|environment|query|string|false|If you specify `development`, extracts preferentially using config versions |
|body|body|[ExtractFromUrlRequest](#schemaextractfromurlrequest)|false|none|

#### Detailed descriptions

**environment**: If you specify `development`, extracts preferentially using config versions 
published to the development environment in the Sensible app. The extraction runs all configs in the doc type before 
picking the best fit. For each config, falls back to production version if no development version of the config exists.

#### Enumerated Values

|Parameter|Value|
|---|---|
|environment|production|
|environment|development|

> Example responses

> 200 Response

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "status": "COMPLETE"
}
```

> 400 Response

```
"Either a specific set of messages about fields in the request, or error messages like the following examples -\nNot available to logged in users\nTo use the asynchronous flow you must have persistence enabled\nSpecified document type does not exist\nSpecified document type ${named type} does not exist\nNo published configurations found for environment ${environment}\nSpecified golden does not exist\nSpecified configuration/version does not exist\nSpecified configuration/version is not valid\nMust provide the Content-Type header when request body is present\nContent-Type must be application/json\nMissing request body or body.document\nCould not determine the content type of the document\nCould not determine the content type of the document. Please check that the document was correctly encoded as Base64\nThis PDF is invalid. If you submitted this PDF using Base64 encoding, please check that the encoding is correct\nThis PDF is password protected. Please resubmit with password protection disabled\nThis PDF is empty\nThis PDF exceeds the maximum dimensions for OCR of 17 x 17 inches\nThis PDF exceeds the maximum size for OCR of 50MB\nNo fingerprints match for this PDF and fingerprint_mode is set to strict\nContent type of ${found} does not match declared type of ${expected}\nDocument is not present\n"
```

<h3 id="provide-a-download-url-for-a-pdf-portfolio-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|returns the ID to use to retrieve the extraction|[AsyncResponse](#schemaasyncresponse)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|string|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Not authorized|string|
|415|[Unsupported Media Type](https://tools.ietf.org/html/rfc7231#section-6.5.13)|Unsupported Media Type|string|
|429|[Too Many Requests](https://tools.ietf.org/html/rfc6585#section-4)|Too Many Requests|string|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|string|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
bearerAuth
</aside>

# Schemas

<h2 id="tocS_Classification">Classification</h2>
<!-- backwards compatibility -->
<a id="schemaclassification"></a>
<a id="schema_Classification"></a>
<a id="tocSclassification"></a>
<a id="tocsclassification"></a>

```json
{
  "configuration": "anyco",
  "fingerprint_present": 1,
  "fingerprints": 1,
  "score": {
    "value": 17,
    "fields_present": 17,
    "penalties": 1.5
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|configuration|string|false|none|the config tested|
|fingerprint_present|integer|false|none|number of this config's fingerprints that Sensible found in the document|
|fingerprints|integer|false|none|number of fingerprints defined in this config|
|score|[Score](#schemascore)|false|none|The score for the extraction, used to help choose the best extraction.|

<h2 id="tocS_ClassificationSummary">ClassificationSummary</h2>
<!-- backwards compatibility -->
<a id="schemaclassificationsummary"></a>
<a id="schema_ClassificationSummary"></a>
<a id="tocSclassificationsummary"></a>
<a id="tocsclassificationsummary"></a>

```json
[
  {
    "configuration": "anyco_rate_confirmation",
    "fingerprints": 2,
    "fingerprints_present": 2,
    "score": {
      "value": 3,
      "fields_present": 4,
      "penalities": 0.5
    }
  },
  {
    "configuration": "acme_co",
    "fingerprints": 2,
    "fingerprints_present": 2,
    "score": {
      "value": 0,
      "fields_present": 2,
      "penalities": 1.5
    }
  }
]

```

Metadata about how Sensible chose the config to use for this extraction.
Sensible compares all configs in the document type, then chooses the best extraction using
fingerprints, scores, or a combination of the two. 
(When two extractions tie by score and fingerprints, Sensible chooses the 
first configuration in alphabetic order).
For more details, see [fingerprints](https://docs.sensible.so/docs/fingerprint#notes)

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Classification](#schemaclassification)]|false|none|Metadata about how Sensible chose the config to use for this extraction.<br>Sensible compares all configs in the document type, then chooses the best extraction using<br>fingerprints, scores, or a combination of the two. <br>(When two extractions tie by score and fingerprints, Sensible chooses the <br>first configuration in alphabetic order).<br>For more details, see [fingerprints](https://docs.sensible.so/docs/fingerprint#notes)|

<h2 id="tocS_Score">Score</h2>
<!-- backwards compatibility -->
<a id="schemascore"></a>
<a id="schema_Score"></a>
<a id="tocSscore"></a>
<a id="tocsscore"></a>

```json
{
  "value": 17,
  "fields_present": 17,
  "penalties": 1.5
}

```

The score for the extraction, used to help choose the best extraction.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|value|integer|false|none|the score total is fields_present minus penalty points. In the absence of fingerprints, Sensible returns the extraction in the document type with the highest score.|
|fields_present|integer|false|none|number of non-null fields Sensible extracted from the document using this config|
|penalties|number|false|none|errors are 1 penality point and warnings are 0.5 points. See the validations_summary for a breakdown.|

<h2 id="tocS_ParsedDocument">ParsedDocument</h2>
<!-- backwards compatibility -->
<a id="schemaparseddocument"></a>
<a id="schema_ParsedDocument"></a>
<a id="tocSparseddocument"></a>
<a id="tocsparseddocument"></a>

```json
{
  "weight": {
    "source": "0.0lbs",
    "value": 0,
    "unit": "pounds",
    "type": "weight"
  },
  "distance": {
    "source": "193mi",
    "value": 193,
    "unit": "miles",
    "type": "distance"
  },
  "load_number": {
    "type": "string",
    "value": "Wk91242"
  },
  "carrier_email": null,
  "price": {
    "source": "$695.00",
    "value": 695,
    "unit": "$",
    "type": "currency"
  },
  "pickup_date": null
}

```

data extracted from the document, structured as an array of fields

### Properties

*None*

<h2 id="tocS_Validation">Validation</h2>
<!-- backwards compatibility -->
<a id="schemavalidation"></a>
<a id="schema_Validation"></a>
<a id="tocSvalidation"></a>
<a id="tocsvalidation"></a>

```json
{
  "description": "Dollar amount should be more than $100",
  "severity": "warning",
  "message": "Missing prerequisites: broker.email"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|description|string|false|none|Description of the validation|
|severity|string|false|none|Severity of the failing validation (error, warning, skipped)|
|message|string|false|none|Messages about why the validation failed|

#### Enumerated Values

|Property|Value|
|---|---|
|severity|error|
|severity|warning|
|severity|skipped|

<h2 id="tocS_Validations">Validations</h2>
<!-- backwards compatibility -->
<a id="schemavalidations"></a>
<a id="schema_Validations"></a>
<a id="tocSvalidations"></a>
<a id="tocsvalidations"></a>

```json
[
  {
    "description": "load weight should be over 1 ton",
    "severity": "warning"
  },
  {
    "description": "carrier email must be in format string@string",
    "severity": "skipped",
    "message": "Missing prerequisites - carrier_email"
  }
]

```

which extracted fields failed validation rules you write in the Sensible app.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Validation](#schemavalidation)]|false|none|which extracted fields failed validation rules you write in the Sensible app.|

<h2 id="tocS_ValidationsSummary">ValidationsSummary</h2>
<!-- backwards compatibility -->
<a id="schemavalidationssummary"></a>
<a id="schema_ValidationsSummary"></a>
<a id="tocSvalidationssummary"></a>
<a id="tocsvalidationssummary"></a>

```json
{
  "fields": 6,
  "fields_present": 4,
  "errors": 0,
  "warnings": 1,
  "skipped": 1
}

```

Summary of the extracted fields that failed validation rules you write in the Sensible app.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|fields|integer|false|none|the numbers of fields specified in the config to extract from the document|
|fields_present|integer|false|none|the actual number of non-null fields extracted from the document|
|errors|number|false|none|the number of errors in the extraction|
|warnings|number|false|none|the number of warnings in the extraction|
|skipped|number|false|none|the number of fields skipped in the extraction because a prerequisite field was null|

<h2 id="tocS_PortfolioRequest">PortfolioRequest</h2>
<!-- backwards compatibility -->
<a id="schemaportfoliorequest"></a>
<a id="schema_PortfolioRequest"></a>
<a id="tocSportfoliorequest"></a>
<a id="tocsportfoliorequest"></a>

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "types": [
    "tax_returns",
    "bank_statements",
    "credit_reports"
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|webhook|[Webhook](#schemawebhook)|false|none|Specifies to return extraction results to the defined webhook as soon as they're complete, <br>so you don't have to poll for results status. Sensible also calls this webhook on error.|
|types|[string]|false|none|Specifies the document types contained in the PDF portfolio.|

<h2 id="tocS_Extraction">Extraction</h2>
<!-- backwards compatibility -->
<a id="schemaextraction"></a>
<a id="schema_Extraction"></a>
<a id="tocSextraction"></a>
<a id="tocsextraction"></a>

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "configuration": "anyco_rate_confirmation",
  "status": "COMPLETE",
  "parsed_document": {
    "weight": {
      "source": "0.0lbs",
      "value": 0,
      "unit": "pounds",
      "type": "weight"
    },
    "distance": {
      "source": "193mi",
      "value": 193,
      "unit": "miles",
      "type": "distance"
    },
    "load_number": {
      "type": "string",
      "value": "Wk91242"
    },
    "carrier_email": null,
    "price": {
      "source": "$695.00",
      "value": 695,
      "unit": "$",
      "type": "currency"
    },
    "pickup_date": null
  },
  "validations": [
    {
      "description": "load weight should be over 1 ton",
      "severity": "warning"
    },
    {
      "description": "carrier email must be in format string@string",
      "severity": "skipped",
      "message": "Missing prerequisites - carrier_email"
    }
  ],
  "validations_summary": {
    "fields": 6,
    "fields_present": 4,
    "errors": 0,
    "warnings": 1,
    "skipped": 1
  },
  "classification_summary": [
    {
      "configuration": "anyco_rate_confirmation",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 3,
        "fields_present": 4,
        "penalities": 0.5
      }
    },
    {
      "configuration": "acme_co",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 0,
        "fields_present": 2,
        "penalities": 1.5
      }
    }
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|[ExtractionId](#schemaextractionid)|false|none|unique ID for the extraction, used to retrieve the extraction|
|created|[ExtractionCreated](#schemaextractioncreated)|false|none|date the extraction was created.|
|type|[ExtractionType](#schemaextractiontype)|false|none|the name of the document type.|
|configuration|string|false|none|the name of the config (SenseML query) used to extract the structured data. Sensible chooses the best config in the document type that fits the submitted document automatically|
|status|[ExtractionStatus](#schemaextractionstatus)|false|none|the extraction status (WAITING, COMPLETE, FAILED)|
|parsed_document|[ParsedDocument](#schemaparseddocument)|false|none|data extracted from the document, structured as an array of fields|
|validations|[Validations](#schemavalidations)|false|none|which extracted fields failed validation rules you write in the Sensible app.|
|validations_summary|[ValidationsSummary](#schemavalidationssummary)|false|none|Summary of the extracted fields that failed validation rules you write in the Sensible app.|
|classification_summary|[ClassificationSummary](#schemaclassificationsummary)|false|none|Metadata about how Sensible chose the config to use for this extraction.<br>Sensible compares all configs in the document type, then chooses the best extraction using<br>fingerprints, scores, or a combination of the two. <br>(When two extractions tie by score and fingerprints, Sensible chooses the <br>first configuration in alphabetic order).<br>For more details, see [fingerprints](https://docs.sensible.so/docs/fingerprint#notes)|

<h2 id="tocS_ExtractionAsyncResult">ExtractionAsyncResult</h2>
<!-- backwards compatibility -->
<a id="schemaextractionasyncresult"></a>
<a id="schema_ExtractionAsyncResult"></a>
<a id="tocSextractionasyncresult"></a>
<a id="tocsextractionasyncresult"></a>

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "configuration": "anyco_rate_confirmation",
  "status": "COMPLETE",
  "parsed_document": {
    "weight": {
      "source": "0.0lbs",
      "value": 0,
      "unit": "pounds",
      "type": "weight"
    },
    "distance": {
      "source": "193mi",
      "value": 193,
      "unit": "miles",
      "type": "distance"
    },
    "load_number": {
      "type": "string",
      "value": "Wk91242"
    },
    "carrier_email": null,
    "price": {
      "source": "$695.00",
      "value": 695,
      "unit": "$",
      "type": "currency"
    },
    "pickup_date": null
  },
  "validations": [
    {
      "description": "load weight should be over 1 ton",
      "severity": "warning"
    },
    {
      "description": "carrier email must be in format string@string",
      "severity": "skipped",
      "message": "Missing prerequisites - carrier_email"
    }
  ],
  "validations_summary": {
    "fields": 6,
    "fields_present": 4,
    "errors": 0,
    "warnings": 1,
    "skipped": 1
  },
  "classification_summary": [
    {
      "configuration": "anyco_rate_confirmation",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 3,
        "fields_present": 4,
        "penalities": 0.5
      }
    },
    {
      "configuration": "acme_co",
      "fingerprints": 2,
      "fingerprints_present": 2,
      "score": {
        "value": 0,
        "fields_present": 2,
        "penalities": 1.5
      }
    }
  ],
  "download_url": "https://sensible-so-document-type-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/246a6f60-0e5b-11eb-b720-295a6fba723e.pdf?AWSAccessKeyId=REDACTED"
}

```

### Properties

allOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[Extraction](#schemaextraction)|false|none|none|

and

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|object|false|none|none|
|» download_url|string|false|none|the URL of the document|

<h2 id="tocS_AsyncResponse">AsyncResponse</h2>
<!-- backwards compatibility -->
<a id="schemaasyncresponse"></a>
<a id="schema_AsyncResponse"></a>
<a id="tocSasyncresponse"></a>
<a id="tocsasyncresponse"></a>

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "status": "COMPLETE"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|[ExtractionId](#schemaextractionid)|false|none|unique ID for the extraction, used to retrieve the extraction|
|created|[ExtractionCreated](#schemaextractioncreated)|false|none|date the extraction was created.|
|type|[ExtractionType](#schemaextractiontype)|false|none|the name of the document type.|
|status|[ExtractionStatus](#schemaextractionstatus)|false|none|the extraction status (WAITING, COMPLETE, FAILED)|

<h2 id="tocS_AsyncUploadResponse">AsyncUploadResponse</h2>
<!-- backwards compatibility -->
<a id="schemaasyncuploadresponse"></a>
<a id="schema_AsyncUploadResponse"></a>
<a id="tocSasyncuploadresponse"></a>
<a id="tocsasyncuploadresponse"></a>

```json
{
  "id": "246a6f60-0e5b-11eb-b720-295a6fba723e",
  "created": "2019-08-24",
  "type": "rate_confirmation",
  "status": "COMPLETE",
  "upload_url": "https://sensible-so-utility-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/EXTRACTION_UPLOAD/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=REDACTED&Expires=1623861476&Signature=REDACTED&x-amz-security-token=REDACTED"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|[ExtractionId](#schemaextractionid)|false|none|unique ID for the extraction, used to retrieve the extraction|
|created|[ExtractionCreated](#schemaextractioncreated)|false|none|date the extraction was created.|
|type|[ExtractionType](#schemaextractiontype)|false|none|the name of the document type.|
|status|[ExtractionStatus](#schemaextractionstatus)|false|none|the extraction status (WAITING, COMPLETE, FAILED)|
|upload_url|string(url)|false|none|The URL at which to PUT the PDF bytes array for extraction. for example, curl -T ./sample.pdf "YOUR_UPLOAD_URL"|

<h2 id="tocS_ExtractFromUrlRequest">ExtractFromUrlRequest</h2>
<!-- backwards compatibility -->
<a id="schemaextractfromurlrequest"></a>
<a id="schema_ExtractFromUrlRequest"></a>
<a id="tocSextractfromurlrequest"></a>
<a id="tocsextractfromurlrequest"></a>

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "document_url": "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf",
  "content_type": "application/pdf"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|webhook|[Webhook](#schemawebhook)|false|none|Specifies to return extraction results to the defined webhook as soon as they're complete, <br>so you don't have to poll for results status. Sensible also calls this webhook on error.|
|document_url|[DocumentUrl](#schemadocumenturl)|false|none|URL that responds to a GET request with the bytes of the document to be extracted. <br>This URL must be either publicly accessible, or presigned with a security token as part of the URL path. <br>To check if the URL meets these criteria, open the URL with a web browser. <br>The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication.|
|content_type|[ContentType](#schemacontenttype)|false|none|The content type of the document being presented for extraction. This field is optional, but if supplied must be presented consistently<br>in all interactions.|

<h2 id="tocS_GenerateUrlRequest">GenerateUrlRequest</h2>
<!-- backwards compatibility -->
<a id="schemagenerateurlrequest"></a>
<a id="schema_GenerateUrlRequest"></a>
<a id="tocSgenerateurlrequest"></a>
<a id="tocsgenerateurlrequest"></a>

```json
{
  "webhook": {
    "url": "https://example.com/example_webhook_url",
    "payload": "info extra to the default extraction payload"
  },
  "content_type": "application/pdf"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|webhook|[Webhook](#schemawebhook)|false|none|Specifies to return extraction results to the defined webhook as soon as they're complete, <br>so you don't have to poll for results status. Sensible also calls this webhook on error.|
|content_type|[ContentType](#schemacontenttype)|false|none|The content type of the document being presented for extraction. This field is optional, but if supplied must be presented consistently<br>in all interactions.|

<h2 id="tocS_ExtractionId">ExtractionId</h2>
<!-- backwards compatibility -->
<a id="schemaextractionid"></a>
<a id="schema_ExtractionId"></a>
<a id="tocSextractionid"></a>
<a id="tocsextractionid"></a>

```json
"246a6f60-0e5b-11eb-b720-295a6fba723e"

```

unique ID for the extraction, used to retrieve the extraction

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string(uuid)|false|none|unique ID for the extraction, used to retrieve the extraction|

<h2 id="tocS_ExtractionCreated">ExtractionCreated</h2>
<!-- backwards compatibility -->
<a id="schemaextractioncreated"></a>
<a id="schema_ExtractionCreated"></a>
<a id="tocSextractioncreated"></a>
<a id="tocsextractioncreated"></a>

```json
"2019-08-24"

```

date the extraction was created.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string(date)|false|none|date the extraction was created.|

<h2 id="tocS_ExtractionType">ExtractionType</h2>
<!-- backwards compatibility -->
<a id="schemaextractiontype"></a>
<a id="schema_ExtractionType"></a>
<a id="tocSextractiontype"></a>
<a id="tocsextractiontype"></a>

```json
"rate_confirmation"

```

the name of the document type.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string|false|none|the name of the document type.|

<h2 id="tocS_ExtractionStatus">ExtractionStatus</h2>
<!-- backwards compatibility -->
<a id="schemaextractionstatus"></a>
<a id="schema_ExtractionStatus"></a>
<a id="tocSextractionstatus"></a>
<a id="tocsextractionstatus"></a>

```json
"COMPLETE"

```

the extraction status (WAITING, COMPLETE, FAILED)

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string|false|none|the extraction status (WAITING, COMPLETE, FAILED)|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|WAITING|
|*anonymous*|COMPLETE|
|*anonymous*|FAILED|

<h2 id="tocS_Webhook">Webhook</h2>
<!-- backwards compatibility -->
<a id="schemawebhook"></a>
<a id="schema_Webhook"></a>
<a id="tocSwebhook"></a>
<a id="tocswebhook"></a>

```json
{
  "url": "https://example.com/example_webhook_url",
  "payload": "info extra to the default extraction payload"
}

```

Specifies to return extraction results to the defined webhook as soon as they're complete, 
so you don't have to poll for results status. Sensible also calls this webhook on error.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|url|string(url)|false|none|the webhook destination. Sensible will POST to this URL when the extraction is complete.|
|payload|string|false|none|Include info additional to the API response, for example a UUID for verification.|

<h2 id="tocS_DocumentUrl">DocumentUrl</h2>
<!-- backwards compatibility -->
<a id="schemadocumenturl"></a>
<a id="schema_DocumentUrl"></a>
<a id="tocSdocumenturl"></a>
<a id="tocsdocumenturl"></a>

```json
"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf"

```

URL that responds to a GET request with the bytes of the document to be extracted. 
This URL must be either publicly accessible, or presigned with a security token as part of the URL path. 
To check if the URL meets these criteria, open the URL with a web browser. 
The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string(url)|false|none|URL that responds to a GET request with the bytes of the document to be extracted. <br>This URL must be either publicly accessible, or presigned with a security token as part of the URL path. <br>To check if the URL meets these criteria, open the URL with a web browser. <br>The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication.|

<h2 id="tocS_ContentType">ContentType</h2>
<!-- backwards compatibility -->
<a id="schemacontenttype"></a>
<a id="schema_ContentType"></a>
<a id="tocScontenttype"></a>
<a id="tocscontenttype"></a>

```json
"application/pdf"

```

The content type of the document being presented for extraction. This field is optional, but if supplied must be presented consistently
in all interactions.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string|false|none|The content type of the document being presented for extraction. This field is optional, but if supplied must be presented consistently<br>in all interactions.|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|application/pdf|
|*anonymous*|image/jpeg|
|*anonymous*|image/png|

