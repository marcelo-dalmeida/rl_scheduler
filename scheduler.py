__author__ = 'Marcelo d\'Almeida'

import util
import math
from notifier import Notifier

class Scheduler:

    def __init__(self, machines, processes):
        self.machines = {}
        self.processes = {}

        for machine in machines:
            self.machines[machine.get_id()] = machine

        for process in processes:
            self.processes[process.get_id()] = process


        notifier = Notifier(self)

        for machine in self.machines.values():
            machine.subscribe(notifier)

        self.ready_tasks_info = []
        self.ready_machines_info = []

        for process in self.processes.values():
            for task_id in process.get_available_tasks_id():
                task_package_info = util.TaskPackageInfo(task_id, process.get_normalized_power(), process.get_id())
                self.ready_tasks_info.append(task_package_info)

        for machine in self.machines.values():
            for thread_id in machine.get_available_thread_id():
                machine_performance_info = Scheduler.get_machine_performance_info(machine, thread_id)
                self.ready_machines_info.append(machine_performance_info)

    def schedule(self):
        while not self.is_work_done():
            machine, thread_id, machine_index = self.decide_machine(self.ready_machines_info)
            if machine is not None:
                if machine.is_any_thread_available():
                    task_package, task_index = self.decide_task(self.ready_tasks_info)
                    if task_package is not None:
                        print(self.ready_machines_info)
                        print(self.ready_tasks_info)
                        self.ready_machines_info.pop(machine_index)
                        self.ready_tasks_info.pop(task_index)
                        machine.start(task_package, thread_id)

        for machine in self.machines.values():
            machine.threads_join()

        for machine in self.machines.values():
            print(machine.report())

    def decide_machine(self, ready_machines):
        max_performance = -math.inf
        max_index = -1

        for i, machine_info in enumerate(ready_machines):
            machine_value = machine_info.machine_value
            if machine_value > max_performance and machine_value != 0:
                max_performance = machine_value
                max_index = i

        if max_index == -1:
            return None, max_index

        machine_info = ready_machines[max_index].machine_info
        machine_id = machine_info.machine_id
        thread_id = machine_info.thread_id
        machine = self.machines[machine_id]

        return machine, thread_id, max_index

    def decide_task(self, ready_tasks):
        max_task_power = -math.inf
        max_index = -1

        for i, task_info in enumerate(ready_tasks):
            task_value = task_info.task_value
            if task_value > max_task_power and task_value != 0:
                max_task_power = task_value
                max_index = i

        if max_index == -1:
            return None, max_index

        task_info = ready_tasks[max_index]
        task_id = task_info.task_id
        process_id = task_info.process_id
        task = self.processes[process_id].get_task(task_id)
        task_package = util.TaskPackage(task, task_info)

        return task_package, max_index

    def notify(self, notification):
        '''
        Informs the process that the task is done and updates the lists of available resources (tasks and machines)
        :param notification:
        :return:
        '''
        task_package_info = notification[0]
        machine_info = notification[1]

        machine_id = machine_info.machine_id
        thread_id = machine_info.thread_id

        machine = self.machines[machine_id]
        machine_performance_info = Scheduler.get_machine_performance_info(machine, thread_id)


        self.ready_machines_info.append(machine_performance_info)


        task_id = task_package_info.task_id
        process_id = task_package_info.process_id

        process = self.processes[process_id]

        unblocked_tasks_id = process.notify(task_id)

        unblocked_tasks_info = Scheduler.get_task_weight_info(process, unblocked_tasks_id)

        self.ready_tasks_info.extend(unblocked_tasks_info)

    def is_work_done(self):
        for process in self.processes.values():
            if not process.is_finished():
                return False
        return True

    @staticmethod
    def get_machine_performance_info(machine, thread_id):
        '''
        The scheduler defines the metric he is interested about in machines so it can be comparable
        at the time of the decision.
        :param machine:
        :param thread_id:
        :return:
        '''
        machine_info = util.MachineInfo(machine.get_id(), thread_id)
        machine_performance_info = util.MachinePerformanceInfo(machine_info, machine.get_power()/machine.get_cost())
        return machine_performance_info

    @staticmethod
    def get_task_weight_info(process, tasks):
        '''
        The scheduler defines the metric he is interested about in tasks so it can be comparable
        at the time of the decision.
        :param process:
        :param tasks:
        :return:
        '''
        unblocked_task_package_info = []

        for task_id in tasks:
            task_package_info = util.TaskPackageInfo(task_id, process.get_normalized_power(), process.get_id())
            unblocked_task_package_info.append(task_package_info)

        return unblocked_task_package_info






