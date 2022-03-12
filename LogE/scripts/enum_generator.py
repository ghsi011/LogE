# python

import argparse
import hashlib
import os
import re
import subprocess
from operator import ge
import typing


def get_last_git_commit_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()[:8]


def sha_256_64(string: str) -> str:
    print(string)
    print(hashlib.sha256(string.encode("ascii")).hexdigest())
    return hashlib.sha256(string.encode("ascii")).hexdigest()[:16]


# find all usages of to_enum<EnumType>(enum_member) function in cpp code and return a dictionary with the Enum type
# as key and a list of all strings given as enum_member for that Enum type as value for example for a given line -
# to_enum<SomeEnum>("SomeEnumValue") - the function will return {"SomeEnum":["SomeEnumValue"]} param[in] file_path
# the cpp file to read return map enums and enum members

def get_all_enum_members(file_path: str) -> dict:
    try:
        # open the file
        lines = []
        with open(file_path, "r") as file:
            lines = file.readlines()

        # regex to find to_enum<EnumType>(enum_member)
        enum_regex = re.compile(r"to_enum<(\w+)>\(\"(\w+)\"\)")

        # map enums and enum members
        enums_map = {}

        for line in lines:
            # find all usages of to_enum<EnumType>(enum_member)
            matches = enum_regex.findall(line)
            # for each match
            for match in matches:
                # get the enum type and the enum member
                enum = match[0]
                enum_value = match[1]
                # if the enum type is not in the map
                if enum not in enums_map:
                    # add it
                    enums_map[enum] = []
                # if the enum member is not in the map
                if enum_value not in enums_map[enum]:
                    # add it
                    enums_map[enum].append(enum_value)

        # return the map
        return enums_map
    except:
        return {}


def generate_enums_module_imp(enums_map: dict, enums_file: typing.TextIO, to_string_file: typing.TextIO,
                              module_name: str):
    enums_header_start = f'''module;
#include <cstdint>

export module {module_name};

'''
    enums_file.write(enums_header_start)
    # enums_file.write("module;\n")
    # enums_file.write("#include <cstdint>\n\n")
    # enums_file.write("export module enums;\n\n")

    to_string_header_start = f'''module;
#include <string>

export module {module_name}_to_string;

import enums;

'''
    to_string_file.write(to_string_header_start)
    # for each enum
    for enum in enums_map:
        # write the enum
        enums_file.write("export enum class " + enum + " : uint64_t {\n")
        # for each enum value
        for commit in enums_map[enum]:
            enums_file.write(f"// commit: {commit}\n")
            for enum_value in enums_map[enum][commit]:
                # write the enum value
                enums_file.write(f"  {enum_value} = 0x{sha_256_64(enum_value)},\n")
        # write the end of the enum
        enums_file.write("};\n\n")
        # write the to_string function
        to_string_file.write(
            "export constexpr std::string_view " + enum + "_to_string(" + enum + " value) {\n")
        to_string_file.write("  switch(value) {\n")
        # for each enum value
        for commit in enums_map[enum]:
            for enum_value in enums_map[enum][commit]:
                # write the case
                to_string_file.write(
                    "    case " + enum + "::" + enum_value + ": return \"" + enum_value + "\";\n")
        # write the default
        to_string_file.write("    default: return \"\";\n")
        # write the end of the function
        to_string_file.write("  }\n")
        to_string_file.write("}\n\n")


# given a map of enums and enum values generate an hpp file named enums.hpp defining the enums in cpp
def generate_enums_module(enums_map: dict, output_file: str, module_name: str):
    # open the file
    with open(output_file, 'w') as enums_file:
        with open(f"{'to_string_'}{output_file}", 'w') as to_string_file:
            generate_enums_module_imp(enums_map, enums_file, to_string_file, module_name)


def get_enums_map_from_existing_file_imp(enums_file: typing.TextIO) -> dict:
    enums_map = {}
    enum = ''
    commit_hash = get_last_git_commit_hash()
    for line in enums_file:
        commit_hash_regex = re.search(r'commit: ([\w]+)', line)
        if commit_hash_regex:
            commit_hash = commit_hash_regex.group(1)

        if line.startswith('export enum class'):
            enum = line.split(' ')[3]
            enums_map[enum] = {}

        # regex finding enum values like "value_name = value,"
        enum_value_regex = re.search(r'([\w_]+) = ([\w_]+),', line)
        if enum_value_regex:
            enum_value_name = enum_value_regex.group(1)
            if commit_hash not in enums_map[enum]:
                enums_map[enum][commit_hash] = []
            enums_map[enum][commit_hash].append(enum_value_name)
    return enums_map


def get_enums_map_from_existing_file(enums_file_path: str) -> dict:
    with open(enums_file_path, 'r') as enums_file:
        return get_enums_map_from_existing_file_imp(enums_file)


def merge_old_and_new_enums(old_enums_map: dict, new_enums: dict):
    combined_enums_map = {}
    current_commit = get_last_git_commit_hash()
    for enum in new_enums:
        combined_enums_map[enum] = {}
        if enum not in old_enums_map:
            combined_enums_map[enum][current_commit] = new_enums[enum]
            continue
        for enum_value in new_enums[enum]:
            is_new = True
            for commit in old_enums_map[enum]:
                if enum_value in old_enums_map[enum][commit]:
                    if commit == "deprecated":
                        break
                    is_new = False
                    if commit not in combined_enums_map[enum]:
                        combined_enums_map[enum][commit] = []
                    combined_enums_map[enum][commit].append(enum_value)
                    break
            if is_new:
                if current_commit not in combined_enums_map[enum]:
                    combined_enums_map[enum][current_commit] = []
                combined_enums_map[enum][current_commit].append(enum_value)

        for commit in old_enums_map[enum]:
            for enum_value in old_enums_map[enum][commit]:
                if enum_value not in new_enums[enum]:
                    if "deprecated" not in combined_enums_map[enum]:
                        combined_enums_map[enum]["deprecated"] = []
                    combined_enums_map[enum]["deprecated"].append(enum_value)

    return combined_enums_map


# python code that uses argparse to get a root dir and a list of file extensions as cmdline arguments then
# recursively iterates over all files with given extensions starting from the root dir then use get_all_enum_members
# on each file and generate enums.hpp using generate_enums_hpp
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", help="Root directory to start the search from")
    parser.add_argument("extensions", help="Comma separated list of file extensions to search for")
    parser.add_argument("-o", "--output_path", help="Output file path", default="enums.ixx")
    parser.add_argument("-m", "--module-name", help="Module name", default="enums")
    args = parser.parse_args()

    print(get_enums_map_from_existing_file(args.output_path))

    old_enums = get_enums_map_from_existing_file(args.output_path)
    extensions = args.extensions.split(",")
    all_enums_dict = {}
    for root, dirs, files in os.walk(args.root_dir):
        for file in files:
            for extension in extensions:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    enums = get_all_enum_members(file_path)
                    for enum_type in enums:
                        if enum_type not in all_enums_dict:
                            all_enums_dict[enum_type] = []
                        for enum_member in enums[enum_type]:
                            if enum_member not in all_enums_dict[enum_type]:
                                all_enums_dict[enum_type].append(enum_member)

    combined_enums = merge_old_and_new_enums(old_enums, all_enums_dict)

    generate_enums_module(combined_enums, args.output_path, args.module_name)
