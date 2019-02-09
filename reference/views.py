from flask import Flask, Markup, render_template
from os import listdir, path, walk
from reference import app
import re


@app.route('/')
def reference():
    commands_path = path.join(app.static_folder, 'commands')
    commands = {}
    for _, subdirList, _ in walk(commands_path):
        # over CATEGORIES
        for category in subdirList:
            commands[category] = []
            # over COMMANDS in category
            for filename in sorted(listdir(path.join(commands_path, category))):
                filestring = open(path.join(commands_path, category, filename)).read()
                filecontents = re.split('\n--+ *\n', filestring, flags=re.MULTILINE)
                commands[category].append((filename, filecontents[0], filecontents[1]))
    return render_template('index.html', allFiles=commands)


@app.route('/reference/<category>/<name>')
def command(category, name):
    content = open(path.join(app.static_folder, 'commands', category, name)).read()
    return render_template('command.html', name=name, documentation=content)