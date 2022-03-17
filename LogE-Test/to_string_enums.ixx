module;
#include <string>

export module enums_to_string;

import enums;

export constexpr std::string_view LogEnum_to_string(LogEnum value) {
  switch(value) {
    case LogEnum::test_log: return "test_log";
    case LogEnum::success_status: return "success_status";
    case LogEnum::other_failure_status: return "other_failure_status";
    case LogEnum::some_failure_status: return "some_failure_status";
    default: return "";
  }
}

