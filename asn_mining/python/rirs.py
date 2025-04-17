from iana.iana_index import create_iana_index
from resources import *
from stats import download
import json


iana_map = create_iana_index(IANA_16_BIT_FILE, IANA_32_BIT_FILE)

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

with open('dif_bgp_nro', 'r') as f:
    json.loads(f.read())