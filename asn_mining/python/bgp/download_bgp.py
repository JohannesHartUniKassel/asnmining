from resources import BGP_DATA_FILE, BGP_URL
from util.downloader import download

def download_bgp():
    bgp = download(BGP_URL, BGP_DATA_FILE)
    return bgp