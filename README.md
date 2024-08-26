# EnviroBot 
This discord bot was made for DevNestHacks using discord.py.
Current features:
- `/advice`: receive a 'green' tip through AI
- `/ecochallenge`: recieve a random eco-friendly challenge!
- `/forecast [city]`: view the forecast for the next five days
- `/help`: list out all the commands
- `/news`: view the latest cliamte change news (BBC)
- `/ping`: test the bot ping
- `/weather [city]`: view the current weather (default: Oakville)
* This is not slash commands, the prefix is '/' *

## Invite the bot
Click on the [Invite Link](https://discord.com/oauth2/authorize?client_id=1277436730756304959&permissions=8&integration_type=0&scope=applications.commands+bot) to test the bot out in your own server!

## Short Demo
https://youtu.be/AsvVXgRYxbU

## Run it locally
For windows:
`pip install discord.py requests beautifulsoup4 python-dotenv asyncio transformers`

For mac:
`pip3 install discord.py requests beautifulsoup4 python-dotenv asyncio transformers`
* Pre-reqs: have python installed on your computer

1. Install the packages above and clone the repo
2. Create a `.env` file in the `/src` directory
3. Head to the Discord developer portal, and create a bot
4. Ensure you have intents enabled in settings
5. Copy your discord token and in your `.env` file, write:
> DISCORD_BOT_TOKEN = your_token
6. Head over to [Weather Api](https://www.weatherapi.com/), and create a free account. Copy the API Key
7. Return to your `.env` file, and add the following to the second line:
> APP_KEY = your_api_key
8. Run the program in your terminal, and it should work!
> python3 src/main.py
