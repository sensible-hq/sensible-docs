import json
import requests
import os
import shutil
import pandas as pd
import tkinter as tk
# import sys


# The name of a document type in Sensible, e.g., auto_insurance_quote
DOCUMENT_TYPE = "walkthroughs"
# store your key as an env variable in the command line using
# export SENSIBLE_API_KEY = "<Your_Key>" 
# or hardcode it instead as SENSIBLE_API_KEY = "<Your_Key>"
SENSIBLE_API_KEY = input('enter your Sensible API key') 


def extract_doc(pdf_bytes):
    headers = {
        'Authorization': 'Bearer {}'.format(SENSIBLE_API_KEY),
        'Content-Type': 'application/pdf'
    }
    body = pdf_bytes
    response = requests.request(
        "POST",
        "https://api.sensible.so/dev/extract/{}".format(DOCUMENT_TYPE),
        headers=headers,
        data=body)
    try:
        response.raise_for_status()
    except requests.RequestException:
        print(response.text)
    else:
        return response


if __name__ == '__main__':

    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    
    validations = {}
    for file in os.listdir(path):
        # TODO: test if works when dir is a parent rel to scripts dir

        simple_dict = {}

        if(file.endswith(".pdf") or file.endswith(".PDF")):
          with open(os.path.join(path, file), 'rb') as pdf_file:
            pdf_bytes = pdf_file.read()
          response =  extract_doc(pdf_bytes)
          json_response = response.json()
          # The API response has more info than needed for a simple spreadsheet, so cherry pick
          # the field names and their values from the parsed_document object in the response
          # into a simpler dictionary
          parsed_doc = json_response["parsed_document"]
          for key,value in parsed_doc.items():
            if isinstance(value, dict):
              simple_dict[key] = value["value"] 
          print("Validations summary for extraction " , json_response["id"], ":  ", json_response["validation_summary"])
          validations[json_response["id"]] = json_response["validations"]
          
             
          # write the API response to file
          file_name = json_response["id"] + ".json"
            
          path_to_json = os.path.join(os.path.dirname( __file__ ), results_path, file_name)
          with open(path_to_json, 'w+', encoding ='utf-8') as temp_file: 
            temp_file.write(json.dumps(simple_dict, indent=2, sort_keys = True)) 
    # write any extraction errors or warnings to file
    print(validations)
    validations_path = os.path.join(os.path.dirname( __file__ ), "validations.json")
    with open(validations_path, 'w+', encoding ='utf-8') as temp_file:
      temp_file.write(json.dumps(validations, indent=2, sort_keys = True)) 
    # convert the API responses to a CSV table
    convert_json(results_path)      