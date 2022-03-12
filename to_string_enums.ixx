module;
#include <string>

export module enums_to_string;

import enums;

export constexpr std::string_view LogEnum_to_string(LogEnum value) {
  switch(value) {
    case LogEnum::test_log: return "test_log";
    case LogEnum::MySecret: return "MySecret";
    case LogEnum::another_enum_value: return "another_enum_value";
    case LogEnum::another_enum_value1: return "another_enum_value1";
    case LogEnum::another_enum_value7: return "another_enum_value7";
    default: return "";
  }
}

export constexpr std::string_view MyEnum_to_string(MyEnum value) {
  switch(value) {
    case MyEnum::my_enum_val: return "my_enum_val";
    case MyEnum::my_enum_val2: return "my_enum_val2";
    case MyEnum::my_enum_val3: return "my_enum_val3";
    default: return "";
  }
}

