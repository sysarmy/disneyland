from icmplib import ping
import json
import logging
import requests
from requests.structures import CaseInsensitiveDict


def run():
    response = {"id": "xxx", "isp": "NOMBRE DEL ISP", 'measurements': []}
    hosts = ['fr-sxb-as8839.anchors.atlas.ripe.net', 'us-mia-as15133.anchors.atlas.ripe.net', 'us-qas-as15169.anchors.atlas.ripe.net', 'br-sao-as16509.anchors.atlas.ripe.net', 'au-syd-as16509.anchors.atlas.ripe.net', 'us-mia-as15133.anchors.atlas.ripe.net', 'us-qas-as15169.anchors.atlas.ripe.net','fr-lio-as41405.anchors.atlas.ripe.net']
    # tirarle ping a 3 anchors US,EU,APAC
    # buildear el json
    for h in hosts:
        host = ping(h,count=3,privileged=True)
        #print(f"{host.min_rtt} {host.max_rtt} {host.jitter} {host.packet_loss}")
        response['measurements'].append({'anchor': h.split(".")[0], 'min_rtt': host.min_rtt, 'max_rtt': host.max_rtt, 'jitter': host.jitter, 'packet_loss': host.packet_loss})

    print(json.dumps(response))

    url = "https://xxxxxxxxxxx/api/v1/quartz"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["api_key"] = "xxxxxxxxxxxxxxxx"

    resp = requests.post(url, headers=headers, data=json.dumps(response))

    print(resp.status_code)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(format='%(message)s',filename='broken-glass.log', level=logging.DEBUG)
    run()