#!/usr/bin/env python3

import argparse
import sys
import signal
from pathlib import Path
from src.Osintgram import Osintgram
from src import printcolors as pc
from src import artwork

try:
    import readline  # Cross-platform readline library
except ImportError:
    is_windows = True
    try:
        from pyreadline3 import Readline
        readline = Readline()
    except ImportError:
        sys.stderr.write("Error: pyreadline3 is required on Windows.")
        sys.exit(1)
else:
    is_windows = False


def print_logo():
    pc.printout(artwork.ascii_art, pc.YELLOW)
    pc.printout("\nVersion 2.0 - Enhanced by Community\n\n", pc.YELLOW)
    pc.printout("Type 'list' to show all allowed commands\n")
    pc.printout("Type 'FILE=y' to save results to files like '<target_username>_<command>.txt'\n")
    pc.printout("Type 'FILE=n' to disable saving to files\n")
    pc.printout("Type 'JSON=y' to export results to JSON files like '<target_username>_<command>.json'\n")
    pc.printout("Type 'JSON=n' to disable exporting to files\n")


def display_commands():
    commands_info = {
        "FILE=y/n": "Enable/disable output in a '<target_username>_<command>.txt' file.",
        "JSON=y/n": "Enable/disable export in a '<target_username>_<command>.json' file.",
        "addrs": "Get all registered addresses by target photos.",
        "cache": "Clear cache of the tool.",
        "captions": "Get target's photos captions.",
        "commentdata": "Get a list of all the comments on the target's posts.",
        "comments": "Get total comments of target's posts.",
        "followers": "Get target followers.",
        "followings": "Get users followed by target.",
        "fwersemail": "Get email of target followers.",
        "fwingsemail": "Get email of users followed by target.",
        "fwersnumber": "Get phone number of target followers.",
        "fwingsnumber": "Get phone number of users followed by target.",
        "hashtags": "Get hashtags used by target.",
        "info": "Get target info.",
        "likes": "Get total likes of target's posts.",
        "mediatype": "Get target's posts type (photo or video).",
        "photodes": "Get description of target's photos.",
        "photos": "Download target's photos in output folder.",
        "propic": "Download target's profile picture.",
        "stories": "Download target's stories.",
        "tagged": "Get list of users tagged by target.",
        "target": "Set new target.",
        "wcommented": "Get a list of users who commented on target's photos.",
        "wtagged": "Get a list of users who tagged the target."
    }
    for cmd, desc in commands_info.items():
        pc.printout(f"{cmd}\t", pc.YELLOW)
        print(desc)


def signal_handler(sig, frame):
    pc.printout("\nExiting... Goodbye!\n", pc.RED)
    sys.exit(0)


def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    return None


def quit_command():
    pc.printout("Goodbye!\n", pc.RED)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
if not is_windows:
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
else:
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

parser = argparse.ArgumentParser(
    description="Osintgram is an OSINT tool for Instagram. It offers an interactive shell "
                "to analyze Instagram accounts by their username."
)
parser.add_argument('id', type=str, help='Instagram username of the target.')
parser.add_argument('-C', '--cookies', help="Clear previous cookies.", action="store_true")
parser.add_argument('-j', '--json', help="Save commands output as JSON files.", action='store_true')
parser.add_argument('-f', '--file', help="Save output in a file.", action='store_true')
parser.add_argument('-c', '--command', help="Run in single-command mode and execute the provided command.", action='store')
parser.add_argument('-o', '--output', help="Specify where to store downloaded photos.", type=Path, default=Path.cwd())

args = parser.parse_args()

api = Osintgram(args.id, args.file, args.json, args.command, args.output, args.cookies)

commands = {
    'list': display_commands,
    'help': display_commands,
    'quit': quit_command,
    'exit': quit_command,
    'addrs': api.get_addrs,
    'cache': api.clear_cache,
    'captions': api.get_captions,
    "commentdata": api.get_comment_data,
    'comments': api.get_total_comments,
    'followers': api.get_followers,
    'followings': api.get_followings,
    'fwersemail': api.get_fwersemail,
    'fwingsemail': api.get_fwingsemail,
    'fwersnumber': api.get_fwersnumber,
    'fwingsnumber': api.get_fwingsnumber,
    'hashtags': api.get_hashtags,
    'info': api.get_user_info,
    'likes': api.get_total_likes,
    'mediatype': api.get_media_type,
    'photodes': api.get_photo_description,
    'photos': api.get_user_photos,
    'propic': api.get_user_propic,
    'stories': api.get_user_stories,
    'tagged': api.get_people_tagged_by_user,
    'target': api.change_target,
    'wcommented': api.get_people_who_commented,
    'wtagged': api.get_people_who_tagged
}

if not args.command:
    print_logo()

while True:
    try:
        if args.command:
            cmd = args.command
            _cmd = commands.get(cmd)
        else:
            pc.printout("Run a command: ", pc.YELLOW)
            cmd = input().strip()
            _cmd = commands.get(cmd)

        if _cmd:
            _cmd()
        elif cmd == "FILE=y":
            api.set_write_file(True)
        elif cmd == "FILE=n":
            api.set_write_file(False)
        elif cmd == "JSON=y":
            api.set_json_dump(True)
        elif cmd == "JSON=n":
            api.set_json_dump(False)
        elif not cmd:
            continue
        else:
            pc.printout("Unknown command\n", pc.RED)

        if args.command:
            break

    except Exception as e:
        pc.printout(f"Error: {str(e)}\n", pc.RED)

