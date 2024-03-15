# To import Turtl json backups into Joplin
# json to markdown directory structure
# just the python version of https://discourse.joplinapp.org/t/turtl-to-markdown-directory/3313 thx to magnusmanske

import json
import os
import re
import sys

def sanitize_filename(s):
    s = re.sub(r'[_/\|"]', ' ', s)
    s = re.sub(r'\.+', '.', s)
    return s

if len(sys.argv) < 3:
    sys.exit("USAGE: {} turtl_backup_file.json output_directory".format(sys.argv[0]))

input_file = sys.argv[1]
output_dir = sys.argv[2]

try:
    with open(input_file, 'r') as file:
        j = json.load(file)
except FileNotFoundError:
    sys.exit("File {} does not exist, or is not valid JSON".format(input_file))

os.makedirs(output_dir, exist_ok=True)

spaces = {s['id']: sanitize_filename(s['title']) for s in j.get('spaces', [])}
for s_id, title in spaces.items():
    os.makedirs(os.path.join(output_dir, title), exist_ok=True)

boards = {}
for b in j.get('boards', []):
    space_name = spaces[b['space_id']]
    board_title = f"{space_name}/{sanitize_filename(b['title'])}"
    boards[b['id']] = board_title
    os.makedirs(os.path.join(output_dir, board_title), exist_ok=True)

for n in j.get('notes', []):
    board_title = spaces[n['space_id']] if n.get('board_id') is None else boards[n['board_id']]
    add = 0  # Initialize add as 0 for clarity
    while True:
        if add == 0:
            filename = os.path.join(output_dir, board_title, sanitize_filename(n['title']) + ".md")
        else:
            filename = os.path.join(output_dir, board_title, sanitize_filename(n['title']) + f"-{add}.md")
        if not os.path.exists(filename):
            break
        add += 1
    text = n.get('password', n.get('text', ''))
    with open(filename, 'w') as note_file:
        note_file.write(text)

