__author__ = 'Marcelo d\'Almeida'


class Notifier:

    def __init__(self, subject):
        self._subject = subject

    def notify(self, *notification):
        self._subject.notify(notification)
