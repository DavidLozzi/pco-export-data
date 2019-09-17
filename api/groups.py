import requests
import ...config

def getAll():
  groupsRequest = requests.get(
    'https://api.planningcenteronline.com/groups/v2/groups',
    auth=(API_USERNAME, API_PASSWORD)
  )

  if groupsRequest.status_code != 200:
    print(groupsRequest.text)

  return groupsRequest
