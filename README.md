# ai-agents-101
A repository to learn how to build ai agents and then to be able to share and teach.
I am following something similar to : https://pub.towardsai.net/i-compared-6-python-ai-agent-frameworks-so-you-dont-have-to-langgraph-vs-crewai-vs-pydanticai-vs-d8a5e6e43262 
-- OpenAI Agents SDK
-- LangGraph
-- Pydantic
-- Smolagents
-- Google ADK
-- CrewAI
- test commit

## JavaScript Setup

Install the Node.js project dependencies:

```bash
npm install
```

Set your OpenAI API key in the environment:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Run the Hello World Example

```bash
npm run hello
```

This runs `1_hello_world.mjs`, which sends a prompt to the OpenAI Responses API and prints the generated text.

## Python Setup

Create and activate a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

Install the Python requirements:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key in the environment:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Run the Python hello world example:

```bash
python 1_hello_world.py
```

This runs `1_hello_world.py`, which sends the same prompt to the OpenAI Responses API and prints the generated text.
