import discord
import re
import os
import requests
import json
import random
from discord.ext import commands
from replit import db

DISCORD_TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "dejected", "sorrowful", "despondent", "out of sorts", "saddened", "gloomy", "glum", "melancholy", "disconsolate", "downhearted", "downcast", "cast down", "lonely"]
starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!",
  "Optimism is the faith that leads to achievement - Helen Keller",
  "You got this.",
  "I know this won't be easy, but I know you've also got what it takes to get through it.",
  "Sending you good thoughts - and hoping you believe in yourself just as much as I believe in you."
]

if "responding" not in db.keys():
  db["responding"] = True
  
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_enouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else: 
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@bot.event
async def on_ready():
  print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  msg = message.content

  if msg.startswith("$hello"):
    await message.channel.send("Hey there partner!")
    
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
    
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_enouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)
    
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
      
bot.run(DISCORD_TOKEN)