import os
import discord

def auto_upload(folder_path, bot_token):
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    files_to_upload = []

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('auto upload'):
            files_to_upload.clear()
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    files_to_upload.append(file_path)

            if files_to_upload:
                for file_path in files_to_upload:
                    await message.channel.send(file=discord.File(file_path))
            else:
                await message.channel.send("No files to upload.")

    client.run(bot_token)

# Example usage:
# auto_upload_files("your/folder/path", "<Your Bot Token>")
