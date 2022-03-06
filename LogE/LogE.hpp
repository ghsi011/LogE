#pragma once
#include <vector>

class LogE final
{
public:
    void log(uint64_t log);
    std::vector<uint64_t> get_logs();

private:
    std::vector<uint64_t> m_log_queue;
};

