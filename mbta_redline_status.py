import requests
from datetime import datetime, timedelta, timezone

# MBTA API endpoint url for alerts
API_URL = "https://api-v3.mbta.com/alerts?filter[route]=Red"

# My MBTA Developer API key
API_KEY = "3b210c66cb154a1cbdbf6f482b582f55"

def check_red_line_disruptions():
    headers = {
        "x-api-key": API_KEY
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()

        if data['data']:
            # Dictionary to store the latest alert for each description
            latest_alerts = {}
            
            # Set cutoff date for 1 week ago, with UTC timezone
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)

            # Populate dictionary with only the latest alerts within 1 week for each description
            for alert in data['data']:
                description = alert['attributes']['header']
                updated_at_iso = alert['attributes']['updated_at']
                updated_at = datetime.fromisoformat(updated_at_iso.replace("Z", "+00:00"))
                
                # Get the lifecycle status
                lifecycle = alert['attributes']['lifecycle']
                
                # Only consider alerts that are not UPCOMING and within the last week
                if lifecycle != 'UPCOMING' and updated_at >= cutoff_date:
                    # Update if this description is new or if this alert is more recent
                    if description not in latest_alerts or updated_at > latest_alerts[description]['updated_at']:
                        latest_alerts[description] = {
                            'updated_at': updated_at,
                            'description': description
                        }

            # Display the alerts, sorted by the most recent update time
            if latest_alerts:
                for i, (description, alert) in enumerate(sorted(latest_alerts.items(), key=lambda x: x[1]['updated_at'], reverse=True), start=1):
                    formatted_time = alert['updated_at'].strftime("%B %d, %Y %I:%M %p")
                    print("Line Disruptions:")
                    print(f"{i}. {formatted_time} - {description}")
            else:
                print("There are no current Line disruptions")
    else:
        print("Failed to fetch data:", response.status_code)

check_red_line_disruptions()