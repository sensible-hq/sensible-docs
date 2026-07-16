# Converting a PDF to Excel Using Python

## How to Convert a PDF to Excel Using Python

The tutorial uses weekly [situation report PDFs](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports) from the [WHO](https://www.who.int/) on [COVID-19](https://www.who.int/health-topics/coronavirus) to show you how to convert a PDF to Excel using Python. You’ll use the Sensible API to configure a scraper to extract information about new cases, deaths, and so on from a table in the PDF over a 28-day period and then save that data in an Excel file.

### Prerequisites

Before continuing, make sure that you have the following set up:

  * [Python 3.10](https://www.python.org/downloads/release/python-31010/) installed on your computer
  * A code editor like [Visual Studio Code](https://code.visualstudio.com/)
  * A browser with an internet connection



### Getting Started

To begin, make a project directory and launch a terminal within it. Run the following commands in the terminal to create and activate a Python virtual environment:
    
    
    $ python3 -m venv env
    $ source env/bin/activate
    

Then, run the following command to install the `requests` library in Python:
    
    
    $ pip install requests
    

This library will communicate with the Sensible API via [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) requests.

Next, open your browser and navigate to the [Sensible user registration](https://app.sensible.so/register/) page. Enter the requested details into the form on the page and click the **Create account** button, then enter the verification code you received via email:

‍

Sign in to your account, enter the additional detail requested, and click **Submit** to access the Sensible web app:

### Creating Your API Key

To create your Sensible API key, first click the **profile icon** in the top right corner of the page. This action will open a drop down menu. From this menu, select the [**Account settings**](https://app.sensible.so/account/) option. On the page that loads, create your API key by clicking the **Create API key** button which opens a dialogue box. Enter a description for the API key and your account password in the respective fields shown in the image below. Then, click the **Create** button.

Finally, click the **Clipboard Icon** shown below to copy your API key.

To use an existing Sensible API key instead, scroll horizontally in the “API keys” section and click the **three dots menu** button. Then, click the **Retrieve Key** option, enter your password, and copy your API key.

You will use this API key in the next few steps as you write and run the Python script.

### Creating a Configuration

[Configurations](https://docs.sensible.so/docs/senseml-reference-introduction) are JSON files that allow you to extract data from documents using SenseML, Sensible’s query language.

To create a configuration, first, return to the Sensible web app and navigate to the **Document Types** page. Then, click **New document type** to open a dialog box. Enter the name of the document type as shown below, leave all other options in their default state, and click **Create** :

This creates and opens the document type. The **Configurations** tab is opened by default within the document type. To make a configuration, click the **Create configuration** button, give it a name, and then click the **Create** button:

Next, navigate to the **Reference documents** tab. Here, you must include one or more good examples of the types of documents that are expected when this document type is used. Download the PDF of the [COVID-19 situation report for March 8, 2023](https://www.who.int/publications/m/item/weekly-epidemiological-update-on-covid-19---8-march-2023).

Click the **Upload document** button, attach the report, and select the configuration created earlier under the **Associated configuration** field. Then, click the **Upload** button:

After that, open the configuration editor by clicking any part of the reference document. Enter the following configuration in the left pane of this screen to extract the desired content from the document:
    
    
    {
      "fields": [
        {
          "id": "newly_reported_covid_19_cases",
          "anchor": "Newly reported and cumulative COVID-19 confirmed cases and deaths",
          "type": "table",
          "method": {
            "id": "table",
            "columns": [
              {
                "id": "WHO Region",
                "terms": [
                  "WHO Region"
                ],
                "isRequired": true
              },
              {
                "id": "New cases in 28 days",
                "terms": [
                  "New cases in",
                  "last 28 days"
                ],
                "stopTerms": [
                  "change",
                  "death"
                ],
                "isRequired": true,
                "type": {
                  "id": "custom",
                  "pattern": "^[0-9 ]+",
                  "type": "number"
                }
              },
              {
                "id": "Change in new cases in 28 days (%)",
                "terms": [
                  "Change in",
                  "new cases in",
                  "last 28 days *"
                ],
                "stopTerms": [
                  "death"
                ],
                "isRequired": true
              },
              {
                "id": "Cumulative cases",
                "terms": [
                  "Cumulative cases"
                ],
                "isRequired": true,
                "type": {
                  "id": "custom",
                  "pattern": "^[0-9 ]+",
                  "type": "number"
                }
              },
              {
                "id": "New deaths in 28 days",
                "terms": [
                  "new deaths",
                  "in last 28",
                  "days (%)"
                ],
                "stopTerms": [
                  "change"
                ],
                "isRequired": true,
                "type": {
                  "id": "custom",
                  "pattern": "^[0-9 ]+",
                  "type": "number"
                }
              },
              {
                "id": "Change in new deaths in 28 days (%)",
                "terms": [
                  "Change in",
                  "new deaths",
                  "in last 28"
                ],
                "isRequired": true
              },
              {
                "id": "Cumulative deaths",
                "terms": [
                  "Cumulative deaths",
                ],
                "isRequired": true,
                "type": {
                  "id": "custom",
                  "pattern": "^[0-9 ]+",
                  "type": "number"
                }
              }
            ],
            "stop": {
              "type": "startsWith",
              "text": "*Percent change in the"
            }
          }
        }
      ]
    }
    

This configuration file is a nested JSON object. The first level defines a `"fields"` key that takes a list of JSON objects. The objects under the `"fields"` key define the section of the text to focus on. In this case, the code is extracting the content of a table. To help Sensible locate the table of interest, the configuration assigns the `"anchor"` key to a string that contains relevant text in the table's title and defines the field type as `"table"`.

Next, the configuration defines a `"methods"` key. The value of this field is another object that contains an `"id"` and a `"columns"` key. The `"columns"` key defines all the relevant columns of interest in the table. For every column, the code defines an identifier using `"id"` and sets the `"isRequired"` key to true. It also defines the `"terms"` key as a list of terms that are present in the column name to allow Sensible to locate them more easily. Additionally, it defines `"stopTerms"` for some columns to prevent Sensible from associating your desired column with other columns that contain those terms.

The configuration also adds a `"type"` key for columns that contain numeric values without spaces to identify them as numbers. In other cases, a custom type is used to extract only the number from the text using regular expression. Finally, it defines a `"stop"` key to let Sensible know where the table ends. The extracted result is displayed on the right pane, as shown below:

Click the **Publish** button on the top right, and then click **Publish to development** in the window that appears:

Take note that the environment is set to **Development**. This will be referenced in the code. You now have a configuration that can be used to extract data from any similar PDF file.

### Extracting Data with Python

To test your configuration, create a Python script and add the following lines of code to import the required libraries and define the document type, environment, and document name as variables:
    
    
    import requests
    
    document_type = "covid_reports"
    environment = "development"
    document_name = "pdfs/20230301_Weekly_Epi_Update_132.pdf"
    

Store the Sensible API key you saved from the Sensible dashboard in a variable in your script, as shown below:
    
    
    SENSIBLE_API_KEY = "INSERT YOUR API KEY HERE"
    

Next, in the script, add the following lines of code to define a function for extracting content from PDF files using the configuration you published:
    
    
    def extract_content(d_type: str, d_name: str, env: str) -> dict:
        url = "https://api.sensible.so/v0/extract/{}?environment={}".format(d_type, env)
    
        headers = {
            "Authorization": 'Bearer {}'.format(SENSIBLE_API_KEY),
            "content-type": "application/pdf"
        }
    
        with open(d_name, 'rb') as fp:
            pdf_file = fp.read()
            response = requests.post(url, headers=headers, data=pdf_file)
    
            print("Extraction Status code: {}".format(response.status_code))
            if response.status_code == 200:
                return response.json()
            else:
                print(response.json())
    

The code block above defines a function called `extract_content`. This function takes three parameters—document type, document name, and API environment—and returns the extracted data as a dictionary. It first specifies the URL endpoint to which you will make a request. It then defines the request header as a dictionary containing the authorization details and the content type. The function then opens the PDF file to be scraped and passes the PDF content and the defined URL endpoint and header to the `requests.post` method. Finally, the function prints the status code and returns the content of the response.

Next, define a function that will convert the extracted content to an Excel file. Sensible supports [generating Excel files](https://docs.sensible.so/reference/get-excel-extraction) natively, so to do this, add the code below to the script:
    
    
    def convert_to_excel(ids: str) -> str:
        url = "https://api.sensible.so/v0/generate_excel/{}".format(ids)
    
        headers = {
            "accept": "application/json",
            "Authorization": 'Bearer {}'.format(SENSIBLE_API_KEY)
        }
    
        response = requests.get(url, headers=headers)
    
        print("Conversion Status code: {}".format(response.status_code))
        if response.status_code == 200:
            data = response.json()
            return data["url"]
        else:
            print(response.json())
    

This code block defines the `convert_to_excel` method. This method takes the document ID and returns a link to a URL for downloading the Excel file. The function first defines the URL for the API's `generate_excel` endpoint. In this case, the document ID is attached to the URL. Then, as before, it defines the request header with the content type and authorization details. Next, the function makes a GET request by passing the URL and the header to the `requests.get` method. If the response status code is `200` (OK), it returns the URL to download the Excel file. This URL is only available for fifteen minutes.

With the download URL obtained, enter the following lines of code into the script to define a function to download the Excel file to your project directory:
    
    
    def download_xlsx(url: str, d_name: str) -> None:
        response = requests.get(url)
        filename = "{}.xlsx".format(d_name)
        with open(filename, "wb") as fp:
            fp.write(response.content)
    
        print("{} downloaded.".format(filename))
    

This code defines a function to download the file at a given URL. It makes a GET request with the URL and then saves the results to an Excel file.

With these functions defined, you can now extract content from a PDF file and save it as an Excel file.

To test this, download the [COVID-19 situation report for March 1, 2023](https://www.who.int/publications/m/item/weekly-epidemiological-update-on-covid-19---1-march-2023), create a subdirectory named `pdfs` in your project directory, and save the report there.

Then, enter the code below to run all of the functions you've created on the newly downloaded PDF file:
    
    
    pdf_content = extract_content(document_type, document_name, environment)
    
    url = convert_to_excel(pdf_content["id"])
    
    if url is not None:
        download_xlsx(url, document_name[:-4])
    

This code block defines three variables for the document type, environment, and document name. These variables are passed to the `extract_content` function, which returns the relevant content. The ID of this content is then passed to the `convert_to_excel` function, which returns the download URL. This URL is then passed to the `download_xlsx` function, which downloads the Excel file to your project directory.

When you open the file, you should find content similar to the snippet below:

You have now successfully extracted data from a PDF file and converted it to an Excel file. This tutorial’s configuration, source code, and files can be found in [this GitHub repository](https://github.com/sensible-hq/tutorial-pdf-to-excel).

## Conclusion

In this tutorial, you converted PDF files to Excel and used the Sensible web app to create a custom document type as well as a configuration to extract relevant data. Finally, you used Python to interact with the Sensible API to extract and convert data from PDF to Excel.

[Sensible](https://sensible.so/) is a developer-focused document orchestration platform. It allows you to use fine-grained configurations to extract data from structured and unstructured documents. Sensible accomplishes this through the use of SenseML, a JSON-formatted query language. This query language employs machine learning techniques such as natural language processing and optical character recognition to ensure that desired data can be extracted regardless of its format. Try out [Sensible](https://app.sensible.so/) today.

‍
