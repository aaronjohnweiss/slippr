
async def commands(message):
    msg = 'Available Slippr commands:\n> !standings to view current standings\n> !sets to view current set counts\n> !users to view registered users and their tags\n> !add <tag#000> to add a user (no < > brackets)\n> !delete <tag#000> to remove a user (no < > brackets) \n> !countdown <duration_days> <reason> to start a countdown'
    await message.channel.send(msg)
    return
