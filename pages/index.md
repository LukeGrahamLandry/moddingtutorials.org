# Minecraft Modding Tutorials

Welcome! 

## About

I make these because I was frustrated by the lack of documentation and useable tutorials for Forge. All the tutorials I could find were long videos of someone talking extremely slowly. I hope to offer an alternative: text tutorials for those who don't need to a visual follow along. Hopefully my tutorials will be less painful to refer to if you happen to forget something.

This site has tutorials for Forge 1.16.5 and Forge 1.17.1, you can use the yellow drop down menu on the left to switch versions. The tutorials use Mojang's official [mappings](mappings) (aka mojimaps). 

If you find text versions hard to follow, I will soon have videos that slowly work through the 1.17 tutorials on [YouTube](https://www.youtube.com/channel/UC8gYhA5SkhI1tajZ5JF2pbQ/). The source code for all my tutorials can be found on [GitHub](https://github.com/LukeGrahamLandry/modding-tutorials). If you're interested in the history of this site, you can read [The Changelog](changelog) and [Why Long Videos?](why-long-video).

## Contact

If you have any questions or feedback about my tutorials, please [join my discord server](https://discord.com/invite/VbZVnRd). We've got a growing community that can help you out with any problems you may have. This is also where I notify people when new tutorials are released. 

## Commissions 

If you have an idea for a mod and would like to commission me to make it a reality, DM me on discord (LukeGrahamLandry#6888). Please prepare a detailed description of the features you want so I can give you a meaningful quote. I will require a 30% deposit before I begin work. Due to time constraints, no commissions under $100 will be taken. I'm happy to work in versions 1.16.x or 1.17.x on Forge or Fabric. 

You can also take a look at [my mods](my-mods) for some examples of my past work. 

## Donate 

If you found my tutorials helpful and want more, donating is a great way to encourage their creation. Consider making a recurring donation on [Patreon](https://www.patreon.com/LukeGrahamLandry) or a one time donation via [PayPal](https://www.paypal.me/LukeGrahamLandry).

## Topics 

This is an index of the content covered on this site.

### Overview
- [Java Basics](java-basics)
    - summary of Java syntax 
- [Mappings](mappings)
    - the deobfuscation of minecraft's code
- [Registries](registries)
    - how minecraft handles game objects
- [Server vs Client](sides)
    - the separation of logic and rendering

### Tutorials 
- [Environment Setup](environment-setup)
    - install Java and an IDE
    - set up the forge mdk
- [Basic Items](basic-items)
    - an item (with a texture)
    - a new creative tab
- [Advanced Items](advanced-items)
    - a food (with a chance to give a potion effect)
    - an item that can be used as furnace fuel
    - an item that will teleport the player forward when right clicked
- [Basic Blocks](basic-blocks)
    - a block (with a texture) that drops itself when broken
    - automatically register block items
- [Advanced Blocks](advanced-blocks)
    - a block that explodes if right clicked while holding gun powder
    - allow crops to grow on your block
    - rarely spawn cacti 
    - have a placement rotation like furnaces
- [Tools and Armor](tools-armor)
    - a set of tools with custom stats 
    - a set of armor with custom stats
    - a piece of armor that gives a potion effect while being worn
    - a piece of armor that lights attackers on fire 
- [Tile Entities](tile-entities)
    - a block that damages nearby mobs on each tick
    - let your tile entity respond to being right clicked
    - save variables on world restart with NBT
    - sync your tile entity's data between the server and the client
- [Enchantments](enchantments)
    - armor enchant that sets targets on fire and gives a potion effect when attacked
    - checking for your enchantment on events for custom behavior (build a bridge below as you walk)
    - make your custom items enchantable 
- [Recipes](recipes)
    - shaped and shapeless in the crafting table
    - furnaces, smokers, camp fires and blast furnaces
    - smithing table and stone cutter
    - use an event to craft in an anvil
- [Custom Bow and Arrows](bow-and-arrows)
    - register a projectile entity that explodes when it hits someone
    - an arrow item that lets you shoot your custom projectile from a vanilla bow or crossbow
    - a custom bow 

## Thanks

This site is made possible by my wonderful [patrons, clients, and contributors](credits)