# ADR 03: Queue-based WOD Creation – Choices and Simple Improvements

## What We Did (Not Required by Assignment)

- **Used Pydantic for Validation:**  
  We check messages before sending them to make sure they have the right data.

- **Made Messages Persistent:**  
  Messages are saved to disk so they don’t get lost if RabbitMQ restarts.

- **Dead Letter Queue (DLQ):**  
  Failed messages go to a special queue so we can see what went wrong.

- **Retry Tracking:**  
  We keep track of how many times a message was retried.

- **Kept Code Organized:**  
  Different parts (queue setup, validation, consumer) are in their own functions/files.

## How We Could Make It Even Better

- **Add Logging and Monitoring:**  
  Use tools to watch for errors and see what’s happening in real time.

- **Alert on Too Many Failures:**  
  Get notified if lots of messages end up in the DLQ.

- **Retry with Delays:**  
  Wait a bit before retrying failed messages, instead of retrying right away.

- **Avoid Duplicates:**  
  Add a unique ID to each message so we don’t process the same job twice.

- **Easier Message Updates:**  
  Use a shared format for messages so changes are easier to manage.

- **Shut Down Consumers Safely:**  
  Make sure consumers finish their work before stopping.

- **Run More Consumers:**  
  Start more consumers if we need to handle more jobs.

- **DLQ Tools:**  
  Make it easy to see and retry failed messages.