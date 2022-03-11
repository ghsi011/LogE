#include "pch.h"

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

#include "LogE/StringToEnum.hpp"
#include "LogE/LogE.hpp"
#include "magic_enum.hpp"

using namespace loge;

enum class LogEnum : uint64_t
{
    MySecret = str_to_uint64_t("MySecret"),
    test_log = str_to_uint64_t("test_log"),
    unknown = 0,
};

TEST(TestLogE, TestHash)
{
    constexpr auto sha = sha256_literal::compute("MySecret");
    const auto sha_8 = static_cast<uint64_t>(LogEnum::MySecret);
    std::cout << std::to_string(sha_8) << std::endl;

    uint64_t sha_8_tag = *reinterpret_cast<const uint64_t*>(sha.data());
    std::cout << std::to_string(sha_8_tag) << std::endl;
        
    EXPECT_EQ(sha_8_tag, sha_8);
    EXPECT_TRUE(true);
}

TEST(TestLogE, TestLog)
{
    LogE<LogEnum> logger;
    logger.log(to_enum<LogEnum>("test_log"));

    ASSERT_TRUE(logger.get_logs().front() == LogEnum::test_log);
}

TEST(TestLogE, TestPrintLog)
{
    const LogEnum secret = LogEnum::MySecret;
    auto e = magic_enum::enum_name(secret);

    ASSERT_EQ(e, std::string("MySecret"));
}