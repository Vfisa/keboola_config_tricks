import datetime
import operator
import os
import time
import json

path = "/data/in/files/"

files = os.listdir(path)


def most_recent_file(path):
    all_files = os.listdir(path)
    file_times = dict()
    new_file = ''

    for f in all_files:
        if f.find('artifacts') >= 0:
            fname_split = f.split('.')
            if fname_split[-1] == 'gz':
                file_times[f] = int(fname_split[0].split('_')[0])
                
    s = sorted(file_times.items(), key=operator.itemgetter(1), reverse=True)

    if len(s):
        new_file = s[0][0]

    return new_file


def extract_tar_file(in_file_name, dest_to_extract):
    print('Extracing dbt doc zip file:', in_file_name)
    if tarfile.is_tarfile(in_file_name):
        fp = tarfile.open(in_file_name)
        fp.extractall(dest_to_extract)
        fp.close()


def create_dbt_index_file(dbt_docs_folder_path, dbt_docs_path):
    search_str = 'o=[i("manifest","manifest.json"+t),i("catalog","catalog.json"+t)]'
    dbt_files_path = dbt_docs_folder_path + '/' + 'dbt docs generate' + '/'
    with open(dbt_files_path + 'index.html', 'r') as f:
        content_index = f.read()

    with open(dbt_files_path + 'manifest.json', 'r') as f:
        json_manifest = json.loads(f.read())

    with open(dbt_files_path + 'catalog.json', 'r') as f:
        json_catalog = json.loads(f.read())

    with open(dbt_docs_path + '/' + 'index2.html', 'w') as f:
        new_str = "o=[{label: 'manifest', data: " + json.dumps(
            json_manifest) + "},{label: 'catalog', data: " + json.dumps(json_catalog) + "}]"
        new_content = content_index.replace(search_str, new_str)
        f.write(new_content)

    print("Docs file produced: index2.html")


new_file = most_recent_file(path)
print("Recent file:", new_file)
dbt_docs_path = "/data/in/files/dbt_docs"
extract_tar_file(path+new_file, dbt_docs_path)
#list_files(dbt_docs_path)
create_dbt_index_file(dbt_docs_path, "/data/in/files/")

## Just if neccessary
#list_files("/data/in/files/")
