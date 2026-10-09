from asyncio import Task

from django.db import tasks


class task(tasks.Task):
    name = Task.CharField()
    description = Task.TextField()

    def __str__(self):
        return self.title
