#[---------------]#
#[----IMPORTS----]#
#[---------------]#

import pygame
import json

#[------------]#
#[----DATA----]#
#[------------]#

with open("dictionaries/bugDictionaries.json", "r") as f:
    bugs_list = json.load(f)

with open("dictionaries/environmentDictionaries.json", "r") as f:
    environments_list = json.load(f)