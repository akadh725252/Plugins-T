from . import * 
from telethon import Button
from telethon.tl import functions
from telethon.tl.types import ChatAdminRights

@hell_cmd(pattern="leaveall(?:\s|$)([\s\S]*)")
async def leave_all_chats(event):
    await event.edit("Leaving all chats...")

    async for dialog in event.client.iter_dialogs():
        try:
            await event.client(functions.messages.DeleteChatUserRequest(dialog.id, 'me'))
        except Exception as e:
            LOGS.warning(f"Error leaving chat {dialog.id}: {str(e)}")

    await event.edit("Left all chats successfully!")

@hell_cmd(pattern="join(?: (.+))?$")
async def join_chat(event):
    args = event.pattern_match.group(1)
    
    if args:
        try:
            link, username = args.split(" ", 1)
        except ValueError:
            return await event.edit("Invalid syntax. Usage: `/join link username`")

        await event.edit(f"Joining the chat with link: {link} and username: {username}...")

        try:
            await event.client(functions.channels.JoinChannelRequest(link))
        except Exception as e:
            return await event.edit(f"Error joining the chat: {str(e)}")

        await event.edit("Joined the chat successfully!")

    else:
        await event.edit("Please provide a chat link and username. Example: `/join link username`")
      
