import requests
import sys
import xml.etree.ElementTree as ET
from auth import ipmi_username, ipmi_pwd


def main(url):
    auth_form = {'name':ipmi_username, 'pwd':ipmi_pwd}
    event_log_form = {'SEL_INFO.XML': '(1,c0)'}

    ipmi_sesh = requests.Session()
    ipmi_sesh.post(f'http://{url}/cgi/login.cgi', data=auth_form)
    response = ipmi_sesh.post(f'http://{url}/cgi/ipmi.cgi', data=event_log_form)
    ipmi_events = ET.fromstring(response.text)
    events = []
    for SEL_INFO in ipmi_events:
        for SEL in SEL_INFO:
            events.append(SEL.attrib)

    # PCI SERR is shown when the 11th byte of the error string is 0x13
    # First entry in events is total number of events. Can skip
    for event in events[1:]:
        if event.get('SEL_RD')[20:22] == '13':
            print(f'Found PCI SERR at {event.get("TIME")}')

    return

if __name__ == "__main__":
    url = sys.argv[1]
    main(url)
    pass