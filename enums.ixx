module;
#include <string>

export module enums;

export enum class LogEnum : uint64_t {
// commit: e7ecf7b8
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

export enum class MyEnum : uint64_t {
// commit: e7ecf7b9
  my_enum_val = 0x5cae3ca21d2dbf1b,
  my_enum_val2 = 0xa7e090c4c46a38a3,
};

export constexpr std::string_view MyEnum_to_string(MyEnum value) {
  switch(value) {
    case MyEnum::my_enum_val: return "my_enum_val";
    case MyEnum::my_enum_val2: return "my_enum_val2";
    default: return "";
  }
}

