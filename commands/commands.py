
async def commands(message):
    msg = 'Available Slippr commands:\n> !standings to view current server standings\n> !add <tag#000> to add a user (no < > brackets)\n> !delete <tag#000> to remove a user (no < > brackets)'
    await message.channel.send(msg)
    return
