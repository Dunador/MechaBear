#MechaBear

## A bot for Dungeons of Desternia

This readme will attempt to explain the current feature-set by modules

---

### Characters Module

Character module will have commands related to each Member managing their own characters.

`/characters add`

Every Member must register their PCs with MechaBot. This is separate from Avrea as this will track the characters "Twitter Account", their arena record, guilds they belong to, and other items as needed.

`/characters delete`

A Member can delete their characters if they are added on error. a Member can only delete their own characters. This action is not reversible.

`/characters kill` `/characters revive`

This option will mark the character as "dead" or "alive", but will leave it on the list to keep all of their information.

`/characters view`

View your registered characters list and statuses.

`/characters post_setup`

If a member did not opt to configure the "Twitter-like" Peregerine Post, they can do that with this command

#### TODO:
[ ] add `/characters lookup` command for other Members to look up information on Playable Characters

---

### Guilds Module

Guild's Module has commands to help Guild Masters manage the administrative portion of their guilds.

*DM ONLY*
`/guild add`

Adds a Guild entry to the database. 

#### TODO:

`/guild delete`: deletes a guild 

`/guild formula`: manages what formulas for crafting are

`/guild member`: adds an entry into the guild for a guild member, and an entry to the playable character to its guild

`/guild mission`: group of commands to add a record of a mission, for posterity and historical value, record keeping. Information such as what the mission was, the outcome, and who were involved.

---

### Peregrine Post

Using the twitter like feature, where a character posts to a channel for status updates on their character. 

`/peregine` This command will ask you for a message and which character. It can be summoned from any channel and will post to the designated twitter channel

---

### Arena Module

These command groups are for DMs to keep track of arena fights with beasts. 

*DM ONLY* `/arena fight`

Logs in a fight from a playable character and a beast

*DM ONLY* `/arena add_beast`

Adds a beast to the catalog, so that a player log can be added for a fight

`/arena record`

Shows a fighting record for a player wins/losses

`/arena beast_record`

Shows a fighting record for a beast to see what players its beaten

---

### Help Commands

These commands will include step-by-steps, how tos, and references about the setting

`/help` Right now shows a demonstration as to how the command can be employed

#### TODO: 
`/help setting` , `/help rules`, `/help reference` or similar commands can be created to replace all the info-only channels on the server. the help command can be set to be only viewable to the person who called it, and to disappear after a couple of minutes of inactivity

---

### Highlights Reel

`/highlight` this command is a context menu, when you right click a message (Not available on mobile) it will send the post to one channel. Used for a highlight reel, or blooper reel, or when someone says something super duper cool.

#### TODO
Maybe use a Reaction emoji to send things to the highlight reel and display stats such as checking how many people highlighted it

---

### Owner Commands

`/owner token`

Gives a token to a player

#### TODO:
Make token giving automatic per month