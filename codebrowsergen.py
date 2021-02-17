import os
import re
import sys

sidebar = '''<pre><div style="
    left: 0px;
    position: fixed;
    top: 0px;
    padding-top:40px;
    padding-left:20px;
    bottom: 0;
    overflow-y: scroll;
    width: 20%;
    background-color: lightgray;
    ">'''
main_style = '''<div id="top" style="
    max-width: 600px;
    margin: auto;
    # background-color: darkgray;
    font-family: monospace;
    position: absolute;
    top:0;
    left: 30%;
    font-size: 1.25em;
    font-weight: lighter;
    ">'''
text = ''

start_path = os.getcwd()
name = os.path.basename(start_path)
print('name:', name)

for root, dirs, files in os.walk(start_path, topdown=True):
    path = root.split(os.sep)

    folder_name = os.path.basename(root)
    if '__' not in folder_name and os.listdir(root): # ignore some folders
        if folder_name == name:
            sidebar += '<a href="#top">' + folder_name + '</a>\n'
        else:
            sidebar += (len(path) - 1) * '\n  ' + folder_name + '\n'

    ignore = ('.pyc', '.blend', '.txt', '.blend1', '.html', '.bat')

    for file in sorted(files):
        print(file)
        if '.' + file.split('.')[-1] in ignore:
            continue

        if file.endswith('.py') or '.' not in file:
            sidebar += len(path) * '  ' + '<a href="#'
            sidebar += file.split(' ', 1)[0] + '">' + file.split(' ', 1)[0]
            sidebar += '</a>\n'
        else:
            sidebar += len(path) * '  ' + file + '\n'

        file_path = os.path.join(root, file)
        if os.path.isfile(file_path) and file.endswith('.py') or '.' not in file:
            # print('is file')
            with open(file_path, 'r', encoding='utf-8') as t:
                filename = os.path.basename(file_path)
                text += '\n\n\n'
                text += '-' * 32 + '\n'
                text += '<b id="' + filename.split('\\')[-1].split(' ', 1)[0]
                text += '">' + filename.split('\\')[-1] + '</b>' + '\n'
                text += '-' * 32 + '\n'

                t = t.read()
                t = '    ' + '\n    '.join(t.split('\n'))   # indent the text
                text += t.replace('<', '&lt;').replace('>', '&gt;')

# color words
orange_text = 'None,True,False'.split(',')
purple_text = (
    'class ','from ','import ','try:',
    ' pass',' return',' continue', ' assert ',
    ' for ',' in ', 'print','except:',
    'except ','exec(', ' not ', ' is ',
    ' if', '\nif', ' elif ',' else:','def ',
    ' and ', ' with ', ' as ', ' raise '
)
blue_text = '''__init__, open,range(,dict(,
list(,str( int(),float(,getattr(,setattr,isinstance(,type(,eval(,
super(,object(, len(,hasattr'''.split(',')


replacements = dict()
for t in orange_text:
    replacements[t] = '<font color="orange">' + t + '</font>'
for t in blue_text:
    replacements[t] = '<font color="blue">' + t + '</font>'
for t in purple_text:
    replacements[t] = '<font color="purple">' + t + '</font>'
    # replacements[t] = '<div style="text-color: purple;>' + t + '</div>'
from ursina import multireplace
text = multireplace(text, replacements)



text = text.replace('@', '<font color="blue">@')
text = text.replace('example:', '<font color="red">example:</font>')
newtext = ''
for line in text.split('\n'):
    if '@' in line:
        line += '</font>'

    if '#' in line and not ("'#'") in line: # ignore startswith('#'):
        split_line = line.split('#', 1)
        # remove color tags within comment
        comment = split_line[1]
        for tag in ('</font>', '<font color="green">',
        '<font color="orange">', '<font color="blue">',
        '<font color="red">', '<font color="purple">'):
            comment = comment.replace(tag, '')

        line = split_line[0] + '<font color="gray">' + '#' + comment + '</font>'
        line = line.replace("'", '')

    newtext += line + '\n'

text = newtext

# triple quotes
newtext = ''
startquote = False
for comment in text.split("'''"):
    tag = '<font color="green">\'\'\'' if startquote else '\'\'\'</font>'
    newtext += tag + comment

    startquote = not startquote

text = newtext

# single quotes
newtext = ''
startquote = True
comments = text.split("'")
for i, comment in enumerate(comments):
    if not comment.startswith('t ') and not comment.startswith('s '):
        if comments[i-1].endswith('n') and comment.startswith('t '):
            newtext += "'" + comment
        else:
            tag = '<font color="green">\'' if startquote else '\'</font>'
            newtext += tag + comment
            startquote = not startquote
    else:
        newtext += "'" + comment

text = newtext

header = '''<div style="
    font-size: 5em;
    padding-top: 40px"
    >'''



try:    # if you pass title when running the script
    header += sys.argv[1]
except:
    header += name + ' <br>code browser'

header += '''</div>'''

footer = '''<div style="
    font-size: 2em;
    align: center;
    ">'''
footer += '\n' * 2
footer += '''
(\\(\\
(-.-)
(")(") END

</div>'''


with open(name + '_code_browser.html', 'w', encoding='utf-8') as file:
    file.write(main_style)
    file.write(header)
    file.write('<pre>')
    file.write(text)
    file.write(footer)
    file.write(sidebar)

    print('finished building code browser')
