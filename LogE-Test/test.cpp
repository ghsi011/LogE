#include "pch.h"

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

#include "LogE/StringToEnum.hpp"
#include "LogE/LogE.hpp"

enum class LogEnum : uint64_t
{
    MySecret = Loge::str_to_uint64_t("MySecret"),
    test_log = Loge::str_to_uint64_t("test_log"),
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
    LogE logger;
    logger.log(Loge::str_to_uint64_t("test_log"));

    ASSERT_TRUE(static_cast<LogEnum>(logger.get_logs().front()) == LogEnum::test_log);
}