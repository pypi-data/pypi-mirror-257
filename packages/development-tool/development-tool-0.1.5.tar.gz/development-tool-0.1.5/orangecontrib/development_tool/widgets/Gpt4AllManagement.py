import subprocess
import json
import sys

def call_completion_api(localhost, message_content):
    
    print('local', localhost, 'message', message_content)
    command = [
        "curl",
        "--location",
        f"http://{localhost}/v1/chat/completions",
        "--header",
        "Content-Type: application/json",
        "--data",
        json.dumps({
            "temperature": 0.7,
            "model": "gpt4all-l13b-snoozy",
            "messages": [{"role": "user", "content": message_content}]
        })
    ]

    #print("Command", command)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Error Output:", e.stderr)


