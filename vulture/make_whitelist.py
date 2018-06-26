from __future__ import print_function

from collections import defaultdict
from xml.etree import ElementTree as ET

from vulture import utils


def create_namewise_dict(v):
    namewise_unused_funcs = defaultdict(lambda: [])
    for item in v.unused_funcs:
        filename = utils.format_path(item.filename)
        namewise_unused_funcs[filename].append(item)
    return namewise_unused_funcs


def make_whitelist(v, xml):
    xpath_file = './packages/package/classes/class'
    with open(xml) as f:
        tree = ET.parse(f)
    files = [node.attrib['filename'] for node in tree.findall(xpath_file)]
    namewise_unused_funcs = create_namewise_dict(v)
    for filename in files:
        xpath = ('./packages/package/classes/class/[@filename="{}"]'
                 '/lines/line[@hits="1"]'.format(filename))
        lines_hit = [int(
            node.attrib['number']) for node in tree.findall(xpath)]
        unused_funcs = namewise_unused_funcs.get(filename, [])
        if unused_funcs:
            print("# " + filename)
            for item in unused_funcs:
                span = item.first_lineno+1, item.last_lineno+1
                for lineno in range(*span):
                    if lineno in lines_hit:
                        print(item.name)
                        break
            print()
