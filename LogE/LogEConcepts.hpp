#pragma once
#include <type_traits>

namespace loge
{

template <typename T>
concept uint64_enum = std::is_enum_v<T> && std::is_same_v<std::underlying_type_t<T>, uint64_t>;

}
