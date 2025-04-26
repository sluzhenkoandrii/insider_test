from os import getenv

import yaml


def env(var) -> str:
    """Return the value for a specified env. variable, exit if not found."""
    if value := getenv(var):
        return value
    raise SystemExit('env variable ' + var + ' not defined')


if cluster := getenv('CONFIG'):
    with open('configs/' + cluster + '.yml', encoding='utf-8') as file:
        config = yaml.safe_load(file)
else:
    config = {
        'use_insider_url': env('USE_INSIDER_URL'),
        'time_to_wait_for_el': env('time_to_wait_for_el'),
    }
