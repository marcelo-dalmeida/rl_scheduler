__author__ = 'Marcelo d\'Almeida'


class Task(object):

    def __init__(self, id, power, name=None):
        self._id = id

        self._process_id = None

        if name is None:
            self._name = id
        else:
            self._name = name

        self._power = power

    def set_process_id(self, process_id):
        if self._process_id is None:
            self._process_id = process_id
        else:
            raise Exception("Task already has process id")

    def get_id(self):
        return self._id

    def get_process_id(self):
        return self._process_id

    def get_name(self):
        return self._name

    def get_power(self):
        return self._power

    def __repr__(self):
        return self._name