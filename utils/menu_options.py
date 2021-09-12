from dislash import *

# CHARACTERS
CHAR_ADD = [
    Option("name", "Whats their name?", OptionType.STRING, required=True),
    Option("handle", "For use with Peregrin_Post", OptionType.STRING),
    Option("imageurl", "Image Link for Peregrine Post", OptionType.STRING),
    Option("status", "alive or dead?", OptionType.STRING,
           choices=[OptionChoice("alive", "alive"),
                    OptionChoice("dead", "dead")]),
    Option("mainquest", "Highest Main Quest completed?", OptionType.INTEGER)
]

GUILD_ADD = [
    Option("member", "Who is the Guild-master (the Player who runs it)", OptionType.USER, required=True),
    Option("guild_name", "What is the Guild Name you are adding?", OptionType.STRING, required=True)
]

ICE_QUOTES = ['Ice Bear has committed no crime... today',
              'All Ice Bear\'s Friends are Future Enemies',
              'Ice Bear doesn\'t sweat, Ice Bear glows',
              'The World isn\'t Ready For What Ice Bear Can Do',
              'Ice Bear cried, but just inside',
              '#IceBearForPresident',
              'Ice Bear has fought personal demons... years of Therapy',
              'Ice Bear Hates Butts',
              'Ice Bear Wants Separate Checks',
              'Ice Bear Wants Justice',
              'More Ice Bear, More Good',
              'Ice Bear does not Approve',
              'Ice Bear thinks Square is Delicious Shape',
              'Ice Bear Will Break You',
              'Ice Bear needs to see Proof of Ownership',
              'Ice Bear likes Turtles',
              'Ice Bear just wants to shoot Potatoes',
              'Ice Bear Smells Like Clean Babies',
              'Ice Bear is fast and furious'
              ]
