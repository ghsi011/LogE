#include "pch.h"

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

#include "LogE/StringToEnum.hpp"
#include "LogE/LogE.hpp"

import enums;

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
    auto sha1 = compute_sha_without_null("test_log");
    auto sha = compute_sha_without_null("MySecret");
    auto sha2 = compute_sha_without_null("another_enum_value");
    print_256(sha1);
    std::cout << std::endl;
    print_256(sha);
    std::cout << std::endl;
    print_256(sha2);

    const auto sha_8 = static_cast<uint64_t>(LogEnum::MySecret);
    std::cout << std::hex << sha_8 << std::endl;
    uint64_t sha_8_tag = std_array_to_uint64(sha);
    std::cout << std::hex << sha_8_tag << std::endl;

    EXPECT_EQ(sha_8_tag, sha_8);
    EXPECT_TRUE(true);
}

TEST(TestLogE, TestLog)
{
    LogE<LogEnum> logger;
    LogE<MyEnum> logger2;
    LogEnum log1 = to_enum<LogEnum>("test_log");
    logger.log(log1);

    ASSERT_EQ(logger.get_logs().front(), LogEnum::test_log);
    logger.log(to_enum<LogEnum>("MySecret"));
    logger.log(to_enum<LogEnum>("another_enum_value"));
    logger2.log(to_enum<MyEnum>("my_enum_val"));
    logger2.log(to_enum<MyEnum>("my_enum_val2"));
}

TEST(TestLogE, TestPrintLog)
{
    const LogEnum secret = LogEnum::MySecret;
    auto e = LogEnum_to_string(secret);

    ASSERT_EQ(e, std::string("MySecret"));
}