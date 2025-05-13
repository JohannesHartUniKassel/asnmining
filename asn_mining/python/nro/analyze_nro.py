import pandas as pd

import pandas as pd
import numpy as np

def analyze_nro_delegated(nro_file, filter_status=None):
    dtype_dict = {
        'country': 'str',
        'type': 'str',
        'asn': 'str',
        'num': 'int',
        'status': 'str',
        'org': 'str'
    }
    df = pd.read_csv(
        nro_file, 
        header=None, 
        sep='|', 
        names=['org', 'country', 'type', 'asn', 'num', 'date', 'status', 'hash', 'origin'], 
        usecols=list(dtype_dict.keys()),
        dtype=dtype_dict,
        on_bad_lines='skip'
    )
    df = df.dropna(subset=['asn'])
    df['num'] = df['num'].fillna(1).astype(int)
    df = df[df['type'] == 'asn']
    df = df[df['asn'] != '*']
    df['asn'] = df['asn'].astype(int)

    inserted_rows = []
    for index, entry in df[(df['num'] > 1) & (df['org'] != 'iana')].iterrows():
        for i in range(entry.num - 1):
            new_entry = entry.copy()
            new_entry.asn = entry.asn + i + 1
            inserted_rows.append(new_entry)
    added_df = pd.DataFrame(inserted_rows)
    df = pd.concat([df, added_df], ignore_index=True)
    df.sort_values(by='asn', ascending=True, inplace=True)
    if isinstance(filter_status, set):
        df = df[df['status'].isin(filter_status)]
    df['asn'] = df['asn'].astype(str)
    return df
    

def analyze_rir(rir_file, filter_status=None):
    dtype_dict = {
        'country': 'str',
        'type': 'str',
        'asn': 'str',
        'num': 'float',
        'status': 'str',
        'org': 'str'
    }
    df = pd.read_csv(
        rir_file, 
        header=None, 
        sep='|', 
        names=['org', 'country', 'type', 'asn', 'num', 'date', 'status'], 
        usecols=list(dtype_dict.keys()),
        dtype=dtype_dict,
        on_bad_lines='skip'
    )
    df = df.dropna(subset=['asn'])
    df['num'] = df['num'].fillna(1).astype(int)
    df = df[df['type'] == 'asn']
    df = df[df['asn'] != '*']
    df['asn'] = df['asn'].astype(int)
    inserted_rows = []
    for index, entry in df[(df['num'] > 1) & (df['org'] != 'iana')].iterrows():
        for i in range(entry.num - 1):
            new_entry = entry.copy()
            new_entry.asn = entry.asn + i + 1
            inserted_rows.append(new_entry)
    added_df = pd.DataFrame(inserted_rows)
    df = pd.concat([df, added_df], ignore_index=True)
    df.sort_values(by='asn', ascending=True, inplace=True)
    if isinstance(filter_status, set):
        df = df[df['status'] in filter_status]
    df['asn'] = df['asn'].astype(str)
    return df