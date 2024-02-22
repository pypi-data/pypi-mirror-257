import requests
import base64
import json

#base url
base_url = "https://adb-7118152657858843.3.azuredatabricks.net/"
access_token="dapi3dcf3f8d277bc6936678b4332598045d-2"

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
