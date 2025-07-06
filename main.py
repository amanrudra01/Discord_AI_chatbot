import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if self.user != message.author and self.user in message.mentions:
            try:
                response = client_ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful Discord bot."},
                        {"role": "user", "content": message.content}
                    ],
                    temperature=1,
                    max_tokens=256,
                )
                await message.channel.send(response.choices[0].message.content)
            except Exception as e:
                await message.channel.send(f"Error: {e}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv("DISCORD_TOKEN"))