#pragma once
#include "sha256_literal.h"

namespace Loge
{

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
constexpr uint64_t str_to_uint64_t(char const (&data)[N])
{
    auto data_hash = sha256_literal::compute(data);
    return std_array_to_uint64(data_hash);
}

template <size_t N, typename Enum>
constexpr Enum str_to_enum(char const (&data)[N])
{
    return static_cast<Enum>(str_to_uint64_t(data));
}
}
