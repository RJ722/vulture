from __future__ import print_function

from collections import defaultdict
import os.path
from xml.etree import ElementTree as ET

from vulture import utils


def create_namewise_dict(v):
    namewise_unused_funcs = defaultdict(lambda: [])
    for item in v.unused_funcs:
        filename = os.path.normcase(utils.format_path(item.filename))
        namewise_unused_funcs[filename].append(item)
    return namewise_unused_funcs


def make_whitelist(v, xml):
    xpath_file = './packages/package/classes/class'
    with open(xml) as f:
        tree = ET.parse(f)
    files = [node.attrib['filename'] for node in tree.findall(xpath_file)]
    print("Files from XML: ", files)
    namewise_unused_funcs = create_namewise_dict(v)
    print("item.filename: ", namewise_unused_funcs.keys())
    for filename in files:
        xpath = ('./packages/package/classes/class/[@filename="{}"]'
                 '/lines/line[@hits="1"]'.format(filename))
        lines_hit = [int(
            node.attrib['number']) for node in tree.findall(xpath)]
        print("Lines which are hit: ", lines_hit)
        filename = os.path.normcase(os.path.normpath(filename))
        print("Filename after normalizing: ", filename)
        unused_funcs = namewise_unused_funcs.get(filename, [])
        print("namewise unused funcs: ", namewise_unused_funcs.items())
        print("Unused funcs in this file: ", unused_funcs)
        if unused_funcs:
            print("# " + filename)
            print("Unused funcs: ", unused_funcs)
            for item in unused_funcs:
                span = item.first_lineno+1, item.last_lineno+1
                print("Span for ", item, " is: ", span)
                for lineno in range(*span):
                    if lineno in lines_hit:
                        print(item.name)
                        break
            print()
