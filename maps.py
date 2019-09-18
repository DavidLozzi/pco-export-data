from api import api
import config

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