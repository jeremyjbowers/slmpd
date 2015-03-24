#!/usr/bin/env python

import glob
import json

from bs4 import BeautifulSoup
import requests

# Set some global variables.
base_url = 'http://slmpd.org/CrimeReport.aspx'
download_links = []

# This is the basic POST data you need to submit the form.
data = {}

def main():
    """
    Our function names are a table of contents for what we want to do.
    """
    get_download_links()
    download_pdfs()

def _set_keys(page_content):
    soup = BeautifulSoup(page_content)
    keys = soup.select('input[type="hidden"]')

    for key in keys:
        data[key['name']] = key['value']

def _parse_links(page_content):
    """
    This is a utility function for parsing a page and getting links.
    """
    # Parse the page with BeautifulSoup.
    soup = BeautifulSoup(page_content)
    possible_links = soup.select('a')

    for possible_link in possible_links:

        # If the link text contains PDF or CSV, it's possibly a target.
        if '.pdf' or '.csv' in possible_link.text.strip().lower():

            # Ignore one kind of link that is incorrect.
            if possible_link['href'].split("javascript:__doPostBack('")[1].split("',")[0] != "GridView1":

                # For each link, get the filename and the download ID we need.
                link_dict = {}
                link_dict['filename'] = possible_link.text.strip()
                link_dict['id'] = possible_link['href'].split("javascript:__doPostBack('")[1].split("',")[0]

                # Add this little dictionary to our list of links to download.
                download_links.append(link_dict)

def get_download_links():
    """
    Step 1: Get all of the links to download.
    """

    print "Getting links from page 1."

    # Get the first page. It wants a GET request and doesn't like the POST
    # format the other pages use.
    r = requests.get(base_url)

    if int(r.status_code) == 200:
        _set_keys(r.content)
        _parse_links(r.content)

    # Loop over the rest of the pages. Currently: 2-6
    for page_number in range(2, 7):

        print "Getting links from page %s." % page_number

        # Set the POST data dictionary with the bits we need to page through.
        data['__EVENTTARGET'] = 'GridView1'
        data['__EVENTARGUMENT'] = 'Page$%s' % page_number

        # Make a POST request for this page.
        r = requests.post(base_url, data=data)

        if int(r.status_code) == 200:
            _parse_links(r.content)

    # Convert our list of links to JSON.
    payload = json.dumps(download_links)

    # Write our links to a file in case the site is unavailable.
    with open('download_links.json', 'w') as writefile:
        writefile.write(payload)

def download_pdfs():
    """
    Step 2: Download the files.
    """

    # Open our list of links.
    with open('download_links.json', 'r') as readfile:
        download_links = list(json.loads(readfile.read()))

    # Loop over the links.
    for link in download_links:

        # Check to see if we have this file already. If not, download it.
        if len(glob.glob('data/%s' % link['filename'])) == 0:

            print "Downloading file %s." % link['filename']

            # Modify the POST data dictionary to make this file work.
            data['__EVENTTARGET'] = '%s' % link['id']
            data['__EVENTARGUMENT'] = ''

            # Make a request for the file.
            r = requests.post(base_url, data=data)

            if int(r.status_code) == 200:

                # If it worked, write the data to a file in the data/ directory.
                with open('data/%s' % link['filename'], 'w') as writefile:
                    writefile.write(r.content)

if __name__ == "__main__":
    # This function executes when you do "./scraper.py" on the command line.
    main()
