import asyncio
import json

from async_steam import Steam
from decouple import config

# KEY = config("B59856FFDC7B2215EE7F5F26913A5E56")
steam = Steam("B59856FFDC7B2215EE7F5F26913A5E56")

if __name__ == '__main__':
    result = asyncio.run(steam.users.search_user('jeygavrus'))
    print(json.dumps(result, indent=2))
