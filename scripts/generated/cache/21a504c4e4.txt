# Tribes Mod 

- forge 1.16.5
- Commissioned by Khaki.

The tribes mod allows players to form groups (inspired by the Factions plugin).
There are many commands and some GUIs that may be used to manage your tribe.
Many features are configurable.

## Commands

THIS IS TRUE FOR VERSION 1.75

### /tribe join

Opens a gui that shows a list of existing tribes. hover over one to see member count and click to join.
Click the create button to open a GUI to make your own tribe.
- when config tribesRequired=true the gui will be forced open for players not in a tribe and cannot be closed

### /tribe join tribeNameHere

Joins the named tribe

### /tribe create tribeNameHere

Creates and joins a new tribe

### /tribe or /tribes

Opens your main tribe gui. Shows your rank and the name, leader, member count, tier and relations of your tribe.
Buttons to leave and change effects (only for leader).

### /tribe leave

Leaves your tribe.

### /tribe count tribeNameHere

Will show you the member count and tier of the named tribe

### /tribe who playerNameHere

Tells you which tribe the named player is in

### /tribe initials stringHere

Only for leader. Sets your tribes initials. Will be displayed in chat eventually.

### /tribe promote playerNameHere

Increases the tribe rank of the named player. Can only be used on players 2 ranks lower than you. member > officer > vice leader > leader

### /tribe demote playerNameHere

Decreases the tribe rank of the named player. Can only be used on players lower ranked than you. leader > vice leader > officer > member

### /tribe ban playerNameHere

Bans and kicks the named player from your tribe. Can only be used on people with a lower rank in your tribe than you.

### /tribe unban playerNameHere

Unbans the named player from your tribe. Can only be used by rank officer or greater.

### /tribe bans playerNameHere

Displays the number of tribes the named player is banned from (useful for checking if someone is a griefer)

### /tribe ally tribeNameHere

Makes the named tribe your ally. Will show in green in your main tribe GUI. Kills between you will not result in head drops. One directional (you will not automatically become their enemy)

### /tribe enemy tribeNameHere

Makes the named tribe your enemy. Will show in red in your main tribe GUI. Your dogs will attack their members on sight. One directional (you will not automatically become their enemy)

### /tribe neutral tribeNameHere

Removes the named tribe from being your ally or enemy.

### /tribe effects

Only useable by tribe leader. Opens the GUI to manage your tribe's always active potion effects.
How many you choose is based on your tribe's tier (member count).
- daysBetweenEffectsChange config is how many IRL days you must wait before changing your effects again
- tier_negative_effects config is a list of the number of negative effects required by tribe rank
- tier_positive_effects config is a list of the number of positive effects allowed by tribe rank
- ignoredEffects config is a list of effects that cannot be chosen

### /tribe hemisphere SIDE

Allows your tribe to break and place blocks in one of the world's hemisphere. Before you pick one, you can access neither.
You can never change your choice so choose wisely.

- config halfNoMansLandWidth is the distance from zero to the edge of a hemisphere
- when config useNorthSouthHemisphereDirection=true the valid SIDE values are north and south otherwise they're east and west
- config tierForSelectHemi is the minimum tribe tier required to claim a hemisphere
- config requireHemiAccess=false disables this feature
- config rankToChooseHemi is the minimum rank in your tribe for a member to claim a hemisphere (defaults to vice leader)

### /tribe chunk claim

Only for officers and higher. Claim the chunk you're currently in for your tribe. Players not in your tribe will not be able to place/break/use blocks in your chunks.
The owner of the chunk you're currently in will be displayed in the top left corner. Get more members or change the config to be able to claim more chunks.
When people in your tribe die to often your chunks will be briefly able to be raided (defined in config, make the numbers 0 to disable this feature)

The Tribe Compass is an item that will point to nearby claimed chunks (yours and other tribes). Right click in a claimed chunk to ignore it when searching for the closest claimed chunk.
Right click in an ignored chunk to count it again.

- max_claimed_chunks config is a list of the number of claimed chunks allowed by tribe rank
- pvpDeathPunishTimes config controls how long your claims will be disabled when a member is killed by another player
- nonpvpDeathPunishTimes config controls how long your claims will be disabled when a member dies (not because of another player)

### /tribe chunk unclaim

Unclaim the chunk you're currently in.

### /tribe delete

Leader only. Deletes your tribe.

### /tribe deity list

Displays all existing deities. Format is DisplayName is the Label of Domains

- deity list is defined in deities/deities.json

### /tribe deity choose deity

Choose a deity for your tribe to follow. It is just cosmetic. Changes the text in your deity book, the patten on your deity banner and the symbol displayed above your alters.

### /tribe deity book

Use while holding a book or bookshelf to create your deity book.

- text is defined in deities/yourDeityKey.txt

### /tribe deity banner

Use while holding a banner to add your deity's symbol as a gold pattern

- the banner pattern is defined in deities/deities.json and must use the special gold ones added by the tribes mod (not vanilla)

### /tribe autoban set int:deaths int:DAYS

Leader only. If a player dies deaths (default: 3) times within DAYS (default: 2) real life days, they will be banned from your tribe (you can unban them).
This is useful to get rid of people dying too often and allowing your claimed land to be griefed.
To disable this feature, just make one of the number arguments really big (like 9999) so it never happens.

### /tribe autoban boolean rank

Leader only. sets whether the autoban mechanic above should apply to a certain rank (member, officer, vice leader)

### /tribe invite toggle boolean

true: make your tribe invite only. players cannot join without an invite sent by the command below.  
false: default. players may join the tribe freely

### /tribe invite send PlayerNameHere

if your tribe is private, send an invite to the specified player. Pending invites are not saved when the sever restarts. Only usable by officers+

### /tribe invite revoke PlayerNameHere

if your tribe is private and the specified player has a pending invite, remove the invite. Only usable by officers+

## Other Config Options

**info coming soon...** but the default config file (generated when you first open a world) has comments explaining what everything does

## Deity Data Format

**info coming soon...** but when you open a world it will generate the defaults at world/data/deities so you can edit them however you like. the json file has thier meta data and the txt files have holy book contents. 