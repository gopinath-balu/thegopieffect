import os
import json
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union

#Python #NLP #NER #Nifty

def parse_entities(data: str, entity: Union[str, list] = 'All') -> list:
    """Parse given entities from the data
        unique_entities = {'ACUITY', 'BRAND_NAME', 'DIAGNOSIS', 
                           'DIRECTION', 'DOSAGE', 'DURATION',
                           'DX_NAME', 'FORM', 'FREQUENCY',
                           'GENERIC_NAME', 'O', 'PROCEDURE_NAME',
                           'ROUTE_OR_MODE', 'SIGN', 'STRENGTH',
                           'SYMPTOM', 'SYSTEM_ORGAN_SITE',
                           'TEST_NAME', 'TEST_UNIT', 
                           'TEST_VALUE', 'TREATMENT_NAME'
                          }
    Args:
        data (str): Textual data to be parsed entities
        entity (Union[str, list]): Entity which needs to be parsed
    Returns:
        list: List of parsed entities
    """
    MODEL_URL = 'http://0.0.0.0:8080/cliner-service/ner'
    HEADERS   = {'Content-type': 'application/json',}
    
    return_dict = dict()
    
    if isinstance(entity, str):
        entities = [entity]
    elif isinstance(entity, list):
        entities = entity
    
    assert isinstance(entities, list)
    
    data = f'{{"text": "{data}"}}'
    response = requests.post(MODEL_URL, headers=HEADERS, data=data.encode('utf-8'))
    model_resp = response.json()

    if 'error' not in model_resp.keys():
        result = model_resp['result']
        if set(entities) == {'All'}:
            for term, ent in result:
                return_dict.setdefault(ent, []).append((term))
            del return_dict['O']
            return return_dict
        else:
            for ent in entities:
                ent_list = list()
                for item in result:
                    if item[1] == ent:
                        ent_list.append(item[0])
                return_dict[ent] = ent_list
        return return_dict
    else:
        raise Exception('Error in CliNER service, check!')
        
        
#Python #Core #List #Grouping

def group_list_on_keys(list_of_lists: list[list]) -> dict:
    """Group list of lists based on a given key in the element of list
        #input
        data=[
                ['Sarah',  '12', 'Chocolate'],
                ['Anders', '11', 'Vanilla'],
                ['Sarah',  '13', 'Strawberry'],
                ['John',   '11', 'None']
              ]
        #output
        {
         'Sarah': [('12', 'Chocolate'), ('13', 'Strawberry')], 
         'Anders': [('11', 'Vanilla')], 
         'John': [('11', 'None')]
        }

    Args:
        list_of_lists (list[list]): Given input list of list

    Returns:
        dict: Grouped output based on one key
    """

    grouped = {}

    for name, x, y in data:
        grouped.setdefault(name, []).append((x,y))

    return grouped
