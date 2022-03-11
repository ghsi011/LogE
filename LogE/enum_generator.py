# python

import argparse
import hashlib
import os
import re

def sha_256_64(string):
    print(string)
    print(hashlib.sha256(string.encode("ascii")).hexdigest())
    return hashlib.sha256(string.encode("ascii")).hexdigest()[:16]

# find all usages of to_enum<EnumType>(enum_member) function in cpp code and return a dictionary with the Enum type as key and a list of all strings given as enum_member for that Enum type as value
# for example for a given line - to_enum<SomeEnum>("SomeEnumValue") - the function will return {"SomeEnum":["SomeEnumValue"]}
# param[in] file_path the cpp file to read
# return map enums and enum members

def get_all_enum_members(file_path):
    # open the file
    file = open(file_path, "r")
    lines = file.readlines()
    file.close()

    # regex to find to_enum<EnumType>(enum_member)
    regex = re.compile(r"to_enum<(\w+)>\(\"(\w+)\"\)")

    # map enums and enum members
    enums = {}

    # for each line
    for line in lines:
        # find all usages of to_enum<EnumType>(enum_member)
        matches = regex.findall(line)
        # for each match
        for match in matches:
            # get the enum type and the enum member
            enum_type = match[0]
            enum_member = match[1]
            # if the enum type is not in the map
            if enum_type not in enums:
                # add it
                enums[enum_type] = []
            # if the enum member is not in the map
            if enum_member not in enums[enum_type]:
                # add it
                enums[enum_type].append(enum_member)

    # return the map
    return enums


# given a map of enums and enum values generate an hpp file named enums.hpp defining the enums in cpp
def generate_enums_module(enums_map):
    # open the file
    file = open("enums.ixx", "w")
    file.write("module;\n")
    file.write("#include <string>\n\n")
    file.write("export module enums;\n\n")
    #for each enum
    for enum_type in enums_map:
        # write the enum
        file.write("export enum " + enum_type + " : uint64_t {\n")
        # for each enum value
        for enum_member in enums_map[enum_type]:
            # write the enum value
            file.write(f"  {enum_member} = 0x{sha_256_64(enum_member)},\n")
        # write the end of the enum
        file.write("};\n\n")
        # write the to_string function
        file.write("export constexpr std::string_view " + enum_type + "_to_string("+ enum_type + " value) {\n")
        file.write("  switch(value) {\n")
        # for each enum value
        for enum_member in enums_map[enum_type]:
            # write the case
            file.write("    case " + enum_type + "::" + enum_member + ": return \"" + enum_member + "\";\n")
        # write the default
        file.write("    default: return \"\";\n")
        # write the end of the function
        file.write("  }\n")
        file.write("}\n\n")
    # close the file
    file.close()


# python code that uses argparse to get a root dir and a list of file extensions as cmdline arguments then recursively iterates over all files with given extensions starting from the root dir
# then use get_all_enum_members on each file and generate enums.hpp using generate_enums_hpp
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", help="Root directory to start the search from")
    parser.add_argument("extensions", help="Comma separated list of file extensions to search for")
    args = parser.parse_args()

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
    generate_enums_module(all_enums_dict)