def dump_df_to_file(df, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write('[\n')
        json_result = df.to_json(orient='records', lines=True).splitlines()
        f.writelines("\t" + line + ',\n' for line in json_result[:-1])
        f.write("\t" + json_result[-1] + '\n')
        f.write(']\n')
        f.close()