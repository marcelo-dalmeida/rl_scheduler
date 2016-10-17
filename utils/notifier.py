__author__ = 'Marcelo d\'Almeida'


class Notifier:
    '''
    This is the Notifier.
    A way of creating communication between objects without making the object available to the other class.
    '''

    def __init__(self, subject):
        '''
        When you want to pass specific information to a second object, the first object creates a Notifier object passing
        itself and passes this Notifier object to the object which the communication is desired (the second one).
        The recommended way is to create methods 'subscribe' and 'unsubscribe' in the class that is going to notify
        (the second one), so it is clear that the other object is going to notify one or more notifier objects.
        '''
        self._subject = subject


    def notify(self, *notification):
        '''
        Pass information that you want let the other object know or simply flag to him that some process is done
        '''
        self._subject.notify(notification)
