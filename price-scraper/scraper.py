from selectorlib import Extractor, Formatter
import requests
import json

# Can be better formatter than .replace
def DeleteEuroSymbol(item):
    "Replace Euro symbol with empty string"
    for element in data:
        # print(data[element])
        if "\u00a0\u20ac" in data[element]:
            data[element] = data[element].replace("\u00a0\u20ac", "")
    return item

def ConvertToFloat(item):
    return float(item.replace(",","."))

def Desicion(data):
    # print(json.dumps(data, indent=True))

    if ConvertToFloat(data['OurOrDealPrice']) < data["DesiredPrice"]:
        data["DiscountInfo"] = "Price is smaller than DesiredPrice"
        return data
    # TODO May Calculate last value via variables
    elif type(data['LightningDeal']) is not list:
        data["DiscountInfo"]  = "There is LightningDeal"
    elif type(data['Voucher']) is not list:
        data["DiscountInfo"]  = "There is Voucher"
        return data
    return None

try:
    json_data_file = open('config/config.json')
    config_data = json.load(json_data_file)
    headers = config_data["headers"]
except Exception as e:
    print("No config/config.json file found")
    exit(1)

json_data_file = open('items_list.json')
list_data = json.load(json_data_file)
retval = []

for item in list_data['itemslist']:
    url = item["url"]
    desired_price = float(item["DesiredPrice"])

    # TODO Make this dynamic via url for different web sites
    selector_file = 'selectors/amazon_de.yml'

    # Create an Extractor by reading from the YAML file
    extractor_element = Extractor.from_yaml_file(selector_file)

    # Download the page using requests
    req = requests.get(url, headers=headers)

    # Pass the HTML of the page and create
    data = extractor_element.extract(req.text)
    data  = DeleteEuroSymbol(data)

    # Add link and desired price
    data["link"] = url
    data["DesiredPrice"] = desired_price

    desval = Desicion(data)

    if desval is not None:
        retval.append(desval)

if len(retval) > 0:
    print(json.dumps(retval, indent=True))
    exit(1)
