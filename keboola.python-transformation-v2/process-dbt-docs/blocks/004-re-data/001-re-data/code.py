import yaml

API_KEY = "{{ API_KEY }}"

CONFIG_ID = "{{ CONFIG_ID }}"

artifact_url = "in/files/dbt_docs/dbt docs generate"

os.environ["RE_DATA_SEND_ANONYMOUS_USAGE_STATS"] = "0"
print("ANONYMOUS_USAGE_STATS turned off: {}".format(os.environ["RE_DATA_SEND_ANONYMOUS_USAGE_STATS"]))


def create_yaml(filename, data):
    """
    Create yaml files
    """
    
    with open(filename, 'w') as f:
        yaml.dump(data, f)
        print("file {} created".format(filename))


    
config = {
    "re_cloud":{
    "api_key": API_KEY}
    }

dbt_project = {
    "target-path": artifact_url
    }

# create re_data
create_yaml(endpath+"re_data.yml", config)
# create dbt_project
create_yaml("in/files/dbt_docs/dbt docs generate/dbt_project.yml", dbt_project)


# Push data to Re:data
re_bash_call = 're_cloud upload dbt-docs --name "{}" --project-dir "{}" --config-dir "{}"'.format(CONFIG_ID, artifact_url, endpath)
print(re_bash_call)

os.system(re_bash_call)

