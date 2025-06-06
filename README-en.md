# Discord Earthquake Information Bot

This bot uses a P2P earthquake information API to automatically notify the latest earthquake information to Discord servers.

[Japan](README.md)

## Features

- Checks the latest earthquake information every minute
- Notifies all joined servers when a new earthquake occurs
- Changes the notification message color based on the maximum seismic intensity (yellow for 5 weak or higher, red for 6 weak or higher)
- Retains the previous notification information after a restart to prevent duplicate notifications

## Required Environment

- Python 3.8
- discord.py library
- aiohttp library
- requests library
- dotenv library

## Environment Variables

Please set up the `.env` file.
