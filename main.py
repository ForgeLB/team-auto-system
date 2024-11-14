from dotenv import load_dotenv
import os
import time
import insert_deal
from modules.pipedrive_integration import get_new_pipedrive_deals
from modules.monday_integration import update_monday_board
from modules.slack_integration import send_slack_message


# Load environment variables from .env file
load_dotenv()

# Access the environment variables
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
MONDAY_BOARD_ID = os.getenv("MONDAY_BOARD_ID")
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
PIPEDRIVE_API_KEY = os.getenv("PIPEDRIVE_API_KEY")

# Track already sent deals to avoid duplicates
sent_deal_ids = set()

def main():
    while True:  # Infinite loop to keep checking for new deals
        # Fetch deals from Pipedrive
        deals = get_new_pipedrive_deals()
        if deals:
            print("Pipedrive deals fetched successfully:", deals)

            for deal in deals:
                deal_id = deal.get("id")
                
                # Check if this deal was already sent
                if deal_id not in sent_deal_ids:
                    deal_title = deal.get("title", "No Title Provided")
                    deal_value = deal.get("value", "No Value Specified")
                    deal_currency = deal.get("currency", "Unknown Currency")
                    person_name = deal.get("person_id", {}).get("name", "No Contact Person")
                    deal_status = deal.get("status", "No Status")

                    # Format the message to be sent to Slack
                    message = (
                        f"*New Deal Fetched from Pipedrive:*\n"
                        f"*Title:* {deal_title}\n"
                        f"*Status:* {deal_status}\n"
                        f"*Value:* {deal_value} {deal_currency}\n"
                        f"*Contact:* {person_name}\n"
                    )

                    # Send the message to Slack
                    send_slack_message(SLACK_API_TOKEN, SLACK_CHANNEL_ID, message)

                    # Add the deal ID to the set of sent deal IDs
                    sent_deal_ids.add(deal_id)

                    # Update Monday.com with deal information
                    update_monday_board(MONDAY_API_KEY, MONDAY_BOARD_ID, deal_id, deal_title)

        else:
            print("Failed to fetch Pipedrive deals.")

        # Sleep for a specified interval before checking again (e.g., 60 seconds)
        time.sleep(60)  # Adjust this interval as needed

if __name__ == "__main__":
    main()
    
    
    
    
    
    
def main():
    # Fetch deals from Pipedrive
    deals = get_new_pipedrive_deals()
    if deals:
        print("Pipedrive deals fetched successfully:", deals)

        for deal in deals:
            deal_id = deal.get("id")
            deal_title = deal.get("title", "No Title Provided")
            deal_value = deal.get("value", "No Value Specified")
            deal_currency = deal.get("currency", "Unknown Currency")
            person_name = deal.get("person_id", {}).get("name", "No Contact Person")
            deal_status = deal.get("status", "No Status")

            # Insert the deal into the database
            insert_deal(deal_title, deal_value, deal_currency, deal_status, person_name)

            # Format the blocks to display deal information
            blocks = [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "*New Deal Fetched from Pipedrive:*"}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Title:*\n{deal_title}"},
                        {"type": "mrkdwn", "text": f"*Status:*\n{deal_status}"},
                        {"type": "mrkdwn", "text": f"*Value:*\n{deal_value} {deal_currency}"},
                        {"type": "mrkdwn", "text": f"*Contact:*\n{person_name}"},
                    ]
                },
                {"type": "divider"}
            ]

            # Send the message to Slack with the formatted block
            send_slack_message(SLACK_API_TOKEN, SLACK_CHANNEL_ID, "New Deal Alert", blocks=blocks)

            # Update Monday.com with deal information
            update_monday_board(MONDAY_API_KEY, MONDAY_BOARD_ID, deal_id, deal_title)

    else:
        print("Failed to fetch Pipedrive deals.")

if __name__ == "__main__":
    main()
