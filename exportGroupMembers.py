import requests
from geopy import distance
import config
import time

# APIS
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

class groups:
  groupUrl = 'https://api.planningcenteronline.com/groups/v2/groups'
  groupId = ""
  locationUrl = ""

  def __init__(self, grpId):
    self.groupId = grpId
  def getAll(self):
    return api().get('%s?per_page=100' % (self.groupUrl))
  def getDetails(self):
    resp = api().get('%s/%s' % (self.groupUrl, self.groupId))
    self.locationUrl = resp["data"]["links"]["location"]
    return resp
  def getMembers(self):
    return api().get('%s/%s/memberships' % (self.groupUrl, self.groupId))
  def getLocation(self):
    if self.locationUrl == None:
      return None
    else:
      return api().get(self.locationUrl)

class people:
  peopleUrl = 'https://api.planningcenteronline.com/people/v2/people'
  peopleId = ''
  maritalUrl = ''
  addressUrl = ''

  def __init__(self, peepId):
    self.peopleId = peepId
  def getPerson(self):
    resp = api().get('%s/%s' % (self.peopleUrl, self.peopleId))
    self.maritalUrl = resp["data"]["links"]["marital_status"]
    self.addressUrl = resp["data"]["links"]["addresses"]
    return resp
  def getMaritalStatus(self):
    if self.maritalUrl == None:
      return None
    else:
      return api().get(self.maritalUrl)
  def getAddress(self):
    if self.addressUrl == None:
      return None
    else :
      return api().get(self.addressUrl)

class maps:
  mapUrl = 'https://maps.googleapis.com/maps/api/geocode/json?key=%s' % (config.GOOGLE_APIKEY)
  address = ''
  addresses = {}

  def __init__(self, address):
    self.address = address
  def getLocation(self):
    if self.address not in self.addresses:
      resp = api().get('%s&address=%s' % (self.mapUrl, self.address))
      self.addresses[self.address] = resp["results"][0]["geometry"]["location"]# expects { "lat": 00.000, "lng": 00.000 }
    
    return self.addresses[self.address]


outputFile = open("groupsExport.csv", "w+")
# add new columns to csvHeader AND update the number of columns in csvPlaceholder
csvHeader = "First Name, Last Name, Gender, Birthdate, City, State, Zip, Location Long, Location Lat, Distance to Group, Marital Status, Membership, Status, Person Record Updated, Person Record Created, Joined Group At, Role, Group, Group Location, Group Long, Group Lat\r\n"
csvPlaceholder = ("\"%s\"," * 21) + "\r\n"
outputFile.write(csvHeader)

groupsList = groups('').getAll()

for grp in groupsList["data"]:
  time.sleep(.4) # slowing down API calls to not exceed rates of 100 in 20s
  print(grp["attributes"]["name"])
  groupObj = groups(grp["id"])
  groupDetail = groupObj.getDetails()
  members = groupObj.getMembers()
  grpLocation = groupObj.getLocation()
  if grpLocation != None:
    groupAddress = grpLocation["data"]["attributes"]["full_formatted_address"].replace("\n", ", ")
    groupLong = grpLocation["data"]["attributes"]["longitude"]
    groupLat = grpLocation["data"]["attributes"]["latitude"]

  for member in members["data"]:
    # try:
      print("    %s %s" % (member["attributes"]["first_name"], member["attributes"]["last_name"]))
      time.sleep(.2) # a little more slow down
      personObj = people(member["attributes"]["account_center_identifier"])
      person = personObj.getPerson()
      maritalStatus = personObj.getMaritalStatus()
      addresses = personObj.getAddress()
      if addresses != None and len(addresses["data"]) > 0:
        address = addresses["data"][0]
        mapApi = maps("%s %s %s" % (address["attributes"]["city"] if address["attributes"]["city"] != None else '',
          address["attributes"]["state"] if address["attributes"]["state"] != None else '',
          address["attributes"]["zip"] if address["attributes"]["zip"] != None else ''))
        mapLocation = mapApi.getLocation()
        memberDistance = distance.distance((groupLat, groupLong),(mapLocation["lat"], mapLocation["lng"])).miles

      outputFile.write(csvPlaceholder % (
        person["data"]["attributes"]["first_name"],
        person["data"]["attributes"]["last_name"],
        person["data"]["attributes"]["gender"],
        person["data"]["attributes"]["birthdate"],
        address["attributes"]["city"] if address["attributes"]["city"] != None else '',
        address["attributes"]["state"] if address["attributes"]["state"] != None else '',
        address["attributes"]["zip"] if address["attributes"]["zip"] != None else '',
        mapLocation["lng"],
        mapLocation["lat"],
        memberDistance,
        maritalStatus["data"]["attributes"]["value"] if maritalStatus != None else '',
        person["data"]["attributes"]["membership"],
        person["data"]["attributes"]["status"],
        person["data"]["attributes"]["updated_at"],
        person["data"]["attributes"]["created_at"],
        member["attributes"]["joined_at"],
        member["attributes"]["role"],
        groupDetail["data"]["attributes"]["name"],
        groupAddress,
        groupLong,
        groupLat
        ))
    # except:
    #   print("errored for %s %s" % (member["attributes"]["first_name"], member["attributes"]["last_name"]))

outputFile.close()