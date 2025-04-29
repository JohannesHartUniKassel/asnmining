import pandas as pd

def analyze_nro_delegated(nro_file, filter_status=None):
    dtype_dict = {
        'country': 'str',
        'type': 'str',
        'asn': 'str',
        'status': 'str',
        'org': 'str'
    }
    df = pd.read_csv(
        nro_file, 
        header=None, 
        sep='|', 
        names=['org', 'country', 'type', 'asn', 'dn', 'date', 'status', 'hash', 'origin'], 
        usecols=list(dtype_dict.keys()),
        dtype=dtype_dict,
        on_bad_lines='skip'
    )
    df = df[df['type'] == 'asn']
    df = df[df['asn'] != '*']
    if isinstance(filter_status, set):
        df = df[df['status'] in filter_status]
    df = df.dropna(subset=['asn'])
    return df
    

def analyze_rir(rir_file, filter_status=None):
    dtype_dict = {
        'country': 'str',
        'type': 'str',
        'asn': 'str',
        'status': 'str',
        'org': 'str'
    }
    df = pd.read_csv(
        rir_file, 
        header=None, 
        sep='|', 
        names=['org', 'country', 'type', 'asn', 'dn', 'date', 'status'], 
        usecols=list(dtype_dict.keys()),
        dtype=dtype_dict,
        on_bad_lines='skip'
    )
    df = df[df['type'] == 'asn']
    df = df[df['asn'] != '*']
    if isinstance(filter_status, set):
        df = df[df['status'] in filter_status]
    df = df.dropna(subset=['asn'])
    return df