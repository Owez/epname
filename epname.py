import sys
import pathlib
import os
import re

"""Regex for season names"""
SEASON_NAME = "s(e(ason)?)?( )*([0-9])*[0-9]( )?"

"""Regex for episode names"""
EPISODE_NAME = "e(pisode|p(i)?)?( )*([0-9])*[0-9]"


def fatal(msg: str):
    """Fatal error message"""

    print(f"error: {msg}!")
    sys.exit(1)


def log(msg: str):
    """Log message"""

    print(f"info: {msg}")


print("epname: format your movies!")

args = sys.argv[1:]

if len(args) < 1 or len(args) > 2:
    fatal(
        "please provide one argument for the final name and an optional argument for season num of current path"
    )

files = list(os.walk(pathlib.Path().absolute()))[0][2]

if len(files) == 0:
    fatal("no files found to rename")


def gen_file(wanted_name: str, season_num: int, episode_num: int, org_file: str) -> str:
    """Generates number of episode, e.g. 2 and 63 goes to s02e63"""

    file_formatted = "-".join(wanted_name.split(" ")).lower()
    ext = org_file.split(".")[-1].lower()

    return f"{file_formatted}-s{season_num:02}e{episode_num:02}.{ext}"


ran = 0

for file in files:
    episode_match = re.search(EPISODE_NAME, file)

    if episode_match is None:
        continue

    ran += 1
    season_match = re.search(SEASON_NAME, file)

    if season_match is None and len(args) != 2:
        fatal(f"no season found for '{file}' and no season num given as arg")

    season_num = int(
        args[1]
        if season_match is None
        else season_match.group().split("n")[-1].split("s")[-1]
    )
    episode_num = int(episode_match.group().split("e")[-1])
    generated_file = gen_file(args[0], season_num, episode_num, file)

    log(f"renaming '{file}' to '{generated_file}'..")
    os.system(f"mv '{file}' '{generated_file}'")

if ran != 0:
    log(f"renamed {ran} file(s) successfully")
else:
    fatal("found no files to rename")