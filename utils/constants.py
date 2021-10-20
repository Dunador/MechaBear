from disnake import PermissionOverwrite

CHANNEL_ADMIN = PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    manage_messages=True,
    manage_channels=True,
    read_message_history=True
)
CHANNEL_READ_WRITE = PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    read_message_history=True,
)
CHANNEL_HIDDEN = PermissionOverwrite(
    read_messages=False,
    send_messages=False,
    read_message_history=False
)
CHANNEL_READ = PermissionOverwrite(
    read_messages=True,
    send_messages=False,
    read_message_history=True
)