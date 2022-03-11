module;
#include <string>

export module enums;

export enum LogEnum : uint64_t {
  test_log = 0x817a1d5a33978dbb,
  MySecret = 0x49562cfc3b17139e,
  another_enum_value = 0xe7bacff9ede5dd6b,
};

export constexpr std::string_view LogEnum_to_string(LogEnum value) {
  switch(value) {
    case LogEnum::test_log: return "test_log";
    case LogEnum::MySecret: return "MySecret";
    case LogEnum::another_enum_value: return "another_enum_value";
    default: return "";
  }
}

