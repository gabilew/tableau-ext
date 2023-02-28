import os

def prepared_env(prefix):
    config = {}
    config["TOKEN_SECRET"] = os.environ.get(prefix + "_TOKEN_SECRET")
    config["TOKEN_NAME"] = os.environ.get(prefix + "_TOKEN_NAME")
    return config


