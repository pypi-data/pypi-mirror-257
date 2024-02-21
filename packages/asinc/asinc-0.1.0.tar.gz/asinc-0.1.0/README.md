# Asyncio util library

## periodic_call
Allows periodically execute an awaitable incorruptible with event.

```python
import signal
import asyncio
from asinc import periodic_call


async def run():
    stop_event = asyncio.Event()
    signal.signal(signal.SIGINT, lambda: stop_event.set())
    
    await periodic_call(lambda: asyncio.sleep(1), stop_event, 10)
```