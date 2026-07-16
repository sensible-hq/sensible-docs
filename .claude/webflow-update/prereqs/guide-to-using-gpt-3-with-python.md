# Guide to Using GPT-3 with Python

## What Is GPT-3?

GPT-3 is the third iteration of the GPT series. It has been trained on over 175 billion parameters, making it one of the most powerful language models available. The model uses this vast amount of training data to accept input, process it, and appropriately respond to the user. Because of the model's ability to understand the content it receives, it excels at natural language processing tasks that often require an understanding of human-like text (free text) input.

OpenAI provides an [API](https://platform.openai.com/docs/) that lets you use GPT-3 in your applications. For example, your app could use the model to generate a summary of input data, such as a news article or a short book. GPT-3 can also extract structured information from free text, which you can then process in your app. For example, your Python app could use GPT-3 to retrieve details from a rental lease agreement, such as the start and end dates, monthly rent payment information, and termination conditions.

To access the OpenAI API, you can use any of OpenAI's [libraries](https://platform.openai.com/docs/libraries), which are available for several popular programming languages. In this article, you'll use the [Python library](https://pypi.org/project/openai/) to process data using GPT-3 in your application.

## Using GPT-3 with Python

The rest of this tutorial guides you through the process of creating a Python application using the GPT-3 model and testing it with several text-heavy tasks, such as summarizing text, fleshing out outlines, and writing content.

### Prerequisites

Make sure you've installed the [latest version of Python](https://www.python.org/downloads/) ([Python 3.11](https://www.python.org/downloads/release/python-3112/) at the time of writing). You'll also need to install [pip](https://pypi.org/project/pip/), the Python package installer, to download the necessary packages.

Since you'll be using the OpenAI API, you must [sign up for an account](https://platform.openai.com/signup/). Once you've registered, you should receive some free credits, which you'll use for the demonstration in this article. If you've already signed up and have depleted your free credits or they've expired, you'll have to pay for the tokens used in this demonstration.

### Creating the Python Project

Open a new terminal window and execute the following commands to create a new folder for your Python project and navigate into it:
    
    
    mkdir python-gpt-3
    cd python-gpt-3

Create a new file called `main.py`, which will contain the source code for your application:
    
    
    touch main.py

### Setting Up a Virtual Environment

To avoid polluting your global Python environment when installing Python packages, you can install additional packages like the OpenAI package in a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html). The virtual environment will ensure that the packages you install for this project don't interfere with other packages and package versions used by other Python projects.

To set up a new virtual environment, execute the following command in your terminal in your project directory:
    
    
    python -m venv ./venv

Once the command has created the virtual environment, run the appropriate command below in your project directory to activate it:

**Linux/macOS**
    
    
    source ./venv/bin/activate

**Windows (CMD)**
    
    
    venv\Scripts\activate.bat

**Windows (PowerShell)**
    
    
    venv\Scripts\Activate.ps1

The virtual environment name (`venv`) should now appear to the left of your terminal prompt in parentheses:

### Installing the OpenAI Package

You'll use the OpenAI Python package to access the OpenAI API. The package offers methods and classes that simplify accessing different OpenAI models from Python.

Make sure your virtual environment is activated (ie, the environment name appears to the left of your terminal prompt) and install the `openai` package using pip:
    
    
    pip install openai

Once pip downloads and installs the package, you can integrate your Python application with OpenAI, as shown in the next section.

### Retrieving and Setting the OpenAI API Key

Before you can access the OpenAI API from your application, you'll need to retrieve and set the API key your application should use to access OpenAI.

You can retrieve this key by logging in to the [OpenAI platform](https://platform.openai.com/), selecting your account in the top-right menu, and clicking **View API keys** :

On the page that appears, click the **Create new secret key** button. A dialog window should appear containing your API key. Copy the key before closing the dialog box, as you cannot view the key again for security reasons.

In your terminal window, set the `OPENAI_API_KEY` environment variable for the current session by running the appropriate command below, replacing `{OPENAI_API_KEY}` with the API key you retrieved from your OpenAI platform:

**Linux/macOS**
    
    
    export OPENAI_API_KEY={OPENAI_API_KEY}

**Windows (CMD)**
    
    
    set OPENAI_API_KEY={OPENAI_API_KEY}

**Windows (PowerShell)**
    
    
    $env:$OPENAI_API_KEY = {OPENAI_API_KEY}

This environment variable will be read by your Python application and used to access the OpenAI API in the following sections.

### Developing the Python Application

You're now ready to begin developing your Python application. To start, simply open the project folder in your preferred code editor.

If you're using [Visual Studio Code](https://code.visualstudio.com/), you can use the following terminal command to open the project folder:
    
    
    code .

#### Importing Packages

Open the `main.py` file and add the following import statements:
    
    
    import os
    import openai

In the snippet above, you first import the `os` package. This package reads environment variables so you can access the `OPENAI_API_KEY` environment variable value in your Python application. Next, you also import the `openai` package, which you’ll use to send requests to OpenAI’s API and receive responses from the API.

#### Loading the Prompt File

GPT-3 can perform text-heavy tasks that involve lengthy and multiline text. To make it easier to input these tasks in Python, you can store the prompts in text files and prompt the user to enter the name of the text file they want to use as input.

Paste the following lines of code at the bottom of your `main.py` file:
    
    
    prompt_file = input("Prompt file: ")
    
    prompt = ""
    with open(prompt_file, "r") as f:
        prompt = f.read()

This code will prompt the user for a prompt file and read the contents of that file into a `prompt` variable.

#### Sending the Prompt to OpenAI

You can now send the prompt to GPT-3 using the `openai` package you imported earlier. Paste the following code at the bottom of your Python script:
    
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    

The snippet above first loads the OpenAI API key from the `OPENAI_API_KEY` environment variable and assigns it to the `api_key` variable in the `openai` package.

Then, the code sends the prompt to the `gpt-3.5-turbo` model. Several language models provided by OpenAI are available over the API, each optimized for particular use cases. The most suitable models for the tasks demonstrated in this article are the `gpt-3.5-turbo` and `text-davinci-003` models. The snippet above uses `gpt-3.5-turbo` since it’s the cheaper option of the two models.

Since `gpt-3.5-turbo` is designed to be a chat completion model, you specify the prompt in a message object from the user. This prompt is then sent to OpenAI to be processed. When the model has processed the `prompt`, a response is returned and stored in the `response` variable in the snippet above. You’ll output the answer in the next section.

#### Outputting the Response

You can output the response to the prompt you sent to the OpenAI API using the following code (paste it at the bottom of your `main.py` file): 
    
    
    print(response.choices[0].message.content)

### Testing the Script

Now that you've written a Python script to send prompts to OpenAI's GPT-3 model and print the response, you can test the model with different prompts to see how well it performs various text-heavy processing tasks.

#### Summarizing Text

The first prompt you'll test summarizes a passage of text into a couple of sentences. Create a new file called `prompt-summarize.txt` in your project directory and paste the following text:
    
    
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California. Apple is the largest technology company by revenue, totaling US$394.3 billion in 2022. As of March 2023, Apple is the world's biggest company by market capitalization. As of June 2022, Apple is the fourth-largest personal computer vendor by unit sales and second-largest mobile phone manufacturer. It is one of the Big Five American information technology companies, alongside Alphabet (known for Google), Amazon, Meta (known for Facebook), and Microsoft.
    
    Apple was founded as Apple Computer Company on April 1, 1976, by Steve Wozniak, Steve Jobs and Ronald Wayne to develop and sell Wozniak's Apple I personal computer. It was incorporated by Jobs and Wozniak as Apple Computer, Inc. in 1977. The company's second computer, the Apple II, became a best seller and one of the first mass-produced microcomputers. Apple went public in 1980 to instant financial success. The company developed computers featuring innovative graphical user interfaces, including the 1984 original Macintosh, announced that year in a critically acclaimed advertisement. By 1985, the high cost of its products, and power struggles between executives, caused problems. Wozniak stepped back from Apple amicably and pursued other ventures, while Jobs resigned bitterly and founded NeXT, taking some Apple employees with him.
    
    As the market for personal computers expanded and evolved throughout the 1990s, Apple lost considerable market share to the lower-priced duopoly of the Microsoft Windows operating system on Intel-powered PC clones (also known as "Wintel"). In 1997, weeks away from bankruptcy, the company bought NeXT to resolve Apple's unsuccessful operating system strategy and entice Jobs back to the company. Over the next decade, Jobs guided Apple back to profitability through a number of tactics including introducing the iMac, iPod, iPhone and iPad to critical acclaim, launching the "Think different" campaign and other memorable advertising campaigns, opening the Apple Store retail chain, and acquiring numerous companies to broaden the company's product portfolio. When Jobs resigned in 2011 for health reasons, and died two months later, he was succeeded as CEO by Tim Cook.
    
    Apple became the first publicly traded U.S. company to be valued at over $1 trillion in August 2018, then $2 trillion in August 2020, and $3 trillion in January 2022. As of January 2023, it was valued at around $2.2 trillion. The company receives criticism regarding the labor practices of its contractors, its environmental practices, and its business ethics, including anti-competitive practices and materials sourcing. Nevertheless, the company has a large following and enjoys a high level of brand loyalty. It is ranked as one of the world's most valuable brands.
    
    ---
    
    Summarize the article above into four sentences.

The prompt above contains a few paragraphs from [Apple's Wikipedia page](https://en.wikipedia.org/wiki/Apple_Inc.). At the end of the file, there are instructions that tell GPT-3 to summarize the article into four sentences.

Run your Python script using the command below:
    
    
    python main.py

When asked to specify the prompt file, enter `prompt-summarize.txt`:
    
    
    Prompt file: prompt-summarize.txt

The script will take a few seconds to send the prompt to OpenAI and receive a response. Once the API returns a reply, you should see it outputted in the terminal window. Below is an example of a response you might receive; you'll see a different output since GPT-3 is a [non-deterministic model](https://platform.openai.com/docs/models/gpt-3-5), meaning the same inputs can produce different results:
    
    
    Apple is an American technology company that is the largest technology company in terms of revenue and the world's biggest company by market capitalization. It was founded in 1976 by Steve Wozniak, Steve Jobs, and Ronald Wayne. Over the years, the company faced challenges and lost market share to competitors but regained profitability under the leadership of Jobs, who introduced innovative products and strategies. Today, Apple is valued at over $2 trillion but receives criticism for its labor and environmental practices, and business ethics.

Apple is an American technology company that is the largest technology company in terms of revenue and the world's biggest company by market capitalization. It was founded in 1976 by Steve Wozniak, Steve Jobs, and Ronald Wayne. Over the years, the company faced challenges and lost market share to competitors but regained profitability under the leadership of Jobs, who introduced innovative products and strategies. Today, Apple is valued at over $2 trillion but receives criticism for its labor and environmental practices, and business ethics.

Notice how the example response above contains a summary of the Wikipedia article paragraphs in exactly four sentences, as instructed.

#### Generating a Twitter Thread

Since OpenAI trained GPT-3 on a vast amount of input data from different disciplines, you can use the learned data to create brief content on a particular topic in its training base. The following example explains how to prompt GPT-3 to generate a Twitter thread with five tips on how to pay down your debt faster.

Create a new file called `prompt-twitter-thread.txt` in your project folder and paste the following prompt:
    
    
    Write a Twitter thread with 5 tips on how to pay down your debt faster. Each tip should have a title and a description of that tip. Include an introduction tweet with a captivating opening statement to entice the user to open the thread. Also include a conclusion tweet listing all the tips in order. Include appropriate hashtags at the bottom of each tweet in the thread.

The prompt instructs GPT-3 to write a Twitter thread with five tips on paying down your debt faster. It also provides additional instructions on formatting the Twitter thread and its tweets, including an opening tweet with a captivating statement and a conclusion tweet listing all the tips in order. The prompt also instructs GPT-3 to include suitable hashtags in each tweet.

Rerun your Python script using the command below:
    
    
    python main.py

When asked to specify the prompt file, enter the `prompt-twitter-thread.txt` file:
    
    
    Prompt file: prompt-twitter-thread.txt

After a couple of seconds, you should see a response printed in the terminal. Below is an example of the kind of answer you can expect:
    
    
    Introduction: If you feel like you're drowning in debt, you're not alone! But don't worry, there are steps you can take to pay down debt faster. Here are 5 tips to help you get closer to financial freedom. #DebtFree #FinancialFreedom
    
    Tip 1: Prioritize debts with higher interest rates 
    Start by paying off debts with higher interest rates first. The faster you pay them off, the less interest you'll have to pay. This method will also save you more money in the long run. #HighInterestRates #CreditCardDebt
    
    Tip 2: Create a budget and stick to it 
    Developing a budget will help you see where your money is going, and help you identify areas where you can cut back or eliminate unnecessary spending. Stay committed to your budget, and you'll be on the path to paying off debt faster. #Budgeting #DebtManagement
    
    Tip 3: Consider debt consolidation 
    If you're struggling to keep track of multiple debts and payments, consider consolidation. Debt consolidation allows you to combine multiple debts into one manageable payment. This can make it easier to pay off debt faster. #DebtConsolidation #Loan
    
    Tip 4: Increase your payments 
    Make more than the minimum monthly payments on your debts. Even increasing your payments by a small amount each month can help get you out of debt faster. This method will also help to reduce the amount of interest you'll owe. #PayingMore #FasterDebtPayoff
    
    Tip 5: Focus on increasing your income 
    Consider taking on a second job or side hustle to help generate extra income. Use the additional earnings to pay down your debts faster. This might require a bit of sacrifice, but it'll ultimately lead to financial freedom. #SideHustle #FinancialGoals
    
    Conclusion:  Seems like a lot of work, right? But implementing these tips will help you pay off debts faster and achieve financial freedom. To summarize, prioritize high interest debts, create a budget and stick to it, consider debt consolidation, increase your payments, and focus on increasing your income. You got this! #DebtFree #FinancialFreedom #DebtManagement

Notice how the response contains a total of seven tweets. The first tweet introduces the thread, the following five tweets list and elaborate on each tip, and the last tweet summarizes the tips.

#### Extracting Structured Data

The final example extracts structured information from a [fictional bank statement for Bank of America](https://github.com/sensible-hq/sensible-configuration-library/tree/main/bank_statements/bank_of_america), retrieved from [Sensible's configuration library repository](https://github.com/sensible-hq/sensible-configuration-library).

Create a `prompt-bank-statement.txt` file in the project's root directory and paste the following text into the file:
    
    
    BANK OF AMERICA
    
    Customer service information
    Customer service: 1.800.432.1000
    bankofamerica.com
    Bank of America, N.A.
    
    Your Adv Plus Banking
    for June 10, 2021 to July 9, 2021
    
    | Beginning balance on June 10, 2021 | $2,825.37     |
    | Deposits and other additions       | 7667.50       |
    | Withdrawals and other subtractions | -7755.02      |
    | Checks                             | -0.00         |
    | Service Fees                       | -1.81         |
    | **Ending balance on July 9, 2021** | **$2,736.04** |
    
    ---
    
    Convert the bank statement above into a JSON object according to the JSON schema defined below. Do not output the schema itself but transform the statement data into a JSON object representing the schema. Make sure to format dates in the `yyyy-mm-dd` format and output all amounts as numbers only without the currency.
    
    {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "type": "object",
      "properties": {
        "bank": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "website": {
              "type": "string"
            }
          },
          "required": [
            "name",
            "website"
          ]
        },
        "startDate": {
          "type": "string"
        },
        "endDate": {
          "type": "string"
        },
        "currency": {
          "type": "string"
        },
        "openingBalance": {
          "type": "number"
        },
        "closingBalance": {
          "type": "number"
        },
        "transactions": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "description": {
                  "type": "string"
                },
                "amount": {
                  "type": "number"
                }
              },
              "required": [
                "description",
                "amount"
              ]
            }
          ]
        }
      },
      "required": [
        "bank",
        "startDate",
        "endDate",
        "currency",
        "openingBalance",
        "closingBalance",
        "transactions"
      ]
    }

The prompt above contains a text representation of the bank statement, including instructions for GPT-3 on how to handle the bank statement at the end of the text. The prompt requests that GPT-3 produce a JSON object that matches the JSON schema specified. By using a JSON schema, you can extract information from different data sources into a consistent JSON object that can be processed by your system. In this case, you extract the bank details, statement dates, currency, opening and closing balance, and the transactions.

Rerun the script:
    
    
    python main.py

When asked to specify a prompt file, enter `prompt-bank-statement.txt`:
    
    
    Prompt file: prompt-bank-statement.txt

A few seconds later, you should see the response from GPT-3. Below is a sample output:
    
    
    {
      "bank": {
        "name": "Bank of America",
        "website": "bankofamerica.com"
      },
      "startDate": "2021-06-10",
      "endDate": "2021-07-09",
      "currency": "USD",
      "openingBalance": 2825.37,
      "closingBalance": 2736.04,
      "transactions": [
        {
          "description": "Deposits and other additions",
          "amount": 7667.50
        },
        {
          "description": "Withdrawals and other subtractions",
          "amount": -7755.02
        },
        {
          "description": "Checks",
          "amount": 0.00
        },
        {
          "description": "Service Fees",
          "amount": -1.81
        }
      ]
    }

Notice how the output contains a valid JSON object with all the requested information from the bank statement. You could ingest this JSON object in your application for several use cases, such as importing a bank statement into an accounting system or calculating the total money received and spent by the account holder.

## Conclusion

As you've seen, GPT-3 from [OpenAI](https://openai.com/) is an impressive language model that provides developers with a powerful tool for performing text-heavy natural language processing tasks. In this article, you learned about some use cases for GPT-3 and then developed a Python application that harnesses the OpenAI API to leverage GPT-3's capabilities across several use cases.

Using GPT-3, your application can understand free text by translating it into structured data. [Sensible](https://www.sensible.so/) is a document extraction platform for developers that integrates with GPT-3 and GPT-4. Using Sensible, you can convert PDF documents and images into structured data in seconds using an LLM. The platform provides multiple [natural language processing methods](https://docs.sensible.so/docs/natural-language-methods) depending on the kind of data you want to extract. These methods include the List method, which extracts lists of data from a document where you’re not sure of the data structure; the NLP Table method, which extracts data out of a document that’s inside a table; the Query method, which can find a single fact or data point in your document; and, finally, the Summarizer computed field method and Topic method, which are similar to the List method but provide more configuration options. Using these methods, you can easily extract all kinds of information from your unstructured data.

Another benefit of Sensible is that, unlike the examples in this article, you don't need to create an OpenAI account, manage OpenAI API keys to access GPT-3, or worry about context windows because it's already baked into Sensible. [Get your free Sensible API key](https://app.sensible.so/register/) today and see LLMs can be used for document extraction!

‍

‍
