import urllib2
import time
import xml.etree.ElementTree as ET
import os

api_key = os.environ['API_KEY']

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct",
          "nov", "dec"]

url_template = ("https://ukclimateprojections-ui.metoffice.gov.uk/wps/Execute?"
"Request=Execute&"
"Identifier=LS1_Plume_01&Format=text/xml&Inform=true&Store=false&"
"Status=false&DataInputs=Area=point|245333.38|778933.24;Baseline=b8100;"
"Collection=land-prob;ColourMode=c;DataFormat=csv;FontSize=m;"
"ImageFormat=png;ImageSize=1200;LegendPosition=7;PlotType=PDF_PLOT;"
"Scenario=sres-a1b;TemporalAverage={{month}};TimeSlice=2050-2069;"
"TimeSliceDuration=20y;Variable=tasAnom;"
"&ApiKey={{api_key}}")


def save_outputs(url, target_dir):
    response = urllib2.urlopen(url)

    # Open local file for writing
    target = os.path.join(target_dir, os.path.basename(url))
    with open(target, "wb") as local_file:
        local_file.write(response.read())

    print("Wrote output to: {}".format(target))


def get_zip_file_url(xml):
    root = ET.fromstring(xml)
    file_url_element = "{http://www.opengeospatial.net/wps}FileURL"

    for file_url in root.iter(file_url_element):
        if file_url.text.endswith('.zip'):
            return file_url.text

    raise Exception('Cannot locate zip file url in "<FileURL>" tag')


def get_status_url(xml_doc):
    root = ET.fromstring(xml_doc)
    status_url = root.get("statusLocation", None)

    if not status_url:
        raise Exception("Could not determine the status URL.")

    return status_url


def _poll_status_url(status_url):
    # Polls until completion - unless exited

    while 1:
        time.sleep(5)
        response = urllib2.urlopen(status_url)
        xml_doc = response.read()

        if _check_status(xml_doc):
            return xml_doc



def request_all_months(output_dir):
    for month in months:
        url = url_template.format(month=month, api_key=api_key)
        response = urllib2.urlopen(url)
        xml_doc = response.read()

        print("Extract status URL from XML response")
        status_url = get_status_url(xml_doc) 
   
        # Poll Status URL until job completes


        print("Sleeping for 10 seconds to overcome usage limits")
        print("(might need to adjust this)...")
        time.sleep(10)

        # Extract the URL for the output zip file
        zip_url = get_zip_file_url(xml_doc)

        # Append API KEY to zip URL to download using API
        zip_url += "?ApiKey={{api_key}}"
        save_outputs(zip_url, output_dir)


request_all_months("/tmp")

