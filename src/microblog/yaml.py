'''
Unified YAML output format
'''

import yaml
load = yaml.safe_load

YAML_PARAMS = dict(
    allow_unicode=True,
    default_flow_style=False,
    indent=0,
    sort_keys=False,
)

def _str_presenter(dumper, data):  # https://stackoverflow.com/a/33300001
    if any(x in data for x in """\n"':&*"""):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.representer.SafeRepresenter.add_representer(str, _str_presenter)

def dump(data, file):
    yaml.safe_dump(data, file, **YAML_PARAMS)
