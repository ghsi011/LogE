import typing
import hashlib
import os

def sha_256_64(string: str) -> str:
    print(string)
    print(hashlib.sha256(string.encode("ascii")).hexdigest())
    return hashlib.sha256(string.encode("ascii")).hexdigest()[:16]

def generate_enums_module_imp(enums_map: dict, enums_file: typing.TextIO, to_string_file: typing.TextIO,
                              module_name: str):
    enums_header_start = f'''module;
#include <cstdint>

export module {module_name};

'''

    to_string_header_start = f'''module;
#include <string>

export module {module_name}_to_string;

import enums;

'''
    enums_file.write(enums_header_start)
    to_string_file.write(to_string_header_start)

    for enum in enums_map:
        write_enum_to_files(enum, enums_map[enum], enums_file, to_string_file)

def write_enum_to_files(enum_name : str, enum_values: dict, enums_file: typing.TextIO, to_string_file: typing.TextIO):
    enums_file.write("export enum class " + enum_name + " : uint64_t {\n")

    for commit in enum_values:
        enums_file.write(f"// commit: {commit}\n")
        for enum_value in enum_values[commit]:
            # write the enum value
            enums_file.write(f"  {enum_value} = 0x{sha_256_64(enum_value)},\n")

    # write the end of the enum
    enums_file.write("};\n\n")
    # write the to_string function
    to_string_file.write(
        "export constexpr std::string_view " + enum_name + "_to_string(" + enum_name + " value) {\n")
    to_string_file.write("  switch(value) {\n")

    for commit in enum_values:
        for enum_value in enum_values[commit]:
            to_string_file.write(
                "    case " + enum_name + "::" + enum_value + ": return \"" + enum_value + "\";\n")

    to_string_file.write("    default: return \"\";\n")

    # write the end of the function
    to_string_file.write("  }\n")
    to_string_file.write("}\n\n")

# given a map of enums and enum values generate an hpp file named enums.hpp defining the enums in cpp
def generate_enums_module(enums_map: dict, output_file: str, module_name: str):
    # open the file
    with open(output_file, 'w') as enums_file:
        # get the file name from path
        file_name = os.path.basename(output_file)
        file_name = f"{'to_string_'}{file_name}"
        # get the dir from path and add the file name
        dir_name = os.path.dirname(output_file)
        to_string_file_path = os.path.join(dir_name, file_name)

        with open(to_string_file_path, 'w') as to_string_file:
            generate_enums_module_imp(enums_map, enums_file, to_string_file, module_name)