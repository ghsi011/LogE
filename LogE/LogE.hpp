#pragma once
#include <vector>
#include "LogEConcepts.hpp"

namespace loge
{

template <uint64_enum EnumType>
class LogE final
{
public:
    void log(EnumType log);
    std::vector<EnumType> get_logs();

private:
    std::vector<EnumType> m_log_queue;
};

template <uint64_enum EnumType>
void LogE<EnumType>::log(EnumType log)
{
    m_log_queue.push_back(log);
}

template <uint64_enum EnumType>
std::vector<EnumType> LogE<EnumType>::get_logs()
{
    return m_log_queue;
}
}
