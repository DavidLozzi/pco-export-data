from api import api

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