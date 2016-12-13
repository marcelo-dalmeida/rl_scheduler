__author__ = 'Marcelo d\'Almeida'

'''
 This is the Main.
 Setup the machines, processes, and the scheduler.
'''

import sys

from code.scheduler.rl_scheduler import RL_Scheduler

from code.simulator.machine import Machine
from code.simulator.process import Process
from code.simulator.task import Task
from code.utils.logger import Logger
from code.utils.util import handle_task_input



sys.stdout = Logger()

processes = handle_task_input(gflops=20)

machine1 = Machine("1", "Machine 1", thread_quantity=1, power=10, cost=0.226, delay=1)
machine2 = Machine("2", "Machine 2", thread_quantity=1, power=10, cost=0.226, delay=1)
machine3 = Machine("3", "Machine 3", thread_quantity=1, power=10, cost=0.226, delay=1)
machine4 = Machine("4", "Machine 4", thread_quantity=1, power=20, cost=0.532, delay=1)
machine5 = Machine("5", "Machine 5", thread_quantity=1, power=20, cost=0.532, delay=1)
machine6 = Machine("6", "Machine 6", thread_quantity=1, power=20, cost=0.532, delay=1)
machine7 = Machine("7", "Machine 7", thread_quantity=1, power=30, cost=0.913, delay=1)
machine8 = Machine("8", "Machine 8", thread_quantity=1, power=30, cost=0.913, delay=1)
machine9 = Machine("9", "Machine 9", thread_quantity=1, power=30, cost=0.913, delay=1)


process_a_task_package = [(Task("a1", 40), []),
                          (Task("a2", 50), ["a1"]),
                          (Task("a3", 38), ["a2"]),
                          (Task("a4", 15), ["a3"])]

process_b_task_package = [(Task("b1", 30), []),
                          (Task("b2", 20), ["b1"]),
                          (Task("b3", 15), ["b2"]),
                          (Task("b4", 21), ["b3"]),
                          (Task("b5", 2), ["b4"]),
                          (Task("b6", 5), ["b5"])]

process_c_task_package = [(Task("c1", 23), []),
                          (Task("c2", 35), ["c1"]),
                          (Task("c3", 20), ["c2"]),
                          (Task("c4", 12), ["c3"]),
                          (Task("c5", 10), ["c4"])]

process_d_task_package = [(Task("d1", 23), []),
                          (Task("d2", 12), ["d1"]),
                          (Task("d3", 8), ["d2"]),
                          (Task("d4", 12), ["d3"]),
                          (Task("d5", 23), ["d4"])]

process_a = Process("a", task_package=process_a_task_package)
process_b = Process("b", task_package=process_b_task_package)
process_c = Process("c", task_package=process_c_task_package)
process_d = Process("d", task_package=process_d_task_package)

machines = [machine1, machine2, machine3, machine4, machine5, machine6, machine7, machine8, machine9]
#processes = [process_a, process_b, process_c, process_d]

print(processes)

scheduler = RL_Scheduler(machines, processes, epochs=100)
scheduler.schedule()

#scheduler = Scheduler(machines, processes)
#scheduler.schedule()
