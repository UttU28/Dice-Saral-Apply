import requests

TOKEN = "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"
OWNER = "UttU28"
REPO = "updateSites"
WORKFLOW_FILE_NAME = "update_index_html.yml"  # Change this to the actual workflow file name

def trigger_workflow(workflow_file_name, parameter1, parameter2):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {TOKEN}",
    }

    data = {
        "ref": "main",  # Specify the branch name if needed
        "inputs": {
            'parameter1': parameter1,
            'parameter2': parameter2
        }
    }

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{workflow_file_name}/dispatches"
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 204:
        print("Workflow triggered successfully.")
    else:
        print(f"Failed to trigger workflow: {response.status_code}")
        print(response.json())

trigger_workflow(WORKFLOW_FILE_NAME, "sdv", "sdv")
