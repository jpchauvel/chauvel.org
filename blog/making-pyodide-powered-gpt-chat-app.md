---
blogpost: true
date: 12 Mar, 2025
author: hellhound
location: Lima, Perú
category: OpenAI
tags: pyodide, openai, gpt, httpx, python
language: English
---

# Creating a Pyodide-Powered GPT-3.5 Turbo Chat Application: A Proof-of-Concept

![OpenAI](/_static/images/openai.png){ align=center width=400px }

Building a web-based application that leverages both the Python environment and
OpenAI's GPT-3.5 Turbo language model can be an exciting endeavor. This article
walks through the creation of a proof-of-concept chat application using
Pyodide, a tool that allows Python to run in the web browser, and integrating
it with GPT-3.5 Turbo to simulate an intelligent conversational agent.

## The Landscape of Pyodide and GPT-3.5 Turbo Integration

With the capability to run Python directly in web browsers, Pyodide provides an
exciting opportunity to bring the powerful capabilities of Python-based
libraries directly to client-side applications. This includes applications that
can benefit from being close to users, such as interactive tools and data
visualization dashboards.

This proof-of-concept integrates Pyodide with OpenAI's GPT-3.5 Turbo model,
which provides the ability to simulate a human-like conversation. Below, I will
take you through each component of this application, explaining its
functionality, integration techniques, and the rationale behind each choice.

## Components Breakdown

The application is composed of several key files and technologies, including
HTML, JavaScript, and Python integrated via Pyodide. Let's break down these
components step-by-step.

### HTML: Structuring the Interface

The HTML file sets up the basic user interface for the chat application:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pyodide Chat App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: auto;
            padding: 20px;
        }
        #chatbox {
            border: 1px solid #ccc;
            height: 300px;
            overflow-y: scroll;
            padding: 10px;
            margin-bottom: 10px;
        }
        #user-input {
            width: calc(100% - 70px);
        }
        #send-button {
            width: 60px;
        }
    </style>
</head>
<body>

<!-- Pyodide setup logic will insert content here -->
<script src="https://cdn.jsdelivr.net/pyodide/v0.27.3/full/pyodide.js"></script>
<script src="python.js"></script>
</body>
</html>
```

This HTML layout creates a basic interface with a chatbox and user input
control, wrapped in simple CSS to style the appearance. The Pyodide setup is
managed by a JavaScript file that we will explore shortly.

### JavaScript: Bootstrapping Pyodide and Linking Frontend to Backend

JavaScript is employed to set up the Pyodide environment and connect the
frontend UI to the Python backend. Here's the JavaScript bootstrapping file:

#### `python.js`

```javascript
async function setupPyodide() {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage("micropip");

    // JavaScript functions to register with the Python environment
    const jsModule = {
        async displayResponse(response) {
            const chatbox = document.getElementById("chatbox");
            chatbox.innerHTML += `<div><strong>AI:</strong> ${response}</div>`;
        }
    };

    pyodide.registerJsModule("js_module", jsModule);

    await pyodide.runPythonAsync(`
        import micropip
        import os
        from pyodide.http import pyfetch

        response = await pyfetch("app.tar.gz")
        await response.unpack_archive()

        await micropip.install('https://raw.githubusercontent.com/psymbio/pyodide_wheels/main/multidict/multidict-4.7.6-py3-none-any.whl', keep_going=True)
        await micropip.install('https://raw.githubusercontent.com/psymbio/pyodide_wheels/main/frozenlist/frozenlist-1.4.0-py3-none-any.whl', keep_going=True)
        await micropip.install('https://raw.githubusercontent.com/psymbio/pyodide_wheels/main/aiohttp/aiohttp-4.0.0a2.dev0-py3-none-any.whl', keep_going=True)
        await micropip.install('https://raw.githubusercontent.com/psymbio/pyodide_wheels/main/openai/openai-1.3.7-py3-none-any.whl', keep_going=True)
        await micropip.install('https://raw.githubusercontent.com/psymbio/pyodide_wheels/main/urllib3/urllib3-2.1.0-py3-none-any.whl', keep_going=True)
        await micropip.install("ssl")
        import ssl
        await micropip.install("httpx", keep_going=True)
        import httpx
        await micropip.install('https://raw.githubusercontent.com/psymbio/pyodide_wheels/main/urllib3/urllib3-2.1.0-py3-none-any.whl', keep_going=True)
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        from main import sender_message_proxy
    `);
    
    // Prompt the user for the OpenAI API key
    const apiKey = window.prompt("Please enter your OpenAI API key:");

    // Add the HTML content after Pyodide setup.
    document.body.innerHTML += `
        <h1>Pyodide Chat with AI Assistant</h1>
        <div id="chatbox"></div>
        <input type="text" id="user-input" placeholder="Type your message...">
        <button id="send-button">Send</button>
    `;

    const sendMessageToPython = pyodide.globals.get("sender_message_proxy");

    // Add event listener to send button
    document.getElementById("send-button").addEventListener("click", () => {
        const userInput = document.getElementById("user-input").value;
        document.getElementById("user-input").value = "";
        const chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;

        sendMessageToPython(apiKey, userInput);
    });

    // Add event listener for the Enter key on the input field
    document.getElementById("user-input").addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            document.getElementById("send-button").click();
        }
    });

    await pyodide.runPythonAsync(`
        from main import main as py_main

        await py_main()
    `);
}

document.addEventListener("DOMContentLoaded", function() {
    setupPyodide();
});
```

#### Key Aspects of JavaScript Code

- **Initialization of Pyodide**: The script initializes the Pyodide environment
  and ensures that necessary Python packages are available via `micropip`.

- **API Key Prompting**: To ensure interaction with GPT-3.5 Turbo, an API key
  is required. This is fetched via a browser prompt when the application first
loads.

- **JavaScript-Python Interoperability**: By using `pyodide.registerJsModule`,
  we create a bridge between JavaScript and Python. This enables Python to call
a JavaScript function (`displayResponse`), which updates the chat box with
responses from GPT-3.5 Turbo.

- **Loading Backend Logic**: The backend logic is encapsulated in Python and
  integrated via `pyodide.runPythonAsync`. This allows modules defined in
Python to be transparent to JavaScript as synchronous functions.

### Python: Handling Conversations with GPT-3.5 Turbo

The heart of the application involves a series of Python components that manage
communication with the OpenAI API:

#### Python Backend (`main.py`)

```python
import asyncio
import json
from urllib.parse import quote_plus

import httpx
import openai
from pyodide.ffi import create_proxy
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import js_module


class URLLib3Transport(httpx.AsyncBaseTransport):
    def __init__(self) -> None:
        self.pool = urllib3.PoolManager()

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8").replace("'", '"'))
        urllib3_response = self.pool.request(
            request.method,
            str(request.url),
            headers=request.headers,
            json=payload,
        )
        content = json.loads(
            urllib3_response.data.decode("utf-8")
        )
        stream = httpx.ByteStream(
            json.dumps(content).encode("utf-8")
        )
        headers = [(b"content-type", b"application/json")]
        return httpx.Response(200, headers=headers, stream=stream)


client: httpx.AsyncClient = httpx.AsyncClient(transport=URLLib3Transport())
openai_client: openai.AsyncOpenAI = openai.AsyncOpenAI(
    base_url="https://api.openai.com/v1/", api_key="", http_client=client
)
message_queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
loop: asyncio.AbstractEventLoop | None = None


async def handle_message(api_key: str, message: str) -> None:
    openai_client.api_key = api_key
    response = await openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": quote_plus(message),
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=4096,
        temperature=0.2,
    )
    await js_module.displayResponse(response.choices[0].message.content)


async def receiver() -> None:
    while True:
        api_key, message = await message_queue.get()
        await handle_message(api_key, message)


def sender(api_key: str, message: str) -> None:
    message_queue.put_nowait((api_key, message))


async def main() -> None:
    global loop

    loop = asyncio.get_running_loop()
    loop.create_task(receiver())
    while True:
        await asyncio.sleep(0.1)


sender_message_proxy = create_proxy(sender)
```

#### Core Functionality

- **Custom Transport Layer**: A custom `URLLib3Transport` class implements
  `httpx.AsyncBaseTransport` to handle network requests without relying on
JavaScript native fetch API. This layer allows flexible management of HTTP
requests, including retry logic and session management.

- **Async Event Loop**: By utilizing `asyncio`, the application can efficiently
  manage asynchronous tasks, ensuring the application remains responsive, even
when dealing with slow network interactions.

- **Message Handling**: The `handle_message` function manages the interaction
  with the OpenAI API. It constructs a request using user input, sends it to
GPT-3.5 Turbo, and returns the AI's response to the frontend via the
`displayResponse` function provided in `jsModule`.

- **Bridging with JavaScript**: The `sender_message_proxy` is a
  Pyodide-provided bridge that allows JavaScript to enqueue messages to be
processed by the Python event loop.

### Rationale and Alternatives

- **URLLib3Transport**: The choice of using a custom transport instead of
  higher-level HTTP clients like `requests` becomes necessary due to Pyodide's
limitations with network requests, as in the [GitHub issue
solution](https://github.com/pyodide/pyodide/issues/4292#issuecomment-1848861037).
This workaround allows greater flexibility and compatibility within the web
environment Pyodide operates in.

- **Interactive Interface Design**: While the user interface remains minimalist
  in this PoC, it meets current goals while leaving room for enhancement with
richer interactions, styling, or multi-user support.

### Challenges and Considerations

Building this application comes with a unique set of challenges:
- **Security**: Managing an API key within a client-side application poses
  security risks. Users must exercise caution and potentially employ
server-side proxies for any live deployment.

- **Performance**: Browser limitations and Pyodide's alpha status imply
  performance constraints. It's advisable for this to remain in PoC status
pending further optimization.

- **Installation Overhead**: The necessity of bundling Python wheel files makes
  the initial loading process cumbersome. Techniques to streamline package
delivery to clients might need exploration.

## Conclusion

The application described here showcases the possibilities of combining Pyodide
and GPT-3 within a web-based environment, delivering an interactive interface
to experiment with AI capabilities. While it remains a proof-of-concept, it
opens the door to further iterations towards a robust, production-ready
application.

````{note}
You can find the complete code here: https://github.com/jpchauvel/pyodide-chat-gpt

```{raw} html
<a class="reference internal" href="/blog/pyodide-chat-gpt/">
    <span class="xref myst">Try it now!</span>
</a>

```
````
