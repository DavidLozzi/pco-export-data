from api import api

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