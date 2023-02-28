import os


def prepared_env(prefix):
    config = {}

    config["TOKEN_SECRET"] = os.environ.get(prefix + "_TOKEN_SECRET")
    config["TOKEN_NAME"] = os.environ.get(prefix + "_TOKEN_NAME")
    config["BASE_URL"] = os.environ.get(prefix + "_BASE_URL")
    config["API_VERSION"] = os.environ.get(prefix + "_API_VERSION")
    config["SITE_ID"] = os.environ.get(prefix + "_SITE_ID")
    return config


class MissingArgError(ValueError):
    pass