"""Module with utils functions."""
import os
from typing import Dict


def prepared_env(prefix: str) -> Dict[str, str]:
    """This function prepare the specific config file considering prefix.

    Args:
        prefix (str): the prefix of the variables that should be in the environment.

    Raises:
        Exception: environment variables not found.

    Returns:
        Mapping[str,str]: config file with the environment variables.
    """
    config = {}
    config["TOKEN_SECRET"] = os.environ.get(prefix + "_TOKEN_SECRET", "")
    config["TOKEN_NAME"] = os.environ.get(prefix + "_TOKEN_NAME", "")
    config["USERNAME"] = os.environ.get(prefix + "_USERNAME", "")
    config["PASSWORD"] = os.environ.get(prefix + "_PASSWORD", "")
    config["BASE_URL"] = os.environ.get(prefix + "_BASE_URL", "")
    config["API_VERSION"] = os.environ.get(prefix + "_API_VERSION", "")
    config["SITE_ID"] = os.environ.get(prefix + "_SITE_ID", "")

    # check which sign in variables are available
    if config["USERNAME"] != "" and config["PASSWORD"] != "":
        config.pop("TOKEN_SECRET")
        config.pop("TOKEN_NAME")
    elif config["TOKEN_NAME"] != "" and config["TOKEN_SECRET"] != "":
        config.pop("USERNAME")
        config.pop("PASSWORD")
    else:
        raise Exception(
            """Either TOKEN_NAME and TOKEN_SECRET or USERNAME
                and PASSWORD should be in the env variables."""
        )

    null_variables = [var for var in config if config[var] == ""]

    if len(null_variables) > 0:
        raise Exception(f"These env variables are missing {null_variables}.")

    return config
