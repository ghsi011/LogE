#include "LogE.hpp"

void LogE::log(uint64_t log)
{
    m_log_queue.push_back(log);
}

std::vector<uint64_t> LogE::get_logs()
{
    return m_log_queue;
}
