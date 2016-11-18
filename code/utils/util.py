__author__ = 'Marcelo d\'Almeida'


from collections import namedtuple

READY = "Ready"
RUNNING = "Running"
BLOCKED = "Blocked"
FINISHED = "Finished"

MachinePerformanceInfo = namedtuple("MachinePerformanceInfo", "machine_info machine_value")

MachineInfo = namedtuple("MachineInfo", 'machine_id thread_id')

TaskPackageInfo = namedtuple("TaskPackageInformation", "task_id task_value process_id")

TaskPackage = namedtuple("TaskPackage", "task task_info")

MachineReport = namedtuple("MachineReport", "name total_power total_cost total_delay total_time")
