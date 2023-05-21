import os
import yaml

conversations = {}


def save_conversation(conversation, channel_id):
    print('Saving...')
    if not os.path.exists("./conversations"):
        os.makedirs("./conversations")
    with open(f"./conversations/{channel_id}.yml", 'w') as yaml_file:
        yaml.dump(conversation, yaml_file, default_flow_style=False, allow_unicode=True)
    print('Saved!')


def create_or_restore_conversation(channel_id) -> list:
    if not os.path.isfile(f"./conversations/{channel_id}.yml"):
        return []
    with open(f"./conversations/{channel_id}.yml", 'r') as yaml_file:
        return yaml.safe_load(yaml_file)
