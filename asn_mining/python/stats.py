import asn_mining
import requests
from resources import *
import os
from range_map import RangeMap
import csv
import json

def download(url, dest):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest, 'wb') as f:
            f.write(response.content)
    return os.path.abspath(dest)

def split_range(string):
    parts = string.split('-')
    if len(parts) == 1:
        return int(parts[0]), int(parts[0])
    else:
        return int(parts[0]), int(parts[1])

def extract_rir(string):
    return string.replace("Assigned by ", "")

print("Init IANA info...")
iana1 = download(IANA_16_BIT_URL, IANA_16_BIT_FILE)
iana2 = download(IANA_32_BIT_URL, IANA_32_BIT_FILE)
iana_range_map = RangeMap()
with open(iana1, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        range = split_range(row[0])
        iana_range_map.add_range(range[0], range[1], extract_rir(row[1]))
with open(iana2, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        range = split_range(row[0])
        iana_range_map.add_range(range[0], range[1], extract_rir(row[1]))

print("Downloading files...")
print("NRO delegated stats")
nro = download(NRO_DELEGATED_STATS_URL, NRO_DELEGATED_STATS_FILE)
print("APNIC delegated stats")
apnic = download(APNIC_STATS_URL, APNIC_STATS_FILE)
print("RIPE NCC delegated stats")
ripencc = download(RIPE_STATS_URL, RIPE_STATS_FILE)
print("AFRINIC delegated stats")
afrinic = download(AFRINIC_STATS_URL, AFRINIC_STATS_FILE)
print("LACNIC delegated stats")
lacnic = download(LACNIC_STATS_URL, LACNIC_STATS_FILE)
print("ARIN delegated stats")
arin = download(ARIN_STATS_URL, ARIN_STATS_FILE)

print("Analyzing files...")
print("NRO delegated stats")
nro_result = asn_mining.asns_nro(nro)
print("APNIC delegated stats")
apnic_result = asn_mining.asns(apnic)
print("RIPE NCC delegated stats")
ripencc_result = asn_mining.asns(ripencc)
print("AFRINIC delegated stats")
afrinic_result = asn_mining.asns(afrinic)
print("LACNIC delegated stats")
lacnic_result = asn_mining.asns(lacnic)
print("ARIN delegated stats")
arin_result = asn_mining.asns(arin)

print("Loading all country info from RIPE NCC STATS...")
countries = nro_result['country_map'].keys()

country_asns_ripe = dict()
for country in countries:
    print("Downloading country {} info...".format(country))
    resp = requests.get(RIPE_COUNTRY_RESOURCE_LIST_URL.format(country)).json()
    country_asns_ripe[country] = resp['data']['resources']['asn']
    
with open("country_asns_ripe.json", 'w') as f:
    json.dump({key: value for key, value in sorted(country_asns_ripe.items(), key=lambda item: int(item[1]), reverse=True)}, f, indent=4)

print("Downloading BGP data...")
bgp = download(BGP_URL, BGP_DATA_FILE)
print("Analyzing BGP data...")
bgp_result = asn_mining.bgp(bgp)
print("Comparing results...")
nro_result_keys = nro_result['map'].keys()
arin_result_keys = arin_result['map'].keys()
ripencc_result_keys = ripencc_result['map'].keys()
apnic_result_keys = apnic_result['map'].keys()
afrinic_result_keys = afrinic_result['map'].keys()
lacnic_result_keys = lacnic_result['map'].keys()

dif_bgp_nro = bgp_result['all_asns'] - nro_result_keys
dif_nro_bgp = nro_result_keys - bgp_result['all_asns']

dif_bgp_arin_cache = bgp_result['all_asns'] - arin_result_keys
dif_bgp_arin = set()
for asn in dif_bgp_arin_cache:
    if iana_range_map.get_value(int(asn)) == "ARIN":
        dif_bgp_arin.add(asn)
        
with open("dif_bgp_arin.json", 'w') as f:
    json.dump(sorted(dif_bgp_arin, key=lambda x: int(x)), f, indent=4)

dif_bgp_ripencc_cache = bgp_result['all_asns'] - ripencc_result_keys
dif_bgp_ripencc = set()
for asn in dif_bgp_ripencc_cache:
    if iana_range_map.get_value(int(asn)) == "RIPE NCC":
        dif_bgp_ripencc.add(asn)

with open("dif_bgp_ripencc.json", 'w') as f:
    json.dump(sorted(dif_bgp_ripencc, key=lambda x: int(x)), f, indent=4)

dif_bgp_apnic_cache = bgp_result['all_asns'] - apnic_result_keys
dif_bgp_apnic = set()
for asn in dif_bgp_apnic_cache:
    if iana_range_map.get_value(int(asn)) == "APNIC":
        dif_bgp_apnic.add(asn)

with open("dif_bgp_apnic.json", 'w') as f:
    json.dump(sorted(dif_bgp_apnic, key=lambda x: int(x)), f, indent=4)
    
dif_bgp_afrinic_cache = bgp_result['all_asns'] - afrinic_result_keys
dif_bgp_afrinic = set()
for asn in dif_bgp_afrinic_cache:
    if iana_range_map.get_value(int(asn)) == "AFRINIC":
        dif_bgp_afrinic.remove(asn)
        
with open("dif_bgp_afrinic.json", 'w') as f:
    json.dump(sorted(dif_bgp_afrinic, key=lambda x: int(x)), f, indent=4)

dif_bgp_lacnic_cache = bgp_result['all_asns'] - lacnic_result_keys
dif_bgp_lacnic = set()
for asn in dif_bgp_lacnic_cache:
    if iana_range_map.get_value(int(asn)) == "LACNIC":
        dif_bgp_lacnic.add(asn)
        
with open("dif_bgp_lacnic.json", 'w') as f:
    json.dump(sorted(dif_bgp_lacnic, key=lambda x: int(x)), f, indent=4)


with open("dif_bgp_nro.json", 'w') as f:
    json.dump(sorted(dif_bgp_nro, key=lambda x: int(x)), f, indent=4)
with open("dif_nro_bgp.json", 'w') as f:
    json.dump(sorted(dif_nro_bgp, key=lambda x: int(x)), f, indent=4)

not_found_in_files = set()
for asn in dif_bgp_nro:
    responsible_rir = iana_range_map.get_value(int(asn))
    if responsible_rir == "RIPE NCC":
        if asn not in ripencc_result:
            not_found_in_files.add(asn)
    elif responsible_rir == "APNIC":
        if asn not in apnic_result:
            not_found_in_files.add(asn)
    elif responsible_rir == "ARIN":
        if asn not in arin_result:
            not_found_in_files.add(asn)
    elif responsible_rir == "AFRINIC":
        if asn not in afrinic_result:
            not_found_in_files.add(asn)
    elif responsible_rir == "LACNIC":
        if asn not in lacnic_result:
            not_found_in_files.add(asn)
    else:
        not_found_in_files.add(asn)
        
with open("not_found_in_files.json", 'w') as f:
    json.dump(sorted(not_found_in_files, key=lambda x: int(x)), f, indent=4)

inverted_ripe_stats_index = dict()
for country in country_asns_ripe:
    for asn in country_asns_ripe[country]:
        inverted_ripe_stats_index[asn] = {
            "country": country, 
            "rir": iana_range_map.get_value(int(asn))
        }
        
with open("inverted_ripe_stats_index.json", 'w') as f:
    json.dump({key: value for key, value in sorted(inverted_ripe_stats_index.items(), key=lambda item: int(item[0]))}, f, indent=4)
        
not_found_in_ripe_stats = set()
inverted_ripe_stats_index_keys = inverted_ripe_stats_index.keys()
for asn in dif_bgp_nro:
    if asn not in inverted_ripe_stats_index_keys:
        not_found_in_ripe_stats.add(asn)

with open("not_found_in_ripe_stats.json", 'w') as f:
    json.dump(sorted(not_found_in_ripe_stats, key=lambda x: int(x)), f, indent=4)
        
found_in_ripe_stats = {key: inverted_ripe_stats_index[key] for key in dif_bgp_nro if key not in not_found_in_ripe_stats}

with open("found_in_ripe_stats.json", 'w') as f:
    json.dump({key: value for key, value in sorted(found_in_ripe_stats.items(), key=lambda item: int(item[0]))}, f, indent=4)

print("Downloading ASN info from RIPE NCC STATS...")
ripe_asn_info = dict()
for asn in not_found_in_ripe_stats:
    resp = requests.get(RIPE_ASN_COUNTRY_INFO_URL.format(asn)).json()
    if(len(resp['data']['located_resources']) > 0):
        ripe_asn_info[asn] = {
            "country": resp['data']['located_resources'][0]['location'],
            "rir": iana_range_map.get_value(int(asn))
        }
    else:
        ripe_asn_info[asn] = {
            "country": "Unknown",
            "rir": iana_range_map.get_value(int(asn))
        }
        

with open("ripe_asn_info.json", 'w') as f:
    json.dump({key: value for key, value in sorted(ripe_asn_info.items(), key=lambda item: int(item[0]))}, f, indent=4)
    
print("Calculating all asns for alls countries...")
all_asns = dict()
for key, value in country_asns_ripe.items():
    for asn in value:
        all_asns[asn] = key
for asn, value in found_in_ripe_stats.items():
    all_asns[asn] = value['country']

with open("all_asns.json", 'w') as f:
    json.dump({key: value for key, value in sorted(all_asns.items(), key=lambda item: int(item[0]))}, f, indent=4)

all_countries = dict()
for key, value in country_asns_ripe.items():
    all_countries[key] = 0
    for asn in value:
        all_countries[key] += 1
for asn, value in ripe_asn_info.items():
    if value['country'] not in all_countries.keys():
        all_countries[value['country']] = 1
    else:
        all_countries[value['country']] += 1

with open("all_countries.json", 'w') as f:
    json.dump({key: value for key, value in sorted(all_countries.items(), key=lambda item: int(item[1]), reverse=True)}, f, indent=4)