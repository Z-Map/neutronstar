# -*- coding: utf-8 -*-
""" Error module
"""

class NeutronException(Exception):
    """NeutronException are the base class of all neutronstar module exception"""

    def __init__(self, message):
        """message will be displayed when exception is raised"""
        super(NeutronException, self).__init__()
        self.message = message

    def __str__(self):
        return self.message

class TaskError(NeutronException):

    """TaskError represent an error raised during the execution of a target"""
    def __init__(self, task_type, task_name, task_error, task_trace=None):
        super(TaskError, self).__init__(
            "Task {} of type {} failed with return {}".format(task_name,
                task_type, task_error))
        if isinstance(task_error, TaskError):
            self.task_trace = [task_error.task_info] + task_error.task_trace
            task_error = None
        else:
            self.task_trace  = task_trace if task_trace else []
        self.task_info = (task_type, task_name, task_error)

    def __bool__(self):
        return False
