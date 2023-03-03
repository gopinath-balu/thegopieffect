import os
import json
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union

def parse_entities(data: str, entity: Union[str, list]) -> list:
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
    
    data = f'{{"text": "{sample_text}"}}'
    response = requests.post(MODEL_URL, headers=HEADERS, data=data)
    model_resp = response.json()

    if 'error' not in model_resp.keys():
        result = model_resp['result']
        for ent in entities:
            ent_list = list()
            for item in result:
                if item[1] == ent:
                    ent_list.append(item[0])
            return_dict[ent] = ent_list
        return return_dict
    else:
        raise Exception('Error in CliNER service, check!')  