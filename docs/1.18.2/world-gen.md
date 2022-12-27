# World Gen

Since 1.16, the way minecraft handles world generation has been shifting towards being based on json files in data packs rather than making you write code. Eventually I'd like to write my own tutorials on this but for now I'll try to collect a list of resources made by people that understand it much better than me. 

If you have questions about world gen specificlly, [the Minecraft Worldgen Discord Server](https://discord.gg/BuBGds9) might have someone who can help.  

## MC Wiki

- [json format for making a custom dimension](https://minecraft.fandom.com/wiki/Custom_dimension)
- [json format for making biomes](https://minecraft.fandom.com/wiki/Biome/JSON_format)
- [other world gen json formats](https://minecraft.fandom.com/wiki/Custom_world_generation). (Noise settings, carvers, surface builders, features, structure sets, jigsaw pools, structure sets)

## Author: TelepathicGrunt

- [Create a new structure that generates in the world](https://github.com/TelepathicGrunt/StructureTutorialMod/tree/1.18.2-Forge-Jigsaw). Uses jigsaw so you can make kinda dynamic structures built out of many parts like how villages work. (note: in 1.18.2 you can use only json files but in 1.18.0/1 you need code too).
- [Ore gen](https://gist.github.com/TelepathicGrunt/6955dba1aca2636b8816595fa4868b86). Shows how to add a placed feature to any biome using `Feature.ORE` as an example.  
- [Add new buildings to villages](https://gist.github.com/TelepathicGrunt/4fdbc445ebcbcbeb43ac748f4b18f342). Adds new piece to a pool of a jigsaw structure so similar would work for bastions, woodland mansions and many modded structures. Note: *You will still need to add a jigsaw block to your nbt structure piece so that it can connect to the other pieces and spawn. For example, adding to village's houses pool means you need a jigsaw block with "minecraft:building_entrance" in the Name field and the jigsaw block is facing outward towards the street on the bottom edge of the piece.*
- [Add modded crop blocks to village farms](https://gist.github.com/TelepathicGrunt/c02333993a1c35dea26fdb98fead5074). This method can stack with other people attempting to do the same. This works by adding a new processer to the structure piece that randomly replaces some wheat blocks. You could do other block replaces in other structures with the same technique. 
- [Explination of biome tags](https://gist.github.com/TelepathicGrunt/b768ce904baa4598b21c3ca42f137f23). the replacement for `BiomeCategory` for 1.18.2 and later. If you add a custom biome, you should put it in a tag!

## Author: Commoble

- [Add features defined with json to vanilla biomes](https://gist.github.com/Commoble/573ac69ac95818daf643d443bf67b260). 