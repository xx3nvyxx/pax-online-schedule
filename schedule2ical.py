#!/user/bin/env python
"""Convert PAX Online schedule export JSON to ical file"""

import json
from datetime import datetime,timezone

header = """BEGIN:VCALENDAR
PRODID:-//PAX Online//Pax Online 2020//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
"""

footer = """
END:VCALENDAR"""

dtf = "%Y%m%dT%H%M%SZ"

def main():
    with open('schedule-export.json', 'r') as file:
        data = json.loads(file.read())
        schedule = data["events"]
        tags_data = data["tags"]
        tags = {}
        for tag in tags_data:
            tags[tag] = tags_data[tag]["name"]
        #print(tags)
        panels = []
        for panel in schedule:
            location = "unknown"
            if 139 in panel["tags"]:
                location = "https://twitch.tv/PAX"
            elif 140 in panel["tags"]:
                location = "https://twitch.tv/PAX2"
            elif 141 in panel["tags"]:
                location = "https://twitch.tv/PAX3"
            event = "BEGIN:VEVENT\n"
            event += "DTSTAMP:" + datetime.now(timezone.utc).strftime(dtf) + "\n"
            event += "DTSTART:" + datetime.fromtimestamp(panel["start"],tz=timezone.utc).strftime(dtf) + "\n"
            event += "DTEND:" + datetime.fromtimestamp(panel["end"],tz=timezone.utc).strftime(dtf) + "\n"
            event += "UID:" + panel["urlTitle"] + "@online.paxsite.com\n"
            event += "SUMMARY:" + panel["title"] + "\n"
            event += "DESCRIPTION:https://online.paxsite.com/schedule/panel/" + panel["urlTitle"] + "\n"
            if location != "unknown":
                event += "LOCATION:" + location + "\n"
            event += "END:VEVENT\n"
            panels.append(event)
        ical = header + "\n".join(panels) + footer
        print(ical)


if __name__=="__main__":
        main()
