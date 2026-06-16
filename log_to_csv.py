import csv
import os
from datetime import datetime


LOG_FILE = "aiagentlog.csv"
HEADERS = ["date", "time", "user_prompt", "function_name", "function_args", "function_response"]


def log_call(user_prompt, function_name, function_args, function_response):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    file_exists = os.path.isfile(LOG_FILE) and os.path.getsize(LOG_FILE) > 0

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADERS)
        writer.writerow([date_str, time_str, user_prompt, function_name, str(function_args), str(function_response)])
