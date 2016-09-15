__author__ = 'Marcelo d\'Almeida'

from notifier import Notifier
import threading
import time
import random
import util

class Machine:

    def __init__(self, id, name, thread_quantity, power, cost, delay):
        self._id = id
        self._name = name
        self._thread_quantity = thread_quantity

        self._power = power
        self._cost = cost
        self._delay = delay

        self._thread = {}
        self._scheduler_notifier = None

        self._total_power = 0
        self._total_cost = 0
        self._total_time = 0

        self._available_threads_id = []

        for i in range(0, thread_quantity):
            thread_id = random.randint(0, 1000000000)
            self._thread[thread_id] = None
            self._available_threads_id.append(thread_id)


    def start(self,  task, thread_id):
        notifier = Notifier(self)
        #thread_id = self._available_threads_id.pop(0)
        self._thread[thread_id] = self.MachineThread(self._id, thread_id, self._name, self._power, self._cost, self._delay, self._scheduler_notifier)
        self._thread[thread_id].subscribe(notifier)
        self._thread[thread_id].start(task)

    def threads_join(self):
        for thread in self._thread.values():
            if thread is not None:
                thread.join()

    def thread_join(self, thread_id):
        self._thread[thread_id].join()

    def subscribe(self, notifier):
        self._scheduler_notifier = notifier

    def is_thread_available(self, thread_id):
        return self._thread[thread_id] is None or not self._thread[thread_id].isAlive()

    def is_any_thread_available(self):
        return len(self._available_threads_id) > 0

    def notify(self, notification):
        thread_id = notification[0]
        notification_info = notification[1]

        self._total_power += notification_info.total_power
        self._total_cost += notification_info.total_cost
        self._total_time += notification_info.total_time

        self._available_threads_id.append(thread_id)

    def report(self):
        return util.MachineReport(self._name, self._total_power, self._total_cost, self._total_time)

    def get_id(self):
        return self._id

    def get_available_thread_id(self):
        return self._available_threads_id

    def get_name(self):
        return self._name

    def get_power(self):
        return self._power

    def get_cost(self):
        return self._cost

    def get_delay(self):
        return self._delay


    class MachineThread(threading.Thread):

        def __init__(self, machine_id, thread_id, name, power, cost, delay, scheduler_notifier):
            threading.Thread.__init__(self)
            self._machine_id = machine_id
            self._thread_id = thread_id
            self._name = name
            self._delay = delay
            self._power = power
            self._cost = cost
            self._scheduler_notifier = scheduler_notifier
            self._machine_notifier = None
            self._running_task_package = None
            self._machine_info = None
            self._total_power = 0
            self._total_cost = 0
            self._total_time = 0


        def start(self, task_package):
            self._running_task_package = task_package
            self._machine_info = util.MachineInfo(self._machine_id, self._thread_id)
            threading.Thread.start(self)


        def run(self):
            print("Starting " + self.name)
            self.execute()
            self._scheduler_notifier.notify(self._running_task_package.task_info, self._machine_info)
            thread_report = util.MachineReport(self._name, self._total_power, self._total_cost, self._total_time)
            self._machine_notifier.notify(self._thread_id, thread_report)
            print("Exiting " + self.name)

        def execute(self):
            task = self._running_task_package.task
            remaining_power = task.get_power()
            cycles_count = 0
            while remaining_power > 0:
                time.sleep(self._delay)
                print("%s, %s - %s (%s): %s" % (self._name, self._thread_id, task.get_name(), remaining_power, time.ctime(time.time())))

                if self._power > remaining_power:
                    remaining_power = 0
                else:
                    remaining_power -= self._power
                cycles_count += 1

            self._total_power = task.get_power()
            self._total_cost = self._power * cycles_count
            self._total_time = cycles_count


        def subscribe(self, notifier):
            self._machine_notifier = notifier


