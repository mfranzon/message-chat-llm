# FAQ

## How change `/?` to the other prefix? 
To change the default messages/prefix just set the new value to `src/env.py` file.
Defaults:
```
# To get your ollama installed models: `ollama list`.
# And type model to parameter below:
MODEL_NAME = 'llama3.2:1b'  # e.g: mistral

PORT = 5555
PREFIX = '/?'
WELCOME_MSG = f'Welcome to the chat!\nType your message or ask a LLM with {PREFIX} <question>'
ASK_MSG = 'Asking...'
SUCCESS_MSG = 'All participants have successfully received a response.'
```
