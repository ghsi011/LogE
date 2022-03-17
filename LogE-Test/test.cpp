#include "pch.h"

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

#include "LogE/StringToEnum.hpp"
#include "LogE/LogE.hpp"

import enums;
import enums_to_string;

using namespace loge;

void print_256(std::array<uint8_t, 32> value)
{
    for (int i = 0; i < 32; i++) {
        std::cout << std::hex << (int)value[i];
    }
    std::cout << std::endl;
}
TEST(TestLogE, TestHash)
{
    auto sha_success_status = compute_sha_without_null("success_status");
    const auto sha_success_status_8_bytes = static_cast<uint64_t>(LogEnum::success_status);

    uint64_t test_std_array_sha = std_array_to_uint64(sha_success_status);

    EXPECT_EQ(test_std_array_sha, sha_success_status_8_bytes);
    EXPECT_TRUE(true);
}

TEST(TestLogE, TestLog)
{
    LogE<LogEnum> logger;
    
    LogEnum log1 = to_enum<LogEnum>("test_log");
    logger.log(log1);

    ASSERT_EQ(logger.get_logs().front(), LogEnum::test_log);
    logger.log(to_enum<LogEnum>("success_status"));
    logger.log(to_enum<LogEnum>("other_failure_status"));
}

TEST(TestLogE, TestPrintLog)
{
    const LogEnum success_status = LogEnum::success_status;
    auto e = LogEnum_to_string(success_status);

    ASSERT_EQ(e, std::string("success_status"));
}