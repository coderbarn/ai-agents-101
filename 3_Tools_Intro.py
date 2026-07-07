# From: https://github.com/daveebbelaar/ai-cookbook/blob/main/patterns/workflows/1-introduction/3-tools.py

import argparse
import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

parser = argparse.ArgumentParser(description="Get weather for a city.")
parser.add_argument("city", help="City name for the weather lookup.")
args = parser.parse_args()

# --------------------------------------------------------------
# Define the tool (function) that we want to call
# --------------------------------------------------------------


def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    current_weather = data["current"]
    temperature_celsius = current_weather["temperature_2m"]
    current_weather["temperature_2m_fahrenheit"] = (temperature_celsius * 9 / 5) + 32
    return current_weather


# --------------------------------------------------------------
# Step 1: Call model with get_weather tool defined
# --------------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in Celsius and Fahrenheit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {
        "role": "user",
        "content": f"What's the weather like in {args.city} today? Use the city's latitude and longitude to call the weather tool, then show the temperature in both Celsius and Fahrenheit.",
    },
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------

completion.model_dump()

# --------------------------------------------------------------
# Step 3: Execute get_weather function
# --------------------------------------------------------------


def call_function(name, args):
    if name == "get_weather":
        print(f"Calling get_weather with: {args}")
        return get_weather(**args)


for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, tool_args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )

# --------------------------------------------------------------
# Step 4: Supply result and call model again
# --------------------------------------------------------------


class WeatherResponse(BaseModel):
    temperature_celsius: float = Field(
        description="The current temperature in Celsius for the given location."
    )
    temperature_fahrenheit: float = Field(
        description="The current temperature in Fahrenheit for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )


completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
)

# --------------------------------------------------------------
# Step 5: Check model response
# --------------------------------------------------------------

final_response = completion_2.choices[0].message.parsed
final_response.temperature_celsius
final_response.temperature_fahrenheit
final_response.response
print(f"Temperature: {final_response.temperature_celsius} C")
print(f"Temperature: {final_response.temperature_fahrenheit} F")
print(final_response.response)
