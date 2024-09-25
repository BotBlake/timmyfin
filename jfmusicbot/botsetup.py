import os
import yaml

# Path to YML-File
yml_filename = "config.yml"


# Check User Input before parsing through
def get_user_input(prompt, default=None, validation_func=None):
    while True:
        user_input = input(f"{prompt} (Default: {default}): ") or default
        if validation_func and not validation_func(user_input):
            print("Invalid Input. Please try again!")
        else:
            return user_input


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n]: "
    elif default == "yes":
        prompt = " [Y/n]: "
    elif default == "no":
        prompt = " [y/N]: "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


# Validationfunctions
class validate:
    def url(url):
        try:
            return url.startswith("http://") or url.startswith("https://")
        except AttributeError:
            return False

    def discord_token(token):
        try:
            return len(token) > 0
        except TypeError:
            return False

    def apikey(apikey):
        try:
            return len(apikey) > 0
        except TypeError:
            return False

    def command_group(group):
        try:
            return len(group) > 0
        except TypeError:
            return False

    def search_limit(limit):
        try:
            return 1 <= int(limit) <= 100  # Limit for Search results between 1 and 100
        except ValueError:
            return False

    def debug_server(server):
        try:
            return (
                len(server) == 18 and server.isdigit()
            )  # Discord Server ID has exactly 18 digits
        except ValueError:
            return False


# expected Config (as Python-Dictionary)
config_fields = {
    "discord-token": {
        "description": "your Discord-Bot Token",
        "type": str,
        "validation_func": validate.discord_token,
        "required": True,
        "default": None,
    },
    "jf-server": {
        "description": "the URL to the Jellyfin Server",
        "type": str,
        "validation_func": validate.url,
        "required": True,
        "default": None,
    },
    "jf-apikey": {
        "description": "a valid API key for the configured Jellyfin Server",
        "validation_func": validate.apikey,
        "type": str,
        "required": True,
        "default": None,
    },
    "command-group": {
        "description": "the desired slashcommand group for your bot ",
        "validation_func": validate.command_group,
        "type": str,
        "required": True,
        "default": "jfmusic",
    },
    "search-limit": {
        "description": "the Number of items to display when searching (min: 1, max: 100)",
        "validation_func": validate.search_limit,
        "type": int,
        "required": True,
        "default": 25,
    },
    "enable-debug": {
        "description": "wether you want to enable Debug mode or not (true/false)",
        "validation_func": None,
        "type": bool,
        "required": True,
        "default": False,
    },
    "debug-server": {
        "description": "the Server ID of a Debug Server (Discord Server ID)",
        "validation_func": None,
        "type": str,
        "required": True,
        "default": False,
    },
}


def build_config():
    print("Welcome to the Config Build Assistant.")
    print()
    prompt = "Do you want to run the full setup?"
    full_setup = query_yes_no(prompt)

    configuration = dict()
    for key in config_fields:
        if not full_setup and not config_fields[key]["required"]:
            print("Skipping {key}, because non mandatory")
            continue
        else:
            default_value = config_fields[key]["default"]
            prompt = "Enter " + config_fields[key]["description"]
            validator = config_fields[key]["validation_func"]
            answer = get_user_input(
                prompt, default=default_value, validation_func=validator
            )
            configuration[key] = answer
    print("Success!")
    print()
    print(yaml.dump(configuration, default_flow_style=False))
    return configuration


# Funktion zum Erstellen der YML-Datei, wenn sie nicht existiert
def create_yml_file():
    if os.path.exists(yml_filename):
        print(f"The file '{yml_filename}' is already existing!")
    else:
        configuration = build_config()

        # YML-Datei erstellen
        with open(yml_filename, "w") as yml_file:
            yaml.dump(configuration, yml_file, default_flow_style=False)
        print(f"The File '{yml_filename}' was successfully created!")


if __name__ == "__main__":
    create_yml_file()
