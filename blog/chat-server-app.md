---
blogpost: true
date: 24 Apr, 2024
author: hellhound
location: Lima, Perú
category: Server
tags: server, chat, redis, pubsub, websockets, python
language: English
---
# Creating Your Own Small Scale Server Application Using PubSub Pattern

I recently had the idea to develop a small proof-of-concept server application
using the built-in pub/sub functionality of Redis, and decided to get started on
it.

So the first step involved listing my dependencies, and, oh boy, there were
quite a few for such a small app!

- `fastapi`: The framework I chose to expose the websocket endpoint.
- `click`: This package was required to capture simple command line options.
- `websockets`: This one was required to handle websocket communication between
  the server and the clients.
- `redis.asyncio`: This is basically the same as `redis` but for `asyncio`
  integration. It's needed to expose the pub/sub functionality.
- `uvicorn`: And finally, the ASGI web server to run the FastAPI application.

## The First Steps

First we need a FastAPI boilerplate code, like so:

```python
#!/usr/bin/env python3
import logging

import click
import uvicorn
from fastapi import FastAPI

app = FastAPI()

global_room = "global_room"

logging.basicConfig(level=logging.INFO)


@app.websocket("/chat/{nickname}")
async def main_chat_handler(websocket: WebSocket, nickname: str):
    ...


@click.command()
@click.option("--host", default="0.0.0.0", help="Host to run the server on")
@click.option("--port", default=8000, help="Port to run the server on")
@click.option("--redis", default="localhost", help="Redis host")
def run_server(host, port, redis):
    app.redis = redis
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
```

This code is quite mouthful by itself, so I'll do my best explaining what it
does. The first thing we do is to initialize the FastAPI global singleton. Then
I define the `main_chat_handle()` endpoint which is going to be where the main
logic of the chat is located. It receives two parameters: `websocket` and
`nickname`. The websocket is required by FastAPI and it's the one used by the
framework to handle the communication between the server and the client. The
nickname is the "handle" the user specifies when she/he connects to the
websocket.

Then the `run_server()` function is the entry point of the module and all it
does is to pass the redis host, the host and the port of the chat server to the
FastAPI singleton and to the uvicorn instance, respectively and then run the
ASGI web server.

## The Main Handler

Now it's time to define a special helper function that will allow us to get the
redis client:

```python
import redis.asyncio as redis


async def get_redis_client(host: str = "localhost"):
    return await redis.from_url(f"redis://{host}")
```

I will not go into details on how the Redis' pub/sub work. You can see how it's
done by checking this code snippet that I extracted from `redis-py`
documentation:

```python
import asyncio

import redis.asyncio as redis

STOPWORD = "STOP"


async def reader(channel: redis.client.PubSub):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            print(f"(Reader) Message Received: {message}")
            if message["data"].decode() == STOPWORD:
                print("(Reader) STOP")
                break

r = redis.from_url("redis://localhost")
async with r.pubsub() as pubsub:
    await pubsub.subscribe("channel:1", "channel:2")

    future = asyncio.create_task(reader(pubsub))

    await r.publish("channel:1", "Hello")
    await r.publish("channel:2", "World")
    await r.publish("channel:1", STOPWORD)

    await future
```

So for the main handler, the code would look like this:

```python
@app.websocket("/chat/{nickname}")
async def main_chat_handler(websocket: WebSocket, nickname: str):
    logging.info(f"User {nickname} joined the chat")
    client = await get_redis_client(app.redis)

    try:
        await websocket.accept()

        async with client.pubsub() as pubsub:
            await pubsub.subscribe(global_room)

            reader_future = asyncio.create_task(
                chat_reader(pubsub, websocket, nickname)
            )
            publisher_future = asyncio.create_task(
                chat_publisher(client, websocket, nickname)
            )
            await publisher_future
            await reader_future
    except WebSocketDisconnect:
        logging.info(f"User {nickname} is disconnecting...")
```

As you can see, we first accept the socket connection and then we start the
pub/sub instance by subscribing to our global room, which is going to be the
only channel in the pub/sub. The following steps are pretty simple: we schedule
the pub/sub reader and the pub/sub publisher, which as the same time function as
sending and receiving ends of the websocket, respectively.

If a `WebSocketDisconnect` exception ist catched, then we smoothly print the
"User X is disconnecting..." message.

## The Reader and the Publisher

These functions are pretty straightforward to understand. The reader first gets
the message from the channel and then if the nickname of the message is not the
same as the current user's nickname, then it sends the message to the websocket.

The publisher function is even more simpler: All it does is to publish any
received message from the websocket in an infinite loop.

### Reader

```python
async def chat_reader(
    channel: redis.client.PubSub, websocket: WebSocket, nickname: str
):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            message = message["data"].decode()
            data = json.loads(message)
            # Exclude messages sent by the same user
            if data["nickname"] != nickname:
                await websocket.send_text(message)
```

### Publisher

```python
async def chat_publisher(
    client: redis.client.Redis, websocket: WebSocket, nickname: str
):
    while True:
        data = await websocket.receive_text()
        await client.publish(global_room, data)
```

## Final Thoughts

In conclusion, creating a small-scale chat server app using Redis pub/sub
functionality can be a fascinating and educational project for those looking to
delve deeper into asynchronous programming and real-time messaging systems. By
leveraging the power of asyncio, FastAPI, and Redis, developers can implement a
robust chat application that facilitates seamless communication between users.
Through this tutorial, you have not only learned how to set up the server-side
logic for a chat app but also explored the intricacies of handling WebSocket
connections and message broadcasting with Redis pub/sub.

As you continue to refine and expand upon this project, remember to focus on
optimizing performance, enhancing security measures (such as authentication and
encryption), and incorporating additional features to enrich the user
experience. Embrace the iterative nature of software development, experiment
with new functionalities, and don't hesitate to seek community support or
documentation resources when faced with challenges.

Keep coding, stay curious, and let your creativity guide you in unlocking the
potential of real-time communication solutions with Redis and asyncio. Happy
coding!

```{note}
You can find the complete code here: https://github.com/jpchauvel/chat
```
