import requests
import os
import json

README_API_KEY = os.environ['README_API_KEY']

def get_doc_slugs(cat_id):
    url = "https://dash.readme.com/api/v1/categories/document-types/docs"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic {}'.format(README_API_KEY),
    'x-readme-version': 'v0'
    }
    response_json = requests.request("GET", url, headers=headers, data=payload).json()
    return response_json

def get_ref_categories(categories):
    ref_categories = []
    for i in categories:
      if i["reference"] == True:
          ref_categories.append(i)
    return ref_categories 

def get_categories():
    url = "https://dash.readme.com/api/v1/categories"
    payload={}
    headers = {
    'Authorization': 'Basic {}'.format(README_API_KEY),
    'x-readme-version': 'v0'
    }
    response_json = requests.request("GET", url, headers=headers, data=payload).json()
    return response_json

def get_docs(category):
    category_slug = category["slug"]
    url = "https://dash.readme.com/api/v1/categories/{}/docs".format(category_slug)
    payload={}
    headers = {
    'Authorization': 'Basic {}'.format(README_API_KEY),
    'x-readme-version': 'v0',
    'Accept': 'application/json'
    }
    response_json = requests.request("GET", url, headers=headers, data=payload).json()
    return response_json


#def get_doc_markdown(doc_slug):

if __name__ == '__main__':
    categories = get_categories()
    ref_categories = get_ref_categories(categories)
    #print(json.dumps(ref_categories, indent=2))
    ref_docs = []
    print("PRINTING DOCS\n")
    for i in ref_categories:
        # get an array of docs for each cat
        cat_docs = get_docs(i)
        # flatten into 1 array of all docs
        for i in cat_docs:
            ref_docs.append(i)
    #print(json.dumps(ref_docs, indent =2))

    for i in (ref_docs):
        print(type(i))
        print(json.dumps(i, indent=2))
    #for i in ref_docs:
        #i = json.loads(i)
        #print(i)
