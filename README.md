---
title: redq
---

[![image](https://img.shields.io/pypi/v/redq.svg)](https://pypi.python.org/pypi/redq)

[![image](https://img.shields.io/travis/yusufadell/redq.svg)](https://travis-ci.com/yusufadell/redq)

[![Documentation Status](https://readthedocs.org/projects/redq/badge/?version=latest)](https://redq.readthedocs.io/en/latest/?version=latest)

Distributed background task queue for Python, powered by Redis protocol.

- Free software: GNU General Public License v3
- Documentation: <https://redq.readthedocs.io>.

## Example

```python

    from redq import CronTask, redq, Queue

    redq = redq(
        queues=[
            (0, "a-high-priority-queue"),
            (1, "a-medium-priority-queue"),
            (2, "a-low-priority-queue"),
            "default-lowest-priority-queue",
            Queue("another-queue", priority=3),
        ],
    )

    # Number of worker processes. Must be an int or str which evaluates to an
    # int. The variable "cores" is replaced with the number of processors on
    # the current machine.
    concurrency = ("cores*4",)

    schedules = (
        [
            # Runs mytask on the queue with priority 1.
            CronTask(
                "* * * * *",
                "mytask",
                queue="a-medium-priority-queue",
                args=[2, 2],
                kwargs={},
            ),
            # Runs mytask once every 5 minutes.
            ("*/5 * * * *", "mytask", [1, 1], {}),
            # Runs anothertask on the default lowest priority queue.
            ("*/10 * * * *", "anothertask"),
        ],
    )


    @redq.task(queue="medium-priority-queue")
    def mytask(x, y):
        print(x + y)


    @redq.task
    def anothertask():
        print("hello world")


    if __name__ == "__main__":
        # add 1 plus 1 on a worker somewhere, overwriting the task's queue from medium to high
        mytask.delay(1, 1, queue="a-high-priority-queue")
        # add 1 plus 1 on a worker somewhere, running on the default lowest priority queue
        anothertask.delay()
```

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
