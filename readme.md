# PCO Group Member Exports Overview

The goal for this project is to easily export members of all active groups to perform some analysis and reporting on the data.

This python script:
1. Gets all active groups
2. Gets the members for each group
3. Gets the person data for each member
4. Gets the geolocation of the person (using Google APIs)
5. Performs a distance calculation for the members in the group
6. Exports it all to a CSV

The CSV will include the following columns:
 * First Name ![PCO People][people]
 * Last Name ![PCO People][people]
 * Gender ![PCO People][people]
 * Birthdate ![PCO People][people]
 * City ![PCO People][people]
 * State ![PCO People][people]
 * Zip ![PCO People][people]
 * Location Long ![Google Maps][maps]
 * Location Lat ![Google Maps][maps]
 * Distance to Group
 * Marital Status ![PCO People][people]
 * Membership ![PCO People][people]
 * Status ![PCO People][people]
 * Person Record Updated ![PCO People][people]
 * Person Record Created ![PCO People][people]
 * Joined Group At ![PCO People][group]
 * Role ![PCO People][group]
 * Group ![PCO People][group]
 * Group Location ![PCO People][group]
 * Group Long ![PCO People][group]
 * Group Lat ![PCO People][group]

[people]: images/people.png "PCO People"
[group]: images/groups.png "PCO Groups"
[maps]: images/maps.png "Google Maps"

# Setup

## Install Libraries

Before we begin, you'll need Python installed, obviously ;)

Install the following libraries:

```
pip install requests
pip install geopy
```

Learn more about [requests](https://2.python-requests.org/en/master/) and [geopy](https://geopy.readthedocs.io/en/stable/#module-geopy.distance).

## Setup Configuration

You have to create your own `config.py` file to store your API keys. Don't worry, this file is not included in the repo. Copy and paste the following into your config file:

```
API_USERNAME = 'specify your user name'
API_PASSWORD = 'specify your password'
GOOGLE_APIKEY = 'specify your Google API key'
```

Learn how to obtain a [Google API Key](https://developers.google.com/maps/documentation/geocoding/get-api-key).

_**NOTE** The config.py file is ignored by git._

# Using the Script

Simply run the `exportGroupMembers.py`

```
python exportGroupMembers.py
```

As it runs, it'll share each group name and member name in the console, along with each API call being made, just for reference.

This script will export the contents to `groupsExport.csv`. This file is not included in the git repo.