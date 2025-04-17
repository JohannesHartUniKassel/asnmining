from resources import IANA_16_BIT_URL, IANA_16_BIT_FILE, IANA_32_BIT_FILE, IANA_32_BIT_URL
from stats import download

def download_iana():
    i16 = download(IANA_16_BIT_URL, IANA_16_BIT_FILE)
    i32 = download(IANA_32_BIT_URL, IANA_32_BIT_FILE)
    return (i16, i32)