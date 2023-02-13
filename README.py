import os
from urllib.parse import quote

repoName = 'Source-Code-Analysis'
rootDir = './'

def generate(dir, depth, file):
    listdir = os.listdir(dir)
    listdir.sort()
    for path in listdir:
        if depth == 1 and path == 'README.md':
            continue
        if path.startswith('.'):
            continue
        fullPath = os.path.join(dir, path)
        if os.path.isdir(fullPath):
            for i in range(1, depth):
                file.write('##')
            if depth == 2:
                title = ' ' + path + '\n'
                file.write(title)
            generate(fullPath, depth + 1, file)
        else:
            if not path.endswith('.md'):
                continue
            content = '* [' + path + '](https://github.com/lukailun/' + repoName + '/tree/master/' + quote(fullPath.replace(rootDir, '')) + ')\n'
            file.write(content)

with open('README.md', 'w') as README:
    README.write('# Source Code Analysis\n')
    generate(rootDir, 1, README)
    README.write('<br><br>\n> Automatically generate README: python3 README.py')
print('README has been updated.')