import requests
import re
import string
import time
from win10toast import ToastNotifier

refresh_time = 30
url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93311&maxBedrooms=1&maxPrice=800&minPrice=200&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=houseShare%2Cretirement&furnishTypes=&keywords='
num_checks_before_update = 10


def get_properties():
    # Get webpage
    r = requests.get(url)
    html = r.text

    # Remove featured property
    featured = re.search('propertyCard--featured', html)
    if featured:
        html = html[html.find('<div id="property', featured.end()):]

    # Get string indices
    property_strings = [m.end() for m in re.finditer('<meta itemprop="streetAddress" content="', html)]
    properties = []

    # Make list of property names
    for p in property_strings:
        prop_name = html[p:html.find('"', p)]
        if prop_name:
            properties.append(prop_name)
    return properties


def main():
    # Set up list and notifier
    properties = []
    toast = ToastNotifier()

    checks = 0

    while True:
        # Get all properties
        old_properties = properties
        try:
            properties = get_properties()
        except:
            print("Couldn't connect to site")
            time.sleep(refresh_time)
            continue

        # Output after doing specified number of checks
        checks = checks + 1
        if checks == num_checks_before_update:
            print("Checked " + str(checks) + " times")
            checks = 0

        # Notify of new properties
        if len(properties) > len(old_properties) > 0:
            new_properties = "\n".join(properties[len(old_properties):])
            print("New properties:\n" + new_properties)
            toast.show_toast("New apartments", new_properties, duration=refresh_time*2)      
        else:
            # Wait until next refresh
            time.sleep(refresh_time)


if __name__ == "__main__":
    main()
