__author__ = 'Marcelo d\'Almeida'

import util

class Process:
    '''
    It is the representation of the process. It is defined by a list of tasks and some structures to manage statuses
    and dependency between them.
    It also contains the total of power (work needed) to finish all the tasks and some notion of normalized power to
    express the average task power.
    '''
    def __init__(self, id, name=None):
        self._id = id

        if name is None:
            self._name = id
        else:
            self._name = name

        self._tasks = {}
        self._dependencies = {}
        self._blocked_by = {}
        self._status = {}
        self._available_tasks_id = []
        self._finished_count = 0

        self._total_power = 0
        self._normalized_power = 0

    def add(self, task, dependencies):
        '''
        Updates the status of the new task, the dependencies graph, the available list, and the process total power.
        :param task:
        :param dependencies: other tasks that the the task depends on it
        :return:
        '''
        task.set_process_id(self._id)

        self._tasks[task.get_id()] = task
        self._dependencies[task.get_id()] = dependencies

        if len(dependencies) == 0:
            self._status[task.get_id()] = util.READY
        else:
            self._status[task.get_id()] = util.BLOCKED

        for dependency in dependencies:
            if dependency in self._blocked_by.keys():
                self._blocked_by[dependency].append(task.get_id())
            else:
                self._blocked_by[dependency] = [task.get_id()]

        if self._status[task.get_id()] is util.READY:
            self._available_tasks_id.append(task.get_id())

        self._total_power += task.get_power()
        self._set_normalized_power()

    def get_task(self, task_id):
        '''
        This method is intended to only make the access to the task possible, if it is intended to run it
        :param task_id:
        :return task:
        '''
        if self._status[task_id] == util.READY:
            task = self._tasks[task_id]
            self._status[task_id] = util.RUNNING
            self._total_power -= task.get_power()
            self._set_normalized_power()
        else:
            task = None

        return task

    def notify(self, task_id):
        '''
        The process is being notified that the task is finished.
        It updates tha status to FINISHED and updates all the tasks that have this task as dependency..
        :param task_id:
        :return: unblocked_tasks, tasks that were unblocked by the event of finishing the task
        '''
        if self._status[task_id] is util.READY:
            self._available_tasks_id.remove(task_id)
            self._status[task_id] = util.FINISHED

            self._finished_count += 1

            if task_id not in self._blocked_by:
                return []

            blocked_tasks = self._blocked_by[task_id]
            unblocked_tasks = []

            for blocked_task_id in blocked_tasks:
                self._dependencies[blocked_task_id].remove(task_id)
                if len(self._dependencies[blocked_task_id]) == 0:
                    unblocked_tasks.append(blocked_task_id)
                    self._status[blocked_task_id] = util.READY
                    self._available_tasks_id.append(blocked_task_id)

            return unblocked_tasks

        else:
            raise("This task is not " + util.READY)

    def is_finished(self):
        return len(self._tasks) - self._finished_count == 0

    def _set_normalized_power(self):
        if len(self._tasks) != 0:
            self._normalized_power = self._total_power / len(self._tasks)
        else:
            self._normalized_power = 0

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_available_tasks_id(self):
        return self._available_tasks_id

    def get_total_power(self):
        return self._total_power

    def get_normalized_power(self):
        return self._normalized_power

    def __repr__(self):
        return self._name
