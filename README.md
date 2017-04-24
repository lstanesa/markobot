# Markobot

A very simple Discord chat bot that talks back using markov chains.

Copy example_settings.json to settings.json, and write in your API token and the command prefix.
Copy example_chat.json to chat.json and leave it be.

@ the bot to get a markov-generated response.

The bot's whitelist and blacklist features are not finished yet.

Commands:
```
quit               #Shut the bot down
blacklist <user@>  #Prevent the bot from learning from a user (unfinished)
whitelist <user@>  #Whitelist a user if the whitelist is enabled (unfinished)
```

run.py doesn't do anything yet, so start the bot using

```
python bot.py
```
