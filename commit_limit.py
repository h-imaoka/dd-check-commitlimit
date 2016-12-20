import re
import commands
from checks import AgentCheck


class CommitLimitCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)
        self.p1 = re.compile("^CommitLimit:\s+(\d+)")
        self.p2 = re.compile("^Committed_AS:\s+(\d+)")

    def _get_commit_ratio(self):
        ratio = 0
        s = commands.getoutput("cat /proc/meminfo")
        a = s.split("\n")
        limit = 0
        used = 0
        for l in a:
            m = self.p1.search(l)
            if m:
                limit = int(m.group(1))

            m = self.p2.search(l)
            if m:
                used = int(m.group(1))

        ratio = (used * 100 / limit)
        return ratio

    def check(self, instance):
        self.gauge('system.mem.pct_commit_usage',
                   self. _get_commit_ratio())
