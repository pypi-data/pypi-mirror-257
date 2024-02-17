import asyncio as _asyncio


def schedule_task(self, func, *args, **kwargs):
    '''The `schedule_task` function adds a task to a set of background tasks and schedules it to be
    executed asynchronously.

    Parameters
    ----------
    func
        The `func` parameter is the function that you want to schedule as a background task. It should be a
    callable object, such as a function or a method.

    '''
    if not hasattr(self, "background_tasks"):
        self.background_tasks = set()
    task = _asyncio.create_task(func(*args, **kwargs))
    task.add_done_callback(self.background_tasks.discard)
    self.background_tasks.add(task)