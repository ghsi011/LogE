#include "pch.h"

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>

#include "sha256_literal.h"

template <size_t N>
constexpr uint64_t std_array_to_uint64(std::array<uint8_t, N> arr)
{
    static_assert(N >= sizeof(uint64_t));

    uint64_t number = 0;
    for (uint32_t index = 0; index < sizeof(uint64_t); ++index) {
        uint64_t byte = arr[index];

        constexpr uint64_t BITS_IN_BYTE = 8;
        byte = byte << BITS_IN_BYTE * index;
        number += byte;
    }

    return number;
}

template <size_t N>
constexpr uint64_t msg_to_enum(char const (&Data)[N])
{
    auto data_hash = sha256_literal::compute(Data);
    return std_array_to_uint64(data_hash);
}

enum class LogE : uint64_t
{
    MySecret = msg_to_enum("MySecret"),
    unknown = 0,
};



TEST(TestCaseName, TestName)
{

    constexpr auto sha = sha256_literal::compute("MySecret");
    std::string a(sha.begin(), sha.end());
    std::cout << a.c_str() << std::endl;
    const auto sha_4 = static_cast<uint32_t>(LogE::MySecret);
    std::cout << std::to_string(sha_4) << std::endl;

    EXPECT_EQ(1, 1);
    EXPECT_TRUE(true);
}