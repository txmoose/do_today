#!/usr/bin/env python3
"""
This module will get a number of random tasks from a trello board and email them to you
"""

import json
import random
import smtplib
import sys

from email.message import EmailMessage
from trello import TrelloClient


def get_rand_task(tasks, amount):
    """Returns a random set of tasks from a list of tasks on a board"""

    random_tasks = []
    while len(random_tasks) < amount:
        candidate_task = random.choice(tasks)
        if candidate_task not in random_tasks:
            random_tasks.append(candidate_task)

    return random_tasks


def main():
    """Main method"""

    # Get config
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        config_file = "config.json"

    with open(config_file, 'r') as config:
        CONFIG = json.load(config)

    # Logging into Trello
    client = TrelloClient(api_key=CONFIG["api_key"],
                          api_secret=CONFIG["api_secret"],
                          token=CONFIG["token"])

    # Have to get all boards to find working board by name
    all_boards = client.list_boards()

    # Finding working board by .name
    for board in all_boards:
        if board.name == CONFIG["working_board"]:
            working_board = board

    # Get a number of tasks from working_board
    tasks = get_rand_task(working_board.get_cards(), CONFIG["num_tasks"])

    # Build body for daily email of tasks
    body = "Howdy!\n\nToday, you should accomplish the following from your board named {}:\n".format(working_board.name)
    for task in tasks:
        body = body + "{}\n".format(task.name)

    body = body + "\nGood luck!"

    # Prepare email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "Do These Things Today: {}".format(working_board.name)
    msg['From'] = CONFIG["from_email"]
    msg['To'] = CONFIG["to_email"]

    # Send message
    server = smtplib.SMTP(CONFIG["smtp_server"])
    server.send_message(msg)
    server.quit()


if __name__ == "__main__":
    main()
