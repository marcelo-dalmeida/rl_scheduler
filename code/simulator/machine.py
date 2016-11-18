__author__ = 'Marcelo d\'Almeida'

import random
import threading
import time

from code.utils.notifier import Notifier

from code.utils import util


class Machine:
    '''
    Representation of the machine. It is responsible to run the tasks from the processes and to notify the scheduler
    about it.
    It creates threads to run task objects
    Each machine has its own information of power of processing, cost, and delay
    It can generate a report about the all work done
    '''

    def __init__(self, id, name, thread_quantity, power, cost, delay):
        self._id = id
        self._name = name
        self._thread_quantity = thread_quantity

        self._power = power
        self._cost = cost
        self._delay = delay

        self._thread = {}

        for i in range(0, self._thread_quantity):
            thread_id = random.randint(0, 1000000000)
            self._thread[thread_id] = None

        self._scheduler_notifier = None

        self._setup()


    def _setup(self):
        self._total_power = 0
        self._total_cost = 0
        self._total_delay = 0
        self._total_time = 0

        self._available_threads_id = []

        for thread_id in self._thread.values():
            self._available_threads_id.append(thread_id)

    def start(self,  task, thread_id):
        notifier = Notifier(self)
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

    def unsubscribe(self):
        self._scheduler_notifier = None

    def is_thread_available(self, thread_id):
        return self._thread[thread_id] is None or not self._thread[thread_id].isAlive()

    def is_any_thread_available(self):
        return len(self._available_threads_id) > 0

    def notify(self, notification):
        '''
        The thread notifies the machine so it can updates the information about power, cost, and time. It also list the
        thread as available.
        :param notification:
        '''

        thread_id = notification[0]
        notification_info = notification[1]

        self._total_power += notification_info.total_power
        self._total_cost += notification_info.total_cost
        self._total_delay += notification_info.total_delay
        self._total_time += notification_info.total_time

        self._available_threads_id.append(thread_id)

    def report(self):
        return util.MachineReport(self._name, self._total_power, self._total_cost, self._total_delay, self._total_time)

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

    def reset(self):
        self._setup()



    class MachineThread(threading.Thread):
        '''
        Thread. The one that runs it all.
        '''

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
            self._total_delay = 0
            self._total_time = 0


        def start(self, task_package):
            self._running_task_package = task_package
            self._machine_info = util.MachineInfo(self._machine_id, self._thread_id)
            threading.Thread.start(self)


        def run(self):
            '''
            Runs the thread to execute and notify.
            Notifies the scheduler that the task is finished so it can updates the process and its scheduling.
            Notifies the machine so it can update the resources used
            '''
            print("Starting " + self.name)
            self.execute()
            thread_report = util.MachineReport(self._name, self._total_power, self._total_cost, self._total_delay, self._total_time)
            self._scheduler_notifier.notify(self._running_task_package.task_info, self._machine_info, thread_report)
            self._machine_notifier.notify(self._thread_id, thread_report)
            print("Exiting " + self.name)

        def execute(self):
            '''
            Simulates the execution of the tasks, consuming the task power left
            :return:
            '''
            task = self._running_task_package.task
            remaining_power = task.get_power()
            start_time = time.process_time()
            time.sleep(self._delay)
            self._total_delay = self._delay
            while remaining_power > 0:
                print("%s, %s - %s (%s): %s" % (self._name, self._thread_id, task.get_name(), remaining_power, time.ctime(time.time())))

                if self._power > remaining_power:
                    remaining_power = 0
                else:
                    remaining_power -= self._power

            total_time = time.process_time() - start_time
            self._total_power = task.get_power()
            self._total_cost = self._cost * total_time
            self._total_time = total_time


        def subscribe(self, notifier):
            self._machine_notifier = notifier

        def unsubscribe(self):
            self._machine_notifier = None

