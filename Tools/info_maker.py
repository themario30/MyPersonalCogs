import json
from xml.etree import ElementTree
from urllib.request import urlopen

# https://wiki.python.org/moin/PyPISimple
def get_distributions(simple_index='https://pypi.python.org/simple/'):
    with urlopen(simple_index) as f:
        tree = ElementTree.parse(f)
    return [a.text for a in tree.iter('a')]

print('Loading pypi distributions', end='...', flush=True)
valid_packages = set(get_distributions())
print('done.')

data = {}

data["NAME"] = input("Cog name: ")
data["AUTHOR"] = input("Author name: ")

install_msg = input("Installation message (skippable if for repo. Use \\n for newlines): ")
data["INSTALL_MSG"] = install_msg.replace("\\n", "\n")

data["SHORT"] = input("Short description (shown in [p]cog list): ")
description = input("Long description for [p]cog info (use \\n for newlines): ")
data["DESCRIPTION"] = description.replace("\\n", "\n")

tags = input("Enter the tags to show on cogs.red, seperated by spaces: ")
data["TAGS"] = [x.lower() for x in tags.split()]

requirements = []
packages = input("Enter any pip dependencies your cog has, seperated by spaces: ")
packages = set(packages.split())

valid = packages & valid_packages
invalid = packages - valid_packages

while invalid:
    print("The following packages aren't in the package index: " + ', '.join(invalid))
    packages = input("Please enter their correct names (or nothing to skip): ")
    packages = set(packages.split())
    valid |= packages & valid_packages
    invalid = packages - valid_packages

data["REQUIREMENTS"] = list(valid)

with open('info.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4,sort_keys=True, separators=(',',' : '))