import os
import re
from operator import ge
import typing


from git_utils import *

# find all usages of to_enum<EnumType>(enum_member) function in cpp code and return a dictionary of enums and enum values
def get_all_enum_members(file_path: str) -> dict:
    try:
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

            for match in matches:
                # get the enum type and the enum member
                enum = match[0]
                enum_value = match[1]

                if enum not in enums_map:
                    enums_map[enum] = []
                if enum_value not in enums_map[enum]:
                    enums_map[enum].append(enum_value)

        return enums_map
    except Exception as e:
        print(e)
        return {}


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
    # check if the file exists
    if not os.path.isfile(enums_file_path):
        return {}

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
        combined_enums_map[enum] = merge_enum(new_enums[enum], old_enums_map[enum])
    return combined_enums_map

def merge_enum(new_enum: dict, old_enum: dict):
    combined_enum = {}
    current_commit = get_last_git_commit_hash()
    for enum_value in new_enum:
        is_new = True
        for commit in old_enum:
            if enum_value in old_enum[commit]:
                if commit == "deprecated":
                    break
                is_new = False
                if commit not in combined_enum:
                    combined_enum[commit] = []
                combined_enum[commit].append(enum_value)
                break
        if is_new:
            if current_commit not in combined_enum:
                combined_enum[current_commit] = []
            combined_enum[current_commit].append(enum_value)

    for commit in old_enum:
        for enum_value in old_enum[commit]:
            if enum_value not in new_enum:
                if "deprecated" not in combined_enum:
                    combined_enum["deprecated"] = []
                combined_enum["deprecated"].append(enum_value)
    return combined_enum
