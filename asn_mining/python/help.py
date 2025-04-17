country_asns_ripe = {
    "de": [
        "1",
        "2",
    ],
    "fr": [
        "5",
        "6",
        "7",
        "8",
    ],
    "us" : [
        "3",
        "4",
    ]
}



all_countries = dict()
for key, value in country_asns_ripe.items():
    all_countries[key] = 0
    for asn in value:
        all_countries[key] += 1
        
print(all_countries)

ripe_asn_info = {
    "7": {
        "country": "de",
    },
    "8": {
        "country": "de",
    },
    "9": {
        "country": "us",
    },
    "10": {
        "country": "us",
    },
    "11" : {
        "country": "us",
    },
    "12" : {
        "country": "fr",
    }
}

for asn, value in ripe_asn_info.items():
    if value['country'] not in all_countries.keys():
        all_countries[value['country']] = 1
    else:
        all_countries[value['country']] += 1

print({key: value for key, value in sorted(all_countries.items(), key=lambda item: item[1], reverse=True)})