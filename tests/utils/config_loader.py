import os
import yaml
from dotenv import load_dotenv

load_dotenv()  # loads .env into env

def load_config(yaml_path: str = "config.yaml"):
    with open(yaml_path, 'r') as f:
        raw = f.read()
    # simple env substitution for ${VAR}
    for k, v in os.environ.items():
        raw = raw.replace(f"${{{k}}}", v)
    cfg = yaml.safe_load(raw)
    return cfg
