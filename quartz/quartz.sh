#!/usr/bin/bash

hosts=( fr-sxb-as8839.anchors.atlas.ripe.net us-mia-as15133.anchors.atlas.ripe.net us-qas-as15169.anchors.atlas.ripe.net br-sao-as16509.anchors.atlas.ripe.net au-syd-as16509.anchors.atlas.ripe.net us-mia-as15133.anchors.atlas.ripe.net us-qas-as15169.anchors.atlas.ripe.net fr-lio-as41405.anchors.atlas.ripe.net)
#TODO #105 agregar delay random max 2 min

url="http://localhost:1500"
#hosts=( fr-sxb-as8839.anchors.atlas.ripe.net us-mia-as15133.anchors.atlas.ripe.net)
api_key="xxxxxxxxxxxxxxxx"
isp="Fibercorp"
id="nss01"

jsondata="{\"id\": \"$id\", \"isp\": \"$isp\", \"measurements\": []}"

for host in "${hosts[@]}"; do

    read anchor min_rtt avg_rtt max_rtt loss jitter <<< $(ping -c 2 $host | awk '
        /^PING / {h=$2}
        /packet loss/ {pl=$6}
        /min\/avg\/max\/mdev/ {
                split($4,a,"/")
		printf("%s %s %s %s %s %s", h, a[1], a[2], a[3], pl, a[4] )
        }
    ')
    loss=${loss//%/}
    anchor="${anchor%%.*}"
    measure="{ \"anchor\" : \"$anchor\", \"min_rtt\" : \"$min_rtt\", \"max_rtt\" : \"$max_rtt\", \"jitter\" : \"$jitter\", \"packet_loss\" : \"$loss\" }"
    jsondata=$(echo $jsondata | jq --argjson new "$measure" '.measurements += [$new]')
done

echo $jsondata

#curl -X POST $url  -H "Accept: application/json" -H "Content-Type: application/json" -H $api_key -d "$jsondata"
