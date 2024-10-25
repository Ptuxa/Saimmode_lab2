import simpy

import json

from systemRuns import SystemRuns

with open('inputData.json') as f:
    data = json.load(f)

systemRuns = SystemRuns(data)
systemRuns.start()
systemRuns.report_statistics()