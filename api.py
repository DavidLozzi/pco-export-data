import requests
import config

class api:
  def get(self, url):
    print("        " + url)
    resp = requests.get(
      url,
      auth=(config.API_USERNAME, config.API_PASSWORD)
    )

    if resp.status_code != 200:
      print(resp.text)
      print(url)

    return resp.json()