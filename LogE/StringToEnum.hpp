#pragma once
#include "sha256_literal.h"

#include "LogEConcepts.hpp"

namespace loge
{

template <size_t N>
constexpr uint64_t std_array_to_uint64(std::array<uint8_t, N> arr)
{
    static_assert(N >= sizeof(uint64_t));

    uint64_t number = 0;
    uint64_t left_shift_multiplier = sizeof(uint64_t) - 1;
    for (uint32_t index = 0; index < sizeof(uint64_t); ++index) {
        uint64_t byte = arr[index];

        constexpr uint64_t BITS_IN_BYTE = 8;
        byte = byte << (BITS_IN_BYTE * left_shift_multiplier);
        number |= byte;
        --left_shift_multiplier;
    }

    return number;
}

template <size_t N>
constexpr sha256_literal::HashType compute_sha_without_null(char const (&Data)[N])
{
    if (N > 1 && Data[N - 1] == '\0') {
        char no_null[N - 1] = {};
        for (auto i = 0; i < N - 1; i++) {
            no_null[i] = Data[i];
        }
        return sha256_literal::compute(no_null);
    }

    return compute_sha_without_null(Data);
}

template <size_t N>
consteval uint64_t str_to_uint64_t(char const (&data)[N])
{
    auto data_hash = compute_sha_without_null(data);
    return std_array_to_uint64(data_hash);
}

template <uint64_enum Enum, size_t N>
consteval auto to_enum(char const (&data)[N])
{
    //todo verify that the enum value is indeed a member
    return static_cast<Enum>(str_to_uint64_t(data));
}
}
