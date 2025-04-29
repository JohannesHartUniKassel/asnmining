import math
import asn_mining
import requests
from resources import *
import os
from range_map import RangeMap
import csv
import json
from util.downloader import download
import iana.download_iana
import iana.iana_index
import nro.nro_download as nro_download
import nro.analyze_nro as analyze_nro
import ripe.country_data as country_data
from util.df_export import dump_df_to_file

def stats(download_files=True, bgp_cache=False):
    print("Init IANA info...")
    if (download_files):
        iana.download_iana.download_iana()
    iana_range_map = iana.iana_index.create_iana_index(IANA_16_BIT_FILE, IANA_32_BIT_FILE)
    
    if (download_files):
        print("Downloading NRO files...")
        nro, afrinic, apnic, arin, lacnic, ripencc = nro_download.download_all()
    else:
        nro, afrinic, apnic, arin, lacnic, ripencc = NRO_DELEGATED_STATS_FILE, AFRINIC_STATS_FILE, APNIC_STATS_FILE, ARIN_STATS_FILE, LACNIC_STATS_FILE, RIPE_STATS_FILE

    print("Analyzing files...")
    print("NRO delegated stats")
    nro_result = analyze_nro.analyze_nro_delegated(nro)
    nro_result_keys = set(nro_result['asn'].unique())
    dump_df_to_file(nro_result, "nro.json")

    print("APNIC delegated stats")
    apnic_result = analyze_nro.analyze_rir(apnic)
    apnic_result_keys = set(apnic_result['asn'].unique())
    dump_df_to_file(apnic_result, "apnic.json")
        
    print("RIPE NCC delegated stats")
    ripencc_result = analyze_nro.analyze_rir(ripencc)
    ripencc_result_keys = set(ripencc_result['asn'].unique())
    dump_df_to_file(ripencc_result, "ripencc.json")
        
    print("AFRINIC delegated stats")
    afrinic_result = analyze_nro.analyze_rir(afrinic)
    afrinic_result_keys = set(afrinic_result['asn'].unique())
    dump_df_to_file(afrinic_result, "afrinic.json")
        
    print("LACNIC delegated stats")
    lacnic_result = analyze_nro.analyze_rir(lacnic)
    lacnic_result_keys = set(lacnic_result['asn'].unique())
    dump_df_to_file(lacnic_result, "lacnic.json")
        
    print("ARIN delegated stats")
    arin_result = analyze_nro.analyze_rir(arin)
    arin_result_keys = set(arin_result['asn'].unique())
    dump_df_to_file(arin_result, "arin.json")

    if download_files:
        print("Downloading BGP data...")
        bgp = download(BGP_URL, BGP_DATA_FILE)
    else:
        bgp = BGP_DATA_FILE
    if bgp_cache:
        with open("bgp.json", 'r') as f:
            bgp_result = {
                'all_asns': set(json.load(f))
            }
    else:
        print("Analyzing BGP data...")
        bgp_result = asn_mining.bgp(bgp)
    with open("bgp.json", 'w') as f:
        json.dump(sorted(bgp_result['all_asns'], key=lambda x: int(x)), f, indent=4)
        
    print("Comparing results...")
    dif_bgp_nro = bgp_result['all_asns'] - nro_result_keys
    dif_nro_bgp = nro_result_keys - bgp_result['all_asns']
    
    dif_bgp_nro_rir = dict()
    for asn in dif_bgp_nro:
        responsible_rir = iana_range_map.get_value(int(asn))
        if dif_bgp_nro_rir.get(responsible_rir) is None:
            dif_bgp_nro_rir[responsible_rir] = list()
        dif_bgp_nro_rir[responsible_rir].append(asn)
    
    for key, value in dif_bgp_nro_rir.items():
        dif_bgp_nro_rir[key] = sorted(value, key=lambda x: int(x))
    
    with open("dif_bgp_nro_rir.json", 'w') as f:
        json.dump(dif_bgp_nro_rir, f, indent=4)

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
            dif_bgp_afrinic.add(asn)
            
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
        
if __name__ == "__main__":
    import stats
    import os
    download_var = os.environ.get("DOWNLOAD", "true").lower() == "true"
    cache = os.environ.get("CACHE", "false").lower() == "true"
    stats.stats(download_var, cache)