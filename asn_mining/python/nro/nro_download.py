from resources import *
from util.downloader import download

def download_nro_delegated():
    nro = download(NRO_DELEGATED_STATS_URL, NRO_DELEGATED_STATS_FILE) 
    return nro

def download_ripe():
    ripencc = download(RIPE_STATS_URL, RIPE_STATS_FILE)
    return ripencc

def download_apnic():
    apnic = download(APNIC_STATS_URL, APNIC_STATS_FILE)
    return apnic

def download_afrinic():
    afrinic = download(AFRINIC_STATS_URL, AFRINIC_STATS_FILE)
    return afrinic

def download_lacnic():
    lacnic = download(LACNIC_STATS_URL, LACNIC_STATS_FILE)
    return lacnic

def download_arin():
    arin = download(ARIN_STATS_URL, ARIN_STATS_FILE)
    return arin

def download_all():
    return (
        download_nro_delegated(),
        download_afrinic(),
        download_apnic(),
        download_arin(),
        download_lacnic(),
        download_ripe()
    )