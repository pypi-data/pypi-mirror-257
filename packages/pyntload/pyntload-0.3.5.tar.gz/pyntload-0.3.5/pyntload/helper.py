import requests
import base64
import json

access_token=None

#base url
base_url = "https://adb-7118152657858843.3.azuredatabricks.net/"

def set_api_token(token):

    #set access token
    global access_token 
    access_token = token


def read_databricks_notebook(nb_path):
    #API does not accept /Workspace at beginning of path, remove
    nb_path = nb_path.split('/Workspace')[1]

    #get notebook export
    response = requests.request(
        "GET",
        base_url + "api/2.0/workspace/export",
        headers = {
        "Accept": "application/json,text/javascript,*/*",
        'Authorization': 'Bearer ' + access_token,
        "Content-Type": "application/json"
        },
        params= {
            'path': nb_path,
            'format': 'JUPYTER'
        }
    )
    
    #parse python code (json to dict)
    jupyter_code = json.loads(base64.b64decode(response.json()["content"]))
    jupyter_code_cells = [cell for cell in jupyter_code["cells"] if cell["cell_type"]=="code"]
    #jupyter_code_cells = [''.join(cell['source']) for cell in jupyter_code_cells]
        
    return jupyter_code_cells
