import requests
import os
import json

README_API_KEY = os.environ['README_API_KEY']

'''
the check_links.rb is the main checking script
this is a helper script that uses the readme API to download the changelogs (authored at dash.readme rather than locally) to markdown
so the main check_links.rb can convert it to HTML with the rest of the markdown and check the links
extra defs are included for eventually getting API reference pages for checking links in descriptions (tricker task)
'''

def get_changelogs():
    url = "https://dash.readme.com/api/v1/changelogs?perPage=10&page=1"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic {}'.format(README_API_KEY),
    'x-readme-version': 'v0'
    }
    response_json = requests.request("GET", url, headers=headers, data=payload).json()
    #print(json.dumps(response_json, indent=2))

    # script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "./out_changelogs/"
    if not os.path.exists(rel_path):
      # os.makedirs(rel_path, 0o755)
      os.makedirs(rel_path)
    file_path = os.path.join(rel_path + "all_changelogs" + "." + "html")
    print("PATHS: current:", os.getcwd())
    print("PATHS: intended dest:", file_path)
    # left off TODO: make an out dir?
    for page in response_json:
      #print(json.dumps(page['html'], indent=2))
      # left off: write each html to some ./out dir, same as the ruby one...
      with open(file_path, 'a+') as f:
        f.write(page['html'])
    #print("ALL CHANGELOGS")
    #with open(file_path, 'r') as fin:
      #print(fin.read())
    print("in out_changelogs dir:")
    print(os.path.abspath(rel_path))
    print(os.listdir(rel_path))


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


def get_doc_markdown(doc):
    doc_slug = doc["slug"]
    url = "https://dash.readme.com/api/v1/docs/{}".format(doc_slug)
    payload={}
    headers = {
    'Authorization': 'Basic {}'.format(README_API_KEY),
    'x-readme-version': 'v0',
    'Accept': 'application/json'
    }
    response_json = requests.request("GET", url, headers=headers, data=payload).json()
    return response_json

if __name__ == '__main__':
    get_changelogs()

    '''
    # get the API reference documents:
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

    for i in (ref_docs):
        doc_json = get_doc_markdown(i)
        #print(doc_json["title"])
        #print(doc_json["slug"])
        #print(doc_json["body"])
        print(json.dumps(doc_json, indent=2))
        # left off: dang. no good way to get markdown from this unless I'm willing to only test the 'body' and save it as markdown :/
     '''
