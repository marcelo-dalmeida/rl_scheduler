__author__ = 'Marcelo d\'Almeida'

'''
 This is the Main.
 Setup the machines, processes, and the scheduler.
'''

from scheduler.rl_scheduler import RL_Scheduler
from scheduler.scheduler import Scheduler
from simulator.machine import Machine
from simulator.process import Process
from simulator.task import Task

machine1 = Machine("1", "Machine 1", thread_quantity=1, power=5, cost=10, delay=1)
machine2 = Machine("2", "Machine 2", thread_quantity=1, power=3.5, cost=5, delay=1)
machine3 = Machine("3", "Machine 3", thread_quantity=1, power=8.3, cost=11, delay=1)


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

machines = [machine1, machine2, machine3]
processes = [process_a, process_b, process_c, process_d]

scheduler = RL_Scheduler(machines, processes, 1)
scheduler.schedule()

#scheduler = Scheduler(machines, processes)
#scheduler.schedule()

