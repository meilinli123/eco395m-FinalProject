import psycopg2
from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI()

# Connect to your PostgreSQL database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="luolex",
            host="34.173.71.254",
            port="5432",
            database="libraries",
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Query the database based on given visits and states
def get_libname_from_database(visits, states):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT libname FROM your_table WHERE visits = {visits} AND stabr = '{states}'"
            cursor.execute(query)
            libname = cursor.fetchone()
            cursor.close()
            connection.close()
            return libname[0] if libname else None
        except psycopg2.Error as e:
            print(f"Error executing the query: {e}")
            return None

# Function to run the conversation with OpenAI
def run_conversation():
    messages = [{"role": "user", "content": "What is the libname with visits=100 and states='CA'?"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_libname_from_database",
                "description": "Get libname from database based on visits and states",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "visits": {"type": "integer"},
                        "states": {"type": "string"},
                    },
                    "required": ["visits", "states"],
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = globals()[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                visits=function_args.get("visits"),
                states=function_args.get("states"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )

        return second_response

print(run_conversation())
