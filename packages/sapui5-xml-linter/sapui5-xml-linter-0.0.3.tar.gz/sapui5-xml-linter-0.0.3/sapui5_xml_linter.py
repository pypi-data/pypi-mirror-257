#!/usr/bin/python3

""" sapui5-xml-linter
Checks XML view files from SAPUI5/OpenUI5 apps for unneeded attributes
"""

import json
import os
import re
import sys
import urllib.request
from urllib.error import HTTPError

from lxml import etree
from config_path import ConfigPath

config_path = ConfigPath('danielkullmann', 'sapui5-xml-linter', '.json')
base_path = config_path.saveFolderPath(mkdir=True)
api_data = {}
sources = None
tried_to_download_already = set()  # namespaces

API_INDEX_URL = "https://sapui5.hana.ondemand.com/docs/api/api-index.json"
API_BASE = "https://sapui5.hana.ondemand.com/test-resources/"


# Download api files from "https://sapui5.hana.ondemand.com/

def download_api_index():
    with urllib.request.urlopen(API_INDEX_URL) as f:
        content = f.read().decode("utf-8")
        with open(os.path.join(base_path, "api-index.json"), "w", encoding="utf-8") as fh:
            fh.write(content)
        index = json.loads(content)
        return index


def download_api_file_or_fail(name):
    if name in tried_to_download_already:
        return
    urlName = name.replace(".", "/")
    tried_to_download_already.add(name)
    with urllib.request.urlopen(API_BASE + urlName + "/designtime/apiref/api.json") as f:
        fileName = name + ".api.json"
        content = f.read().decode("utf-8")
        fullName = os.path.join(base_path, fileName)
        with open(fullName, "w", encoding="utf-8") as fh:
            fh.write(content)
        print("Downloaded ", fileName)


def try_to_download_api_file(full_tag_name):
    last_dot = full_tag_name.rfind(".")
    name = full_tag_name
    while last_dot >= 0:
        name = full_tag_name[0:last_dot]
        try:
            download_api_file_or_fail(name)
            return name
        except HTTPError:
            pass
        last_dot = name.rfind(".")


def find_api_file_for_tag(full_tag_name):
    all_api_files = list_api_files()
    last_dot = full_tag_name.rfind(".")
    name = full_tag_name
    while last_dot >= 0:
        name = full_tag_name[0:last_dot]
        if name + ".api.json" in all_api_files:
            return name
        last_dot = name.rfind(".")


def upgrade():
    os.makedirs(base_path, exist_ok=True)
    print("Saving api files to", base_path)
    index = download_api_index()
    queue = index["symbols"]
    while queue:
        entry = queue.pop()
        if entry["visibility"] != "public":
            continue
        name = entry["name"]
        # TODO This only downloads sap.m and sap.ui.core api files
        if name not in ("sap", "sap.m", "sap.ui", "sap.ui.core", "sap.ui.layout"):
            continue
        try:
            download_api_file_or_fail(name)
        except HTTPError:
             # do not get api.json for sub-paths if I could get it for this path
            if "nodes" in entry:
                queue.extend(entry["nodes"])


# Find and load api files
def list_api_files():
    api_files = [file for file in os.listdir(base_path) if file.endswith(".api.json")]
    return api_files


def make_map(objectList, key):
    result = {}
    for item in objectList:
        result[item[key]] = item
    return result


def load_api_file(api):
    api_file = os.path.join(base_path, api + ".api.json")
    with open(api_file, encoding="utf-8") as fh:
        d = json.load(fh)
        for entry in d["symbols"]:
            if entry["kind"] == "class" or entry["kind"] == "interface":
                properties = {}
                if "properties" in entry:
                    properties = make_map(entry["properties"], "name")
                if "ui5-metadata" in entry and "properties" in entry["ui5-metadata"]:
                    more_properties = make_map(entry["ui5-metadata"]["properties"], "name")
                    properties = {**properties, **more_properties}
                api_data[entry["name"]] = {
                    "name": entry["name"],
                    "extends": entry.get("extends", None),
                    "implements": entry.get("implements", None),
                    "properties": properties
                }
    post_process_api_data()


def fill_properties(entry, api_data):
    parents = []
    if entry["extends"]:
        parents.append(entry["extends"])
    if entry["implements"]:
        parents.extend(entry["implements"])
    while parents:
        parent = parents.pop()
        nodeData = api_data.get(parent, None)
        if nodeData is not None:
            for key, value in nodeData["properties"].items():
                entry["properties"][key] = value
            if nodeData["extends"]:
                parents.append(nodeData["extends"])
            if nodeData["implements"]:
                parents.extend(nodeData["implements"])


def post_process_api_data():
    for entry in api_data.values():
        fill_properties(entry, api_data)


def is_view_file(file_name):
    if os.path.isfile(file_name):
        if (file_name.endswith(".view.xml") or file_name.endswith(".fragment.xml")):
            return True
    return False


def find_xml_files(source, resultList=None):
    if resultList is None:
        resultList = []
    if os.path.isdir(source):
        for f in os.listdir(source):
            find_xml_files(os.path.join(source, f), resultList)
    elif is_view_file(source):
        resultList.append(source)
    return resultList


def full_tag_name(tag):
    tag = etree.QName(tag)
    return tag.namespace + "." + tag.localname, tag.localname


def make_js_string(value):
    ## Need to handle boolean values separately
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def get_tag_definition(tag, local_name):
    # lower-case tag names are for aggregations etc. of sapui5 classes
    if local_name[0] in "abcdefghijklmnopqrstuvwxyz":
        return None

    # 1. Maybe the data is already there..
    result = api_data.get(tag, None)
    if result is not None:
        return result

    # 2. Or the api file has already been downloaded
    api_file = find_api_file_for_tag(tag)
    if api_file is not None:
        load_api_file(api_file)
        return api_data.get(tag, None)

    # 3. Or we need to download an api file for the tag
    name = try_to_download_api_file(tag)
    if name is not None:
        load_api_file(name)

    return api_data.get(tag, None)


def traverse(node, file, api_data, results=None):
    if results is None:
        results = []
    for child in list(node):
        if child.tag is etree.Comment:
            continue
        tag, local_name = full_tag_name(child.tag)
        attributes = [(key, child.get(key)) for key in child.keys()]
        tag_definition = get_tag_definition(tag, local_name)
        if tag_definition is not None:
            property_definitions = tag_definition.get("properties")
            for (name, value) in attributes:
                property_definition = property_definitions.get(name, None)
                if property_definition is not None:
                    default_value = property_definition.get("defaultValue", None)
                    if default_value is not None:
                        default_value = make_js_string(default_value)
                        if value == default_value:
                            entry = (
                                file,
                                child.sourceline,
                                tag,
                                name + "=\"" + value + "\""
                            )
                            results.append(entry)
        elif local_name[0] not in "abcdefghijklmnopqrstuvwxyz":
            # lower-case tag names are for aggregations etc. of sapui5 classes
            print("Nothing for tag", tag)
        traverse(child, file, api_data, results)
    return results


def process(file, api_data):
    results = []
    with open(file, encoding="utf-8") as fh:
        root = etree.parse(fh).getroot()
        results = traverse(root, file, api_data)
    lines = None
    changes = False
    with open(file, encoding="utf-8") as fh:
        lines = fh.readlines()
    if len(results) > 0:
        # Unfortunately, I don't know the exact source line of the attribute;
        # the source line is the last line for the tag (i.e. the opening part of the tag)
        # This means I start with this line and then go backwards in the file until I find
        # the text to be replaced (or I find the beginning of the tag..)
        for (_, lineNo, tag, replacementText) in results:
            print(file, lineNo, tag, replacementText)
            lineNo -= 1 # lxml reports 1-based line numbers
            ## find all the lines that the opening tag is spread on, and check for replacement text
            line = lines[lineNo]
            while True:
                if line.find(replacementText) >= 0:
                    if line.find(" " + replacementText) >= 0:
                        line = line.replace(" " + replacementText, "")
                    elif line.find(replacementText + " ") >= 0:
                        line = line.replace(replacementText + " ", "")
                    elif line.find(replacementText) >= 0:
                        line = line.replace(replacementText, "")
                    lines[lineNo] = line
                    changes = True
                    break
                regex = "<([a-z]+:)?" + tag
                if re.search(regex, line):
                    # This should never happen..
                    print("found beginning of tag", tag, "on line", lineNo)
                    break
                lineNo -= 1
                line = lines[lineNo]

    i = 1
    while i < len(lines):
        regex1 = "^[ \\t]*(/?>)"
        match1 = re.match(regex1, lines[i])
        regex2 = "^[ \\t]*<[a-z][a-zA-Z0-9:]*/>"
        match2 = re.match(regex2, lines[i])
        regex3 = "^[ \\t]*$"
        match3 = re.match(regex3, lines[i])
        if match1:
            lines[i-1] = lines[i-1].rstrip() + match1.group(1) + "\n"
            lines = lines[0:i] + lines[i+1:]
            changes = True
        elif match2 or match3:
            lines = lines[0:i] + lines[i+1:]
            changes = True
        else:
            i += 1

    if changes:
        with open(file, "w", encoding="utf-8") as fh:
            fh.writelines(lines)


def main():
    if len(sys.argv) > 1 and sys.argv[1].startswith("-"):
        option = sys.argv[1]
        if option == "-u":
            # Upgrade!
            upgrade()
        elif option == "-f":
            print("# All api files (in", base_path, ")")
            for f in list_api_files():
                print(f)
        elif option == "-l":
            print("# All view files")
            files = find_xml_files(".")
            for file in files:
                print(file)
        else:
            # Help
            print("SAPUI5 linter")
            print("checks for default values in attributes and removes them")
        sys.exit(1)

    sources = sys.argv[1:]
    if len(sources) == 0:
        print("No arguments given; please specify a file or directory root")
        sys.exit(1)

    api_files = list_api_files()
    if len(api_files) == 0:
        print("No api files found; please run this script with option -u")
        sys.exit(1)

    load_api_file("sap.m")
    load_api_file("sap.ui.core")
    load_api_file("sap.ui.layout")
    post_process_api_data()

    files = []
    for source in sources:
        files.extend(find_xml_files(source))

    for file in files:
        process(file, api_data)


if __name__ == "__main__":
    main()
