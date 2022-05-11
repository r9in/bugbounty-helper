import discord
from discord.ext import commands
import json
import time
from subprocess import Popen, PIPE

token = "TOKENHERE"
done = ":green_square:"
ndone = ":orange_square:"

client = commands.Bot(command_prefix="", case_insensitive=True, help_command=None)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd)
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):

    if msg.author == client.user:
        return
    if msg.content == "start":

        await msg.delete()

        SAVE_FILE = 'line_number.txt'

        try:
            with open(SAVE_FILE) as save_file:
                line_number_to_show = save_file.read().strip()
            line_number_to_show = int(line_number_to_show)
        except (FileNotFoundError, ValueError) as _:
            line_number_to_show = 0

        with open("checklist.txt") as quotes_file:
            for line_number, line in enumerate(quotes_file):
                if line_number == line_number_to_show:
                    print(line, file=open('logger.txt', 'w'))

        with open(SAVE_FILE, 'w') as save_file:
            line_number_to_show = line_number_to_show + 1
            save_file.write(f'{line_number_to_show}')

        with open("logger.txt") as f:
            for w in f:
                print(w)

                sent_message = await msg.channel.send(f"[  ] {w}")
                res = await client.wait_for(
                    "message",
                    check=lambda x: x.channel.id == msg.channel.id
                    and msg.author.id == x.author.id
                    and x.content.lower() == "done"
                    or x.content.lower() == "notdone",
                    timeout=None,
                )

                if res.content.lower() == "done":
                    await res.delete()
                    await sent_message.edit(content=f"[{done}] {w}")
                    break
                if res.content.lower() == "notdone":
                    await res.delete()
                    await sent_message.edit(content=f"[{ndone}] {w}")
                    break

@client.event
async def on_message(message):

    with open("logger.txt") as f:
        for title in f:

            if message.author == client.user:
                return
            if message.content.startswith("note") and message.channel.name == 'checklist':
                channel = client.get_channel(973370473473777664)
                await channel.send("TYPE YOUR NOTES!")
                notes = await client.wait_for("message")
                nchannel = client.get_channel(974027423064682557)
                embed=discord.Embed(title=f"{title}",description=notes.content,color=0x9208ea)
                await nchannel.send(embed=embed)

try:
    client.run(token)
except KeyboardInterrupt:
    pass
