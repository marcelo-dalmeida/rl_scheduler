__author__ = 'Marcelo d\'Almeida'

import datetime
import string
import math

from code.simulator.process import Process
from code.simulator.task import Task


def get_letter(letter_number):

    #for letter_number in range(1, 18279 + 1):
    #for letter_number in range(702, 18278 + 1):
    #for letter_number in range(27, 702 + 1):
    #for letter_number in range(1, 26 + 1):

    letter_number += 1

    letters = ""
    position = 0
    end = 0

    original = letter_number

    #print('letter_number', letter_number)

    while not letter_number <= end:
        position += 1
        end = pow(26, position) + end


    while position > 0:

        p = pow(26, position - 1)
        l = math.floor(letter_number/p)

        h = letter_number%p

        end = 0
        for i in range(0, position-1):
            end += pow(26, i)

        if h < end:
            l -= 1

        letters += string.ascii_lowercase[l-1]

        letter_number -= p*l
        position -= 1


    #print(letters)

    total = 0
    position = len(letters) - 1
    for letter in letters:
        letter = [ord(char) - 96 for char in letter][0]
        total += letter * pow(26, position)
        position -= 1

    if total != original:
        print("original", original)
        print("total", total)
        raise Exception("Check your letter naming algorithm")

    return letters




def handle_task_input(gflops=None):

    input = open("info/input/input.txt", "r")
    processes = []

    input.readline()

    #processes
    for letter_number, line in enumerate(input.readlines()):

        letters = get_letter(letter_number)

        timestamps = line.split(";")

        task_package = []

        previous_id = None

        number = 1
        #tasks
        for t in range(1, len(timestamps), 2):
            start_time = timestamps[t-1]
            stop_time = timestamps[t]

            start_time = start_time[1:start_time.index("-", 10)]
            stop_time = stop_time[1:stop_time.index("-", 10)]

            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
            stop_time = datetime.datetime.strptime(stop_time, "%Y-%m-%d %H:%M:%S.%f")
            deltatime = stop_time - start_time
            power_needed = deltatime.total_seconds()*gflops

            id = letters+str(number)

            if previous_id is None:
                dependencies = []
            else:
                dependencies = [previous_id]

            previous_id = id

            task_package.append( (Task(id, power_needed), dependencies) )

            number += 1

        process = Process(letters, task_package=task_package)
        processes.append(process)

    #remove header
    processes = processes[1:]

    return processes




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
