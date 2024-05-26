import re
from plyer import notification
from datetime import datetime
import time
from json.decoder import JSONDecodeError
import json

TASKS_FILE = "tasks.json"
tasks = []

def load():
    global tasks
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, JSONDecodeError):
        tasks = []

def notify(task, due):
    notification.notify( title = f"{task} due at {due}",
                        message = "This Task is Due Soon,\nMake sure to finish it!"
                        )

def search_time(file_name, search_pattern):
    while True:
        try:
            with open(file_name, 'r') as f:
                data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "due_datetime" in item:
                        due_datetime = datetime.strptime(item["due_datetime"], "%Y-%m-%d %H:%M")
                        time_difference_hours = (due_datetime - datetime.now()).total_seconds()
                        if 0 < time_difference_hours < 59 and re.search(search_pattern, item["due_datetime"]):
                            print(f">>>>>>Time '{item['due_datetime']}' found in the JSON file.")
                            notify(item["name"], item["due_datetime"])
                            currentSec = 60 - time.localtime().tm_sec
                            time.sleep(currentSec)
                            return
        except json.JSONDecodeError:
            print("Error parsing JSON file. Waiting for update...")
        print(f"Time '{search_pattern}' not found in the JSON file. Going into standby mode...")


load()
global match
match = r'\d{2}:\d{2}'

while True:
    for task in tasks:
        current_datetime = datetime.now()
        due_datetime = datetime.strptime(task["due_datetime"], "%Y-%m-%d %H:%M")
        time_difference_hours = (due_datetime - current_datetime).total_seconds() / 3600
        time_diff = (current_datetime - current_datetime).total_seconds()
        print(f"{due_datetime} has a time diff of: {time_difference_hours} ")
        time.sleep(1)
        if 0 < time_difference_hours < 1:
            notify(task["name"], task["due_datetime"])
            print(f">>>>>>{time_difference_hours}")

    # search for any time string in the 24-hour format "HH:MM" in the tasks.json file
    search_time(TASKS_FILE, match)