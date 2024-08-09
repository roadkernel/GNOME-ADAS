# VADAS

Vault Automated Defense & Alert System is a bot for Gnomes that helps with warning everyone in case of an emergency.

## Setup
Make a database on SupaBase.<br/>
Create a bot @BotFather.<br/>
Copy telegram API, link to a DB, DB key and edit the bot source<br/>

```python
bot = telebot.TeleBot("TELE_API")
supabase_client = supabase.create_client("LINK_TO_BASE", "SUPABASE_KEY")
```

Copy telegram user IDs that you want to allow <br/>inside the bot and edit this line:

```python
registration_keys = ['TELEGRAM_USER_ID', 'TELEGRAM_USER_ID', 'TELEGRAM_USER_ID', 'TELEGRAM_USER_ID']
```

Now you are free to edit the bot content and use it.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
py blank.py
```
