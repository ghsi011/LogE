# LogE

### This library uses c++20 consteval functions and python (partly generated using codex and github copilot) in order to generate Enums on the fly.
### The main anticipated usage for this library is to allow faster logging for performance oriented client-server applications.

## Main features:
* Automatically generate Enum types and members on usage 
* Provide a to_string function for each generated Enum type
* Each Enum member is calculated a hashed value based on its name - ensures better backwards compatibility(member order is irrelevant)
* Easy version control and backwards compatibility using git. (members deleted in source placed under `deprecated` tag until manual deletion)

Example usage: 

main.cpp:
```cpp
import enums; // auto generated on build
import enums_to_string; // auto generated on build

#include "LogE/StringToEnum.hpp"

using namespace loge;

LogEnum do_work()
{
    // do some work
    if(/*failure conditon*/){
        return to_enum<LogEnum>("some_failure_status");
    }

    if(/*other failure conditon*/){
        return to_enum<LogEnum>("other_failure_status");
    }

    return  to_enum<LogEnum>("success_status");
}

int main()
{
    LogEnum result = do_work();

    if(result != LogEnum::success_status){
        std::cout << LogEnum_to_string(result).c_str() << std::endl; 
    }
}
```

given this cmd-line as a pre-build event: 

```python $(SolutionDir)LogE\scripts\enum_generator.py -o $(ProjectDir)enums.ixx -m enums $(SolutionDir) .hpp,.cpp```

these will be generated:

enums.ixx:
```cpp
module;
#include <cstdint>

export module enums;

export enum class LogEnum : uint64_t {
// commit: c4279bc9
  some_failure_status = 0xc668c49b3be6432e,
  other_failure_status = 0x68c81e2f081370b9,
  success_status = 0xfad661541767d1da,
};
```

to_string_enums.ixx:
```cpp
module;
#include <string>

export module enums_to_string;

import enums;

export constexpr std::string_view LogEnum_to_string(LogEnum value) {
  switch(value) {
    case LogEnum::some_failure_status: return "some_failure_status";
    case LogEnum::other_failure_status: return "other_failure_status";
    case LogEnum::success_status: return "success_status";
    default: return "";
  }
}
};
```

## What is happening here?
This is  enum_generator.py usage:
```
\LogE\scripts>python enum_generator.py -h
usage: enum_generator.py [-h] [-o OUTPUT_PATH] [-m MODULE_NAME] root_dir extensions

positional arguments:
  root_dir              Root directory to start the search from
  extensions            Comma separated list of file extensions to search for

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output file path
  -m MODULE_NAME, --module-name MODULE_NAME
                        Module name
```

* note that the output file name you give will have `to_string_` appended to it for the second file(to_string_enums.ixx in the example)
same is true for the module name.

The script will recursively iterate over all files and directories starting from the given root dir, it will only parse files ending with the given extensions.
it will then uses this regex to find new enum types and members:
```python
# regex to find to_enum<EnumType>(enum_member)
enum_regex = re.compile(r"to_enum<(\w+)>\(\"(\w+)\"\)")
```

## Why is this good for server client applications?
* Using this for logging you can send enum members (8 bytes integers) over the network instead of costly strings.
* in addition the client application only needs the enums themselves and doesn't have to link with the to_string module, saving on size(if you have lots of logs) and hiding your log strings in case they are sensitive.


## Version control (using git)

As you can see in the example above, the enum generator script is git aware.

if you use git in your project any new enum value will be placed under the current commit.
should you delete an enum value (actually delete, commenting it won't be enough) it will not be immediately wiped from the generated module but will be placed under the `depcricated` tag for backwards compatibility.

for instance:
```cpp
module;
#include <cstdint>

export module enums;

export enum class LogEnum : uint64_t {
// commit: 21b89507
  test_log = 0x817a1d5a33978dbb,
// commit: c4279bc9
  success_status = 0xfad661541767d1da,
  other_failure_status = 0x68c81e2f081370b9,
// commit: deprecated
  some_failure_status = 0xc668c49b3be6432e,
};
```

## TODO 
* Support generating header versions
* Consider making StringToEnum.hpp a module too
* Write actual Logger using this method 