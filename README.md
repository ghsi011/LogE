## LogE

This library aims to demonstrate the ability to use compile time comutations to generate enums on the fly
It uses c++20 consteval functions and python scripts in order to achive this.

Example usage: 

main.cpp:
```cpp
import enums; // auto generated on build
import enums_to_string; // auto generated on build

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

The script will recursivly 