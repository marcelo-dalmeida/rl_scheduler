__author__ = 'Marcelo d\'Almeida'

from process import Process
from task import Task
from machine import Machine
from scheduler import Scheduler

machine1 = Machine("1", "Machine 1", thread_quantity=2, power=5, cost=10, delay=1)
machine2 = Machine("2", "Machine 2", thread_quantity=2, power=3.5, cost=5, delay=1)

machine3 = Machine("3", "Machine 3", thread_quantity=2, power=8.3, cost=11, delay=1)

process_a = Process("a")
process_b = Process("b")
process_c = Process("c")

process_a.add(Task("a1", 40), [])
process_a.add(Task("a2", 50), ["a1"])
process_a.add(Task("a3", 38), ["a2"])
process_a.add(Task("a4", 15), ["a3"])

process_b.add(Task("b1", 30), [])
process_b.add(Task("b2", 20), ["b1"])
process_b.add(Task("b3", 15), ["b2"])
process_b.add(Task("b4", 21), ["b3"])
process_b.add(Task("b5", 2), ["b4"])
process_b.add(Task("b6", 5), ["b5"])

process_c.add(Task("c1", 23), [])
process_c.add(Task("c2", 35), ["c1"])
process_c.add(Task("c3", 20), ["c2"])
process_c.add(Task("c4", 12), ["c3"])
process_c.add(Task("c5", 10), ["c4"])

machines = [machine1, machine2]
processes = [process_a, process_b, process_c]

scheduler = Scheduler(machines, processes)
scheduler.schedule()

