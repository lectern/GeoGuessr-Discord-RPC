from threading import Thread
from pypresence import Presence
import time, requests, re

import rpc_api

if __name__ == "__main__":
    # run api thread
    Thread(target=rpc_api.app.run).start()
    
    # run discord rpc
    client_id = '1101175866551173192'
    RPC = Presence(client_id)
    RPC.connect()
    start_time = time.time()

    while (True):
        geoguessr = requests.get("http://127.0.0.1:5000/rpc").json()
        title = geoguessr['title'].replace(' - GeoGuessr', "")
        url = geoguessr['url']

        map_name = ""
        if '- Game' in title:
            str_cpy = title
            map_name = ''.join(e for e in str_cpy.replace(" - Game", ""))
            title = ' - Game'
        elif ' - Map' in title:
            str_cpy = title
            map_name = ''.join(e for e in str_cpy.replace(" - Map", ""))
            title = ' - Map'
        title = title.replace("  ", " ")
        
        status = {
            'GeoGuessr - Let\'s explore the world!': 'In Menu',
            'Singleplayer': 'Browsing Singleplayer Menu',
            'Multiplayer': 'Browsing Multiplayer Menu',
            'Quiz': 'Playing Quiz',
            'Support': 'Looking at Support Page',
            'Gift Cards': 'Browsing Gift Cards',
            'Maps': 'Choosing a Map',
            'My maps': 'Browsing My Maps',
            'Liked maps': 'Browsing Liked Maps',
            'Badges': 'Browsing Badges',
            'Activities': 'Browsing Activity',
            'Ongong Games': 'Browsing Ongoing Games',
            'Profile Settings': 'Editing Profile Settings',
            'Profile': 'Viewing Profile',
            'Quickplay': 'Playing Quickplay',
            'MapRunner': 'Playing MapRunner',
            'Start a game': 'Starting a Game',
            ' - Game': f'Playing {map_name}',
            ' - Map': f'Looking at {map_name} Map'
        }
        status.setdefault(title, f'Playing {title}')

        if 'GeoGuessr - Let\'s explore the world!' == title and url != "https://www.geoguessr.com/":
            try:
                url = re.search(r"https://www.geoguessr.com/(.+)/.+", url).group(1)
            except:
                url = re.search(r"https://www.geoguessr.com/(.+)", url).group(1)
            status['GeoGuessr - Let\'s explore the world!'] = f"Playing {url.replace('-', ' ').title()}"

        RPC.update(
            state=status[title],
            large_image='icon',
            start=start_time,
            buttons=[{"label": "Play GeoGuessr", "url": "https://www.geoguessr.com/"}]
        )

        time.sleep(2.5)