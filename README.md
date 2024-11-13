# RedQ: A Distributed Background Task Queue for Python, powered by Redis

> It simplifies asynchronous processing by allowing you to offload time-consuming tasks to worker processes, improving application responsiveness and performance.

**Features:**

* **Simple API:** Easy to enqueue and process tasks with a straightforward interface.
* **Reliable Task Processing:** Ensures tasks are processed exactly once, even in case of failures.
* **Scalable:** Supports distributing tasks across multiple worker processes for improved throughput.
* **Lightweight:** Minimal dependencies and low overhead.
* **Powered by Redis:** Leverages the speed and efficiency of Redis for message queuing.

**Advanced Features:**

* **Task Prioritization:** Assign priorities to tasks to control their processing order.
* **Delayed Tasks:** Schedule tasks to run at a specific time in the future.
* **Error Handling:** Configure error handling and retry mechanisms for failed tasks.
* **Custom Serialization:** Use custom serialization methods for task arguments.

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

**Running Workers:**

To process tasks, you need to run a worker process. This can be done from the command line:

```bash
redq-worker --redis-host localhost --redis-port 6379 --redis-db 0
```

**Configuration:**

RedQ can be configured using environment variables or by passing arguments to the `RedQ` constructor:

* `REDIS_HOST`: Redis host address (default: localhost)
* `REDIS_PORT`: Redis port (default: 6379)
* `REDIS_DB`: Redis database number (default: 0)

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
