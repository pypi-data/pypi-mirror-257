from configparser import ConfigParser
from pathlib import Path

hangpy_dir = Path(__file__).resolve().parent
hangpy_config = f"{hangpy_dir}/config.ini"

def gen_config():
    """Generate config.ini file
    """
    config_file = ConfigParser()
    config_file["Game"] = {
            "lang": "en",
            "word_lang": "es",
            "default_player": "",
        }

    config_file["Player_1"] = {
            "name": "Player 1",
            "points": "0",
        }
    config_file["Player_2"] = {
            "name": "Player 2",
            "points": "0",
        }
    config_file["Player_3"] = {
            "name": "Player 3",
            "points": "0",
        }
    config_file["Player_4"] = {
            "name": "Player 4",
            "points": "0",
        }
    config_file["Player_5"] = {
            "name": "Player 5",
            "points": "0",
        }
    with open(hangpy_config, "w") as file_object:
        config_file.write(file_object)


def clear():
    """Clears terminal
    """
    from os import system, name
    if name == "nt":
        system("cls")
    else:
        system("clear")

# Load config file
CONFIG = ConfigParser()
CONFIG.read(hangpy_config)
if not CONFIG.sections():
    gen_config()
    CONFIG.read(hangpy_config)
