import requests # https://2.python-requests.org/en/master/
import config

# APIS
class api:
  def get(self, url):
    resp = requests.get(
      url,
      auth=(config.API_USERNAME, config.API_PASSWORD)
    )

    if resp.status_code != 200:
      print(resp.text)
      print(url)

    return resp.json()

class groups:
  groupUrl = 'https://api.planningcenteronline.com/groups/v2/groups'

  def getAll(self):
    return api().get('%s?per_page=100' % (self.groupUrl))
  def getMembers(self, groupId):
    return api().get('%s/%s/memberships' % (self.groupUrl, groupId))

class people:
  peopleUrl = 'https://api.planningcenteronline.com/people/v2/people'

  def getPerson(self, peopleId):
    return api().get('%s/%s' % (self.peopleUrl, peopleId))

# MODELS
class member:
  firstname = "david"
  lastname = "lozzi"

  def set(self, fname, lname):
    self.firstname = fname
    self.lastname = lname
    return self

  def fullname(self):
    return self.firstname + " " + self.lastname



groupsList = groups().getAll()

for group in groupsList["data"]:
  print(group["attributes"]["name"])
  members = groups().getMembers(group["id"])

  for member in members["data"]:
    # try:
    person = people().getPerson(member["attributes"]["account_center_identifier"])
    print("    %s %s %s" % (member["attributes"]["first_name"], member["attributes"]["last_name"], person["data"]["attributes"]["gender"]))
    # except:
    #   print("people errored for %s %s" % (member["attributes"]["first_name"], member["attributes"]["last_name"]))
    