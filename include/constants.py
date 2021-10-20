import disnake

CHANNEL_ADMIN = disnake.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    manage_messages=True,
    manage_channels=True,
    read_message_history=True
)
CHANNEL_READ_WRITE = disnake.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    read_message_history=True,
)
CHANNEL_HIDDEN = disnake.PermissionOverwrite(
    read_messages=False,
    send_messages=False,
    read_message_history=False
)
CHANNEL_READ = disnake.PermissionOverwrite(
    read_messages=True,
    send_messages=False,
    read_message_history=True
)
