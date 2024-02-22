# Laravel Queue for Python

Currently:

- only supports reading
- only supports queues in postgres

### Read Jobs from Queue

```
from laravel-queue import Queue

connection_string = "postgresql://user:password@host:5432/db"
queue = Queue(connection_string)
queue.read()
```

#### Queue Args:

    connection: str or sqlalchemy.engine.base.Engine
    queue: str, default 'python', the queue name in the database
    jobs_table: str, default 'jobs.jobs', the table name for the jobs
    failed_jobs_table: str, default 'jobs.failed_jobs', the table name for the failed jobs
