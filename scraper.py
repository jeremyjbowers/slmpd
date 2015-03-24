#!/usr/bin/env python

import glob
import json

import requests
from bs4 import BeautifulSoup

# Set some global variables.
base_url = 'http://slmpd.org/CrimeReport.aspx'
download_links = []

# This is the basic POST data you need to submit the form.
data = {}
data['__VIEWSTATE'] = '/wEPDwUKMTkwOTUyMDQ0OQ9kFgICAw9kFgICAQ88KwARAwAPFgQeC18hRGF0YUJvdW5kZx4LXyFJdGVtQ291bnQCVmQBEBYAFgAWAAwUKwAAFgJmD2QWIgIBD2QWCmYPDxYCHgRUZXh0BR9DcmltZSBSZXBvcnRzIGZvciBGZWJydWFyeSAyMDE1ZGQCAQ9kFgICAQ8PFgQfAgUQRmVicnVhcnkyMDE1LlBERh4PQ29tbWFuZEFyZ3VtZW50BUxDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcRmVicnVhcnkyMDE1LlBERjtGZWJydWFyeTIwMTUuUERGZGQCAg8PFgIfAgUFMTEgS0JkZAIDD2QWAgIBDw8WBB8CBRBGZWJydWFyeTIwMTUuQ1NWHwMFTEM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxGZWJydWFyeTIwMTUuQ1NWO0ZlYnJ1YXJ5MjAxNS5DU1ZkZAIEDw8WAh8CBQY0NjYgS0JkZAICD2QWCmYPDxYCHwIFHkNyaW1lIFJlcG9ydHMgZm9yIEphbnVhcnkgMjAxNWRkAgEPZBYCAgEPDxYEHwIFD0phbnVhcnkyMDE1LlBERh8DBUpDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcSmFudWFyeTIwMTUuUERGO0phbnVhcnkyMDE1LlBERmRkAgIPDxYCHwIFBTExIEtCZGQCAw9kFgICAQ8PFgQfAgUPSmFudWFyeTIwMTUuQ1NWHwMFSkM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxKYW51YXJ5MjAxNS5DU1Y7SmFudWFyeTIwMTUuQ1NWZGQCBA8PFgIfAgUGNTc5IEtCZGQCAw9kFgpmDw8WAh8CBR9DcmltZSBSZXBvcnRzIGZvciBEZWNlbWJlciAyMDE0ZGQCAQ9kFgICAQ8PFgQfAgUQRGVjZW1iZXIyMDE0LlBERh8DBUxDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcRGVjZW1iZXIyMDE0LlBERjtEZWNlbWJlcjIwMTQuUERGZGQCAg8PFgIfAgUFMTEgS0JkZAIDD2QWAgIBDw8WBB8CBRBEZWNlbWJlcjIwMTQuQ1NWHwMFTEM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxEZWNlbWJlcjIwMTQuQ1NWO0RlY2VtYmVyMjAxNC5DU1ZkZAIEDw8WAh8CBQY2MDUgS0JkZAIED2QWCmYPDxYCHwIFH0NyaW1lIFJlcG9ydHMgZm9yIE5vdmVtYmVyIDIwMTRkZAIBD2QWAgIBDw8WBB8CBRBOb3ZlbWJlcjIwMTQuUERGHwMFTEM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxOb3ZlbWJlcjIwMTQuUERGO05vdmVtYmVyMjAxNC5QREZkZAICDw8WAh8CBQUxMSBLQmRkAgMPZBYCAgEPDxYEHwIFEE5vdmVtYmVyMjAxNC5DU1YfAwVMQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXE5vdmVtYmVyMjAxNC5DU1Y7Tm92ZW1iZXIyMDE0LkNTVmRkAgQPDxYCHwIFBjU3OSBLQmRkAgUPZBYKZg8PFgIfAgUeQ3JpbWUgUmVwb3J0cyBmb3IgT2N0b2JlciAyMDE0ZGQCAQ9kFgICAQ8PFgQfAgUPT2N0b2JlcjIwMTQuUERGHwMFSkM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxPY3RvYmVyMjAxNC5QREY7T2N0b2JlcjIwMTQuUERGZGQCAg8PFgIfAgUFMTEgS0JkZAIDD2QWAgIBDw8WBB8CBQ9PY3RvYmVyMjAxNC5DU1YfAwVKQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXE9jdG9iZXIyMDE0LkNTVjtPY3RvYmVyMjAxNC5DU1ZkZAIEDw8WAh8CBQY2MjMgS0JkZAIGD2QWCmYPDxYCHwIFIENyaW1lIFJlcG9ydHMgZm9yIFNlcHRlbWJlciAyMDE0ZGQCAQ9kFgICAQ8PFgQfAgURU2VwdGVtYmVyMjAxNC5QREYfAwVOQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXFNlcHRlbWJlcjIwMTQuUERGO1NlcHRlbWJlcjIwMTQuUERGZGQCAg8PFgIfAgUENyBLQmRkAgMPZBYCAgEPDxYEHwIFEVNlcHRlbWJlcjIwMTQuQ1NWHwMFTkM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxTZXB0ZW1iZXIyMDE0LkNTVjtTZXB0ZW1iZXIyMDE0LkNTVmRkAgQPDxYCHwIFBjY1OCBLQmRkAgcPZBYKZg8PFgIfAgUdQ3JpbWUgUmVwb3J0cyBmb3IgQXVndXN0IDIwMTRkZAIBD2QWAgIBDw8WBB8CBQ5BdWd1c3QyMDE0LlBERh8DBUhDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcQXVndXN0MjAxNC5QREY7QXVndXN0MjAxNC5QREZkZAICDw8WAh8CBQQ3IEtCZGQCAw9kFgICAQ8PFgQfAgUOQXVndXN0MjAxNC5DU1YfAwVIQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXEF1Z3VzdDIwMTQuQ1NWO0F1Z3VzdDIwMTQuQ1NWZGQCBA8PFgIfAgUGNjM2IEtCZGQCCA9kFgpmDw8WAh8CBRtDcmltZSBSZXBvcnRzIGZvciBKdWx5IDIwMTRkZAIBD2QWAgIBDw8WBB8CBQxKdWx5MjAxNC5QREYfAwVEQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXEp1bHkyMDE0LlBERjtKdWx5MjAxNC5QREZkZAICDw8WAh8CBQQ3IEtCZGQCAw9kFgICAQ8PFgQfAgUMSnVseTIwMTQuQ1NWHwMFREM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxKdWx5MjAxNC5DU1Y7SnVseTIwMTQuQ1NWZGQCBA8PFgIfAgUGNjQyIEtCZGQCCQ9kFgpmDw8WAh8CBRtDcmltZSBSZXBvcnRzIGZvciBKdW5lIDIwMTRkZAIBD2QWAgIBDw8WBB8CBQxKdW5lMjAxNC5QREYfAwVEQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXEp1bmUyMDE0LlBERjtKdW5lMjAxNC5QREZkZAICDw8WAh8CBQQ3IEtCZGQCAw9kFgICAQ8PFgQfAgUMSnVuZTIwMTQuQ1NWHwMFREM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxKdW5lMjAxNC5DU1Y7SnVuZTIwMTQuQ1NWZGQCBA8PFgIfAgUGNjA5IEtCZGQCCg9kFgpmDw8WAh8CBRpDcmltZSBSZXBvcnRzIGZvciBNYXkgMjAxNGRkAgEPZBYCAgEPDxYEHwIFC01heTIwMTQuUERGHwMFQkM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxNYXkyMDE0LlBERjtNYXkyMDE0LlBERmRkAgIPDxYCHwIFBDcgS0JkZAIDD2QWAgIBDw8WBB8CBQtNYXkyMDE0LkNTVh8DBUJDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcTWF5MjAxNC5DU1Y7TWF5MjAxNC5DU1ZkZAIEDw8WAh8CBQY2MTQgS0JkZAILD2QWCmYPDxYCHwIFHENyaW1lIFJlcG9ydHMgZm9yIEFwcmlsIDIwMTRkZAIBD2QWAgIBDw8WBB8CBQ1BcHJpbDIwMTQuUERGHwMFRkM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxBcHJpbDIwMTQuUERGO0FwcmlsMjAxNC5QREZkZAICDw8WAh8CBQQ3IEtCZGQCAw9kFgICAQ8PFgQfAgUNQXByaWwyMDE0LkNTVh8DBUZDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcQXByaWwyMDE0LkNTVjtBcHJpbDIwMTQuQ1NWZGQCBA8PFgIfAgUGNTc5IEtCZGQCDA9kFgpmDw8WAh8CBRxDcmltZSBSZXBvcnRzIGZvciBNYXJjaCAyMDE0ZGQCAQ9kFgICAQ8PFgQfAgUNTWFyY2gyMDE0LlBERh8DBUZDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcTWFyY2gyMDE0LlBERjtNYXJjaDIwMTQuUERGZGQCAg8PFgIfAgUFMTEgS0JkZAIDD2QWAgIBDw8WBB8CBQ1NYXJjaDIwMTQuQ1NWHwMFRkM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxNYXJjaDIwMTQuQ1NWO01hcmNoMjAxNC5DU1ZkZAIEDw8WAh8CBQY1MzMgS0JkZAIND2QWCmYPDxYCHwIFH0NyaW1lIFJlcG9ydHMgZm9yIEZlYnJ1YXJ5IDIwMTRkZAIBD2QWAgIBDw8WBB8CBRBGZWJydWFyeTIwMTQuUERGHwMFTEM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxGZWJydWFyeTIwMTQuUERGO0ZlYnJ1YXJ5MjAxNC5QREZkZAICDw8WAh8CBQUxMSBLQmRkAgMPZBYCAgEPDxYEHwIFEEZlYnJ1YXJ5MjAxNC5DU1YfAwVMQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXEZlYnJ1YXJ5MjAxNC5DU1Y7RmVicnVhcnkyMDE0LkNTVmRkAgQPDxYCHwIFBjQyMyBLQmRkAg4PZBYKZg8PFgIfAgUeQ3JpbWUgUmVwb3J0cyBmb3IgSmFudWFyeSAyMDE0ZGQCAQ9kFgICAQ8PFgQfAgUPSmFudWFyeTIwMTQuUERGHwMFSkM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxKYW51YXJ5MjAxNC5QREY7SmFudWFyeTIwMTQuUERGZGQCAg8PFgIfAgUFMTEgS0JkZAIDD2QWAgIBDw8WBB8CBQ9KYW51YXJ5MjAxNC5DU1YfAwVKQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXEphbnVhcnkyMDE0LkNTVjtKYW51YXJ5MjAxNC5DU1ZkZAIEDw8WAh8CBQY0ODIgS0JkZAIPD2QWCmYPDxYCHwIFH0NyaW1lIFJlcG9ydHMgZm9yIERlY2VtYmVyIDIwMTNkZAIBD2QWAgIBDw8WBB8CBRBEZWNlbWJlcjIwMTMuUERGHwMFTEM6XEluZXRwdWJcdmhvc3RzXHNsbXBkLm5ldFxodHRwZG9jc1xDcmltZVxEZWNlbWJlcjIwMTMuUERGO0RlY2VtYmVyMjAxMy5QREZkZAICDw8WAh8CBQUxMSBLQmRkAgMPZBYCAgEPDxYEHwIFEERlY2VtYmVyMjAxMy5DU1YfAwVMQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXERlY2VtYmVyMjAxMy5DU1Y7RGVjZW1iZXIyMDEzLkNTVmRkAgQPDxYCHwIFBjUyNyBLQmRkAhAPZBYKZg8PFgIfAgUfQ3JpbWUgUmVwb3J0cyBmb3IgTm92ZW1iZXIgMjAxM2RkAgEPZBYCAgEPDxYEHwIFEE5vdmVtYmVyMjAxMy5QREYfAwVMQzpcSW5ldHB1Ylx2aG9zdHNcc2xtcGQubmV0XGh0dHBkb2NzXENyaW1lXE5vdmVtYmVyMjAxMy5QREY7Tm92ZW1iZXIyMDEzLlBERmRkAgIPDxYCHwIFBTExIEtCZGQCAw9kFgICAQ8PFgQfAgUQTm92ZW1iZXIyMDEzLkNTVh8DBUxDOlxJbmV0cHViXHZob3N0c1xzbG1wZC5uZXRcaHR0cGRvY3NcQ3JpbWVcTm92ZW1iZXIyMDEzLkNTVjtOb3ZlbWJlcjIwMTMuQ1NWZGQCBA8PFgIfAgUGNTYwIEtCZGQCEQ8PFgIeB1Zpc2libGVoZGQYAQUJR3JpZFZpZXcxDzwrAAwBCAIGZHGheHCewk15ktGAYMSfvrVb8WOmnRL/bnNE8G14A9QS'
data['__VIEWSTATEGENERATOR'] = '930F6B58'
data['__EVENTVALIDATION'] = '/wEdACb6dyMLZjm2MmoskdM08p/rJKBoRMF7DzN7cJuX0OcM/9g3GBBahQM2VFN5WWYKIeYG0vS5nf1UhYpg8OBW1qfSw5E9kW2omrscXrUUbkpAIqb9EDUBKM7U5Cx/kDzLavDZjjmiXL5gye807rlodShWXgeFe07Dx3dz0sy88AT+mMoLmzdRLm9jlNLGjNlvCGi+Be1B7ZZnNPeRuyhxObDXt4JZ+lEm3YmxezchXxsF5/y92D3n385MWhs10uDRtz/Pi4knwf5TXLuV+S5lOM5MuOw4N0eW+rwWgwzSoV8C4HC0RSk2hO7F+P6zfb88943pcME7xokmKGxEnrsu2gR02stwYCRsUKSvGkCWwNFxUZB6oM2f8OPew5ouXc7RhkQfYI1NtCdCXskhmPF9pAfHoQQRt40XZnYpM2c7Mi/0lYdi88QRS4IXmTa3Ll5vVI94iioMtoc+i3mYmNgBgiYul5xALWPfjI044aBZJLLlaN+VGp8S6Ctpqnhc5JJbUQJ0mI4b5H9O3MXNBCQyUfTVFEDvtuWnyyiIYLZRFcDs/dgGOItDrtKkrBQ16l3WWxZF4tX28m6hK9FfPUCmHNlQ1corZnlLQ5m/z+Fa1MQQSdZXbbc1YCwSp595TFk5X1t8I0BKLbYlleG+urUhR5SIJndEbe0XD3euvCI0TEPUafjrvFbCpBPwOUQRHx3haOU9bR5U9tbpdAn4Nxxa5EhUxlVaYX16GZjbv5sbbSkEMW9pPXo3SeZbJobOXh9FFN6i0nJp7ofvso6QrIWORKrhwlUrSSDm2sR055aaggQfv4ARHp1AKE4oEhOK0fbv14bLXnbvLhjeLUMG7ELx7gMG'

def main():
    """
    Our function names are a table of contents for what we want to do.
    """
    get_download_links()
    download_pdfs()

def parse_links(page_content):
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
        parse_links(r.content)

    # Loop over the rest of the pages. Currently: 2-6
    for page_number in range(2, 7):

        print "Getting links from page %s." % page_number

        # Set the POST data dictionary with the bits we need to page through.
        data['__EVENTTARGET'] = 'GridView1'
        data['__EVENTARGUMENT'] = 'Page$%s' % page_number

        # Make a POST request for this page.
        r = requests.post(base_url, data=data)

        if int(r.status_code) == 200:
            parse_links(r.content)

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
