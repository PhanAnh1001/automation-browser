# setting.py
import json

if 'config' not in globals():
    global config
    with open('inputs/config.json', 'r') as file:
        config = json.load(file)

if 'configSecret' not in globals():
    global configSecret
    with open('inputs/config_secret.json', 'r') as file:
        configSecret = json.load(file)
