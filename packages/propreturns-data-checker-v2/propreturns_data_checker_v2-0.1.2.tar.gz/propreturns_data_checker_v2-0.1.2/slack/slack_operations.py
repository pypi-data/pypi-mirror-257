import requests
import logging
import json
from datetime import datetime
import uuid
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def get_mac_address():
    try:
        mac = ":".join(
            [
                "{:02x}".format((uuid.getnode() >> elements) & 0xFF)
                for elements in range(2, 7)
            ][::-1]
        )
        return mac
    except Exception as e:
        logging.error(f"Error getting MAC address: {e}")
        return "Unknown"


def send_slack_message(message, db_name, table_name, action_to_perform="append"):
    """
    Sends a formatted message to a Slack channel with details about the database change.

    Args:
        message (str): The main message to be sent to Slack.
        db_name (str): The name of the PostgreSQL database.
        table_name (str): The name of the table where the change occurred.
        action_to_perform (str): The action performed on the table ("append" by default).

    Returns:
        None

    Raises:
        requests.exceptions.RequestException: If there's an issue with the HTTP request.
        Exception: For any unexpected errors.
    """
    # Define the Slack webhook URL
    webhook_url = config.get("slack", "webhook_url")

    # Get the MAC address of the computer
    mac_address = get_mac_address()

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the formatted message to be sent to Slack
    formatted_message = (
        f"🚨*Alert*🚨\n\n"
        f"*Database Change Detected* 📊\n\n"
        f"{message}\n\n"
        f"*Details : * \n"
        f"Database: `{db_name}`\n"
        f"Table: `{table_name}`\n"
        f"Action: `{action_to_perform}`\n"
        f"MAC Address: `{mac_address}`\n"
        f"Timestamp: `{timestamp}`"
    )

    # Create the payload to be sent to Slack
    payload = {
        "channel": "#postgres-database-updates",
        "text": formatted_message,
        "attachments": [
            {
                "fallback": "Get more info",
                "actions": [
                    {
                        "type": "button",
                        "text": "Get more info",
                        "url": f"{webhook_url}/{mac_address}/{timestamp}",
                    }
                ],
            }
        ],
    }

    # Define headers for the HTTP request
    headers = {"Content-Type": "application/json"}

    try:
        # Send the POST request to the Slack webhook
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

        # Check for any HTTP request issues
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending message to Slack: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
