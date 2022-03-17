# python 3

import argparse
import os

from git_utils import *
from enum_writer import *
from enum_reader import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", help="Root directory to start the search from")
    parser.add_argument("extensions", help="Comma separated list of file extensions to search for")
    parser.add_argument("-o", "--output_path", help="Output file path", default="enums.ixx")
    parser.add_argument("-m", "--module-name", help="Module name", default="enums")
    args = parser.parse_args()

    os.chdir(args.root_dir)

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
