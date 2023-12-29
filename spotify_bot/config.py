import toml


def get_config():
    config = toml.load(".config.toml")
    test_config = toml.load(".test_config.toml")
    return test_config if config["TESTING"] else config
