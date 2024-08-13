import os
import requests
import sys

TOKEN= str(sys.argv[1])
OWNER= "UttU28"
REPO= "updateSites"
Workflow_Name= "update_index_html"
parameter1= "sdv"
parameter2 = "sdv"

print( "the toke value is")
def trigger_workflow(Workflow_Name,parameter1,parameter2):

      headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {TOKEN}",
      }

      data = {
        "event_type": Workflow_Name,
        "client_payload": {
          'parameter1': parameter1,
          'parameter2': parameter2
        }
      }

      responseValue=requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",json=data,headers=headers)
      print(responseValue.content)

trigger_workflow(Workflow_Name,parameter1,parameter2)