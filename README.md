# Dank Memer Trivia Scraper
A discord bot to scrape trivia answers from [Dank Memer](https://dankmemer.lol/) and store them in sqlite database

(Dank Memer changed the trivia format, making this tool currently outdated)

## Requirements: 
Python 3.x

discord bot (bot.py) requires discord.py

`pip install discord.py`

Additional script for automating trivia commands requires pyautogui

`pip install pyautogui`

## Usage
### scraper bot
Create discord bot and invite to server. 

Create .env file with discord bot token.

Create sqlite db and table.

Start bot.py using python.
### trivia command 
Run dank.py to automate dankmemer commands (still in progress)

### TODO: 

- threading on dank.py to automate dank memer commands
- set bot status
- dm me error messages
- timer
