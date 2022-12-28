# About WrapperLib

WrapperLib is a library I wrote to make a few modding tasks easier. Most of what it can do revolves around automatically converting java objects to byte buffers to be sent over the network or json files or nbt compounds to be saved. Everything it provides can be manually done with just Forge but I find it gets tedious quickly.

WrapperLib helpfully provides the same API for all supported Minecraft versions. So it will save you extra time if you end up porting in future. 

Since WrapperLib is an external library, you'll have to add a couple lines to your build.gradle to import it into your development environment. See [Installation](installation) for details. Your players will have to install WrapperLib as additional mod when they play with your mod. 

- [Networking](networking): send information between the client and the server.
- [Config](config): allow players to configure mod features by editing json files.
- [Keybinds](keybinds): react to keyboard input, automatically synced to the server.
- [Saved Data](saved-data): save extra information with world data.
- [Resources](resources): load information from data packs or resource packs.

You can look at [the example mod](https://github.com/LukeGrahamLandry/WrapperLib/tree/1.19/example) for a practical example of these features in action. 