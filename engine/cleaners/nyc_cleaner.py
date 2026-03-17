'''
API Field Name: license_nbr	What it represents: Unique ID	Why we need it: To ensure we don't count the same business twice.
API Field Name: business_name	What it represents: Name	Why we need it: To identify the business.
API Field Name: industry	What it represents: Category	Why we need it: Crucial: To filter (e.g., "Restaurant" vs "Garage").
API Field Name: address_zip	What it represents: ZIP Code	Why we need it: The "Join Key" to link with Zillow and Census data.
API Field Name: address_borough	What it represents: Borough	Why we need it: For high-level dashboard filtering (Brooklyn, Queens, etc).
API Field Name: license_status	What it represents: Status	Why we need it: To filter for "Active" businesses only.
API Field Name: license_creation_date What it represents: Start Date	Why we need it: To calculate the "New Business Growth" over time.
API Field Name: latitude / longitude What it represents: Coordinates	Why we need it: For your JS Map.
'''

import pandas as pd
from sodapy import Socrata
