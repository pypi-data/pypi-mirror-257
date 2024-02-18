#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import tempfile
import platform
import json
import requests

temp_dir = tempfile.gettempdir()
history_file_path = os.path.join(temp_dir, 'ask_history.json')

def call_the_fastest_endpoint_ever(q):

    messages = []

    # System Prompt
    messages.append({
        "role": "system", "content": "You are a command line utility that answers questions quickly and briefly. Don't use any markdown or other formatting. The user is likely looking for a cli command or usage of some tool, attempt to answer the question with just the command that would be relavent, and only if 100% needed, with a single sentence description after the command with a ':'. If there were a few commands you could have given, show them all. Remember that you print to a console, so make it easy to read when possible." + "the user is on the operating system: " + platform.system() + ". Bias towards short answers always, each row should fit in one unwrapped line of the terminal, less than 40 characters! Only 3 rows maximum."
    })

    # Fake Examples
    messages.extend([
        {"role": "user", "content": "how do i convert image size in ffmpeg"},
        {"role": "assistant", "content":"""`ffmpeg -i input.jpg -filter:v scale=h=1024 output.jpg`: Resizes the image to a height of 1024 pixels.
`ffmpeg -i input.jpg -filter:v scale=w:h=1:1 output.jpg`: Resizes image to width and height that are equal
`ffmpeg -i input.jpg -filter:v scale=force_original output.jpg`: preserving original aspect ratio."""},
        {"role": "user", "content": "list items in dir by date"},
        {"role": "assistant", "content":"""`ls -lt`: Lists all items in the current directory sorted by modification time, newest first.
`ls -ltr`: added 'r' sorts by oldest first."},
        {"role": "user", "content": "how do i make a new docker to run a fresh ubuntu to test on"},
        {"role": "assistant", "content":"`docker run -it ubuntu bash`: also opens a bash shell.
`docker run -it --rm ubuntu bash`: --rm removes the container when it exits."""},
        {"role": "user", "content": "find text in files in linux"},
        {"role": "assistant", "content":"""`grep -r 'search_term' /path/to/directory`
`grep -r 'search_term' /path/to/directory --include=*.txt`"""},
        {"role": "user", "content": "how to change file permissions in linux"},
        {"role": "assistant", "content":"""`chmod 777 file`
`chmod 755 file`"""}

    ])

    history = get_last_n_history(5)  # Get the last 5 entries

    if history:
        for entry in history:
            messages.extend([
                {"role": "user", "content": entry["Question"]},
                {"role": "assistant", "content": entry["Answer"]}
            ])

    messages.append({
        "role": "user", "content": q
    })

    response = requests.post(url="https://fastask.fly.dev/itsfast", json={"messages": messages}).json()
    print(response['response'])


    print()
    print()
    add_to_history(q, response['response'])
    
def add_to_history(question, answer):
    history_entry = {"Question": question, "Answer": answer}

    if not os.path.exists(history_file_path):
        with open(history_file_path, 'w') as f:
            json.dump([history_entry], f)
    else:
        try:
            with open(history_file_path, 'r') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

        history.append(history_entry)

        if len(history) > 5:
            history = history[-5:]

        with open(history_file_path, 'w') as f:
            json.dump(history, f)

def get_last_n_history(n):
    # Check if the file exists, if not, return an empty list
    if not os.path.exists(history_file_path):
        return []

    with open(history_file_path, 'r') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []

    # Return the last n entries from the history
    return history[-n:]

def clear_history():
    if os.path.exists(history_file_path):
        os.remove(history_file_path)
    with open(history_file_path, 'w') as f:
        pass  # Create the file if it doesn't exist


def main():

    parser = argparse.ArgumentParser(
        description='This is a command-line tool that answers questions using OpenAI or a local model.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear the history of questions and answers.'
    )
    parser.add_argument(
        'question',
        nargs='*',
        help='Enter the question you want to ask.'
    )
    args = parser.parse_args()


    # If no arguments were passed, print the help message and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.clear:
        clear_history()
        print("FastAsk History cleared.")
        exit()

    question = ' '.join(args.question)

    call_the_fastest_endpoint_ever(question)

if __name__ == '__main__':
    main()
