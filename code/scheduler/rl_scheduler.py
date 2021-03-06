__author__ = 'Marcelo d\'Almeida'

import math
import time

import numpy
from code.utils.notifier import Notifier

from code import plot
from code.learning.learning import Q_Learning
from code.utils import util
import code.learning.util as learning_util


class RL_Scheduler:
    #Q(s,a) = recompensa(s) + alpha * max(Q(s'))

    def __init__(self, machines, processes, epochs=1):
        self.machines = {}
        self.processes = {}

        self.current_epoch = 1
        self.epochs_quantity = epochs

        for machine in machines:
            self.machines[machine.get_id()] = machine

        for process in processes:
            self.processes[process.get_id()] = process

        notifier = Notifier(self)

        for machine in self.machines.values():
            machine.subscribe(notifier)

        self._classify_machine()
        self._classify_task()

        self._setup()

        self.q_learning = Q_Learning(power=self.tasks_total_power)

        #self.q_learning.goal(cost=171, time=7)
        self.q_learning.goal(cost=155, time=6.4)

    def _setup(self):
        self.cumulative_machines_power = 0
        self.cumulative_machines_cost = 0
        self.cumulative_machines_delay = 0

        self.ready_tasks_info = []
        self.ready_machines_info = []
        self.ready_tasks_classification = {}
        self.ready_machines_classification = {}

        self.current_machines_power = 0
        self.current_machines_cost = 0
        self.current_machines_delay = 0

        self.total_machines_power = 0
        self.total_machines_cost = 0
        self.total_machines_delay = 0

        self._start_time = 0
        self._start_global_time = 0
        self._total_time = 0
        self._total_power = 0
        self._total_cost = 0
        self._total_delay = 0

        self.tasks_total_power = 0

        for machine in self.machines.values():
            machine_classification = self.machines_classification[machine.get_id()]
            if machine_classification in self.ready_machines_classification.keys():
                self.ready_machines_classification[machine_classification] += 1
            else:
                self.ready_machines_classification[machine_classification] = 1

            for thread_id in machine.get_available_thread_id():

                self.total_machines_power += machine.get_power()
                self.total_machines_cost += machine.get_cost()
                self.total_machines_delay += machine.get_delay()

                machine_performance_info = RL_Scheduler.get_machine_performance_info(machine, thread_id)
                self.ready_machines_info.append(machine_performance_info)

        for process in self.processes.values():
            for task_id in process.get_available_tasks_id():
                self.tasks_total_power += process.get_total_power()
                task_package_info = util.TaskPackageInfo(task_id, process.get_normalized_power(), process.get_id())
                task_classification = self.tasks_classification[task_id]
                self.ready_tasks_info.append(task_package_info)
                if task_classification in self.ready_tasks_classification.keys():
                    self.ready_tasks_classification[task_classification] += 1
                else:
                    self.ready_tasks_classification[task_classification] = 1


    def _classify_machine(self):
        self.machines_classification = {}
        machines_power = [machine.get_power() for machine in self.machines.values()]
        machines_power_mean = numpy.mean(machines_power)
        machines_power_std = numpy.std(machines_power)

        for machine in self.machines.values():
            if machine.get_power() < (machines_power_mean - machines_power_std/2):
                machine_classification = learning_util.LIGHT_MACHINE
            else:
                if machine.get_power() > (machines_power_mean + machines_power_std/2):
                    machine_classification = learning_util.HEAVY_MACHINE
                else:
                    machine_classification = learning_util.MEDIUM_MACHINE
            self.machines_classification[machine.get_id()] = machine_classification

    def _classify_task(self):
        self.tasks_classification = {}
        tasks_power = []
        for process in self.processes.values():
            for task_id, task_power in process.get_tasks_power():
                tasks_power.append(task_power)

        tasks_power_mean = numpy.mean(tasks_power)
        tasks_power_std = numpy.std(tasks_power)

        for process in self.processes.values():
            for task_id, task_power in process.get_tasks_power():
                if task_power < (tasks_power_mean - tasks_power_std/2):
                    task_classification = learning_util.LIGHT_TASK
                else:
                    if task_power > (tasks_power_mean + tasks_power_std/2):
                        task_classification = learning_util.HEAVY_TASK
                    else:
                        task_classification = learning_util.MEDIUM_TASK
                self.tasks_classification[task_id] = task_classification

    def schedule(self):
        self._start_global_time = time.process_time()
        for self.current_epoch in range(1, self.epochs_quantity + 1):
            self._start_time = time.process_time()
            while not self.is_work_done():
                if self.ready_machines_classification and self.ready_tasks_classification:
                    task_classification, machine_classification = self.decide_action(self.ready_machines_classification, self.ready_tasks_classification)
                    machine, thread_id, machine_index = self.decide_machine(self.ready_machines_info, machine_classification)
                    if machine is not None:
                        if machine.is_any_thread_available():
                            task_package, task_index = self.decide_task(self.ready_tasks_info, task_classification)
                            if task_package is not None:

                                total_global_time = time.process_time() - self._start_global_time

                                print('TOTAL TIME')
                                print(total_global_time)

                                current_time = time.process_time() - self._start_time

                                print('EPOCH')
                                print(self.current_epoch)
                                print('CURRENT TIME')
                                print(current_time)
                                print()
                                print(self.ready_machines_info)
                                print(self.ready_tasks_info)

                                self.current_machines_power += machine.get_power()
                                self.current_machines_cost += machine.get_cost()
                                self.current_machines_delay += machine.get_delay()

                                if machine_classification in self.ready_machines_classification.keys():
                                    self.ready_machines_classification[machine_classification] -= 1
                                if self.ready_machines_classification[machine_classification] == 0:
                                    del self.ready_machines_classification[machine_classification]

                                if task_classification in self.ready_tasks_classification.keys():
                                    self.ready_tasks_classification[task_classification] -= 1
                                if self.ready_tasks_classification[task_classification] == 0:
                                    del self.ready_tasks_classification[task_classification]

                                self.ready_machines_info.pop(machine_index)
                                self.ready_tasks_info.pop(task_index)

                                task_id = task_package.task_info.task_id
                                self.inform_task_decision(task_id, task_classification, machine_classification)
                                machine.start(task_package, thread_id)

            for machine in self.machines.values():
                machine.threads_join()

            self._total_time = time.process_time() - self._start_time

            print()
            print("RESULTS")

            for machine in self.machines.values():
                machine_report = machine.report()
                print(machine_report)
                self._total_power += machine_report.total_power
                self._total_cost += machine_report.total_cost
                self._total_delay += machine_report.total_delay

            print()

            print("Total power:", self._total_power)
            print("Total cost:", self._total_cost)
            print("Total delay:", self._total_delay)
            print("Total time:", self._total_time)

            decision_report = self.q_learning.report_decision()
            reward_report, detailed_reward_report = self.q_learning.report_reward()
            power_q_table, cost_q_table, delay_q_table = self.q_learning.report_q_tables()
            distance_error_report = self.q_learning.report_distance_error()
            plot.decisions(decision_report[0], decision_report[1], self.current_epoch)
            plot.rewards(reward_report, detailed_reward_report, self.current_epoch)
            plot.q_table(power_q_table, cost_q_table, delay_q_table, self.current_epoch)
            plot.distance_error(distance_error_report, self.q_learning.get_goal(), self.current_epoch)

            print("EPOCH " + str(self.current_epoch), "", sep='\n')

            self.q_learning.log_reset()

            for machine in self.machines.values():
                machine.reset()
            for process in self.processes.values():
                process.reset()

            self._reset()

        print("Total Global Time:", time.process_time() - self._start_global_time)


    def decide_action(self, machine_classification_available, task_classification_available):
        state = self.get_state()

        action = self.q_learning.decide(state, machine_classification_available, task_classification_available)
        task_classification, machine_classification = action.split("+")
        return task_classification, machine_classification

    def inform_task_decision(self, task_id, task_classification, machine_classification):
        state = self.get_state()

        action = task_classification + "+" + machine_classification
        self.q_learning.inform_taken_action_started(task_id, state, action)

    def learn(self, finished_task_id):
        state = self.get_state()
        self.q_learning.learn(state, finished_task_id)

    def get_state(self):
        system_wide_power = self.current_machines_power/self.total_machines_power
        system_wide_cost = self.current_machines_cost/self.total_machines_cost
        system_wide_delay = self.current_machines_delay/self.total_machines_delay

        cumulative_power = self.cumulative_machines_power
        cumulative_cost = self.cumulative_machines_cost
        cumulative_delay = self.cumulative_machines_delay

        time_state = time.process_time() - self._start_time

        system_state = learning_util.StateInfo(system_wide_power, system_wide_cost, system_wide_delay, time_state)
        cumulative_state = learning_util.StateInfo(cumulative_power, cumulative_cost, cumulative_delay, time_state)

        return [system_state, cumulative_state]

    def decide_machine(self, ready_machines, machine_classification):

        max_performance = -math.inf
        max_index = -1

        if machine_classification is learning_util.DO_NOTHING:
            return None, None, max_index

        eligible_ready_machines = [(index, machine) for index, machine in enumerate(ready_machines)
                          if self.machines_classification[machine.machine_info.machine_id] in machine_classification]

        for i, machine_info in eligible_ready_machines:
            machine_value = machine_info.machine_value
            if machine_value > max_performance and machine_value != 0:
                max_performance = machine_value
                max_index = i

        if max_index == -1:
            return None, None, max_index

        machine_info = ready_machines[max_index].machine_info
        machine_id = machine_info.machine_id
        thread_id = machine_info.thread_id
        machine = self.machines[machine_id]

        return machine, thread_id, max_index

    def decide_task(self, ready_tasks, task_classification):

        max_task_power = -math.inf
        max_index = -1

        if task_classification is learning_util.DO_NOTHING:
            return None, max_index

        eligible_ready_tasks = [(index, task) for index, task in enumerate(ready_tasks)
                       if self.tasks_classification[task.task_id] in task_classification]

        for i, task_info in eligible_ready_tasks:
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
        machine_report = notification[2]

        machine_id = machine_info.machine_id
        thread_id = machine_info.thread_id

        machine = self.machines[machine_id]
        machine_performance_info = RL_Scheduler.get_machine_performance_info(machine, thread_id)

        self.ready_machines_info.append(machine_performance_info)
        machine_classification = self.machines_classification[machine_id]
        if machine_classification in self.ready_machines_classification.keys():
            self.ready_machines_classification[machine_classification] += 1
        else:
            self.ready_machines_classification[machine_classification] = 1

        self.cumulative_machines_power += machine_report.total_power
        self.cumulative_machines_cost += machine_report.total_cost
        self.cumulative_machines_delay += machine_report.total_delay

        print("CUMULATIVE")
        print(self.cumulative_machines_power)

        self.current_machines_power -= machine.get_power()
        self.current_machines_cost -= machine.get_cost()
        self.current_machines_delay -= machine.get_delay()

        task_id = task_package_info.task_id
        process_id = task_package_info.process_id

        self.learn(task_id)

        process = self.processes[process_id]

        unblocked_tasks_id = process.notify(task_id)

        unblocked_tasks_info = RL_Scheduler.get_task_weight_info(process, unblocked_tasks_id)

        for task_id in unblocked_tasks_id:
            task_classification = self.tasks_classification[task_id]
            if task_classification in self.ready_tasks_classification.keys():
                self.ready_tasks_classification[task_classification] += 1
            else:
                self.ready_tasks_classification[task_classification] = 1

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
        machine_performance_info = util.MachinePerformanceInfo(machine_info, machine.get_power()/ machine.get_cost())
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

    def _reset(self):
        self._setup()
