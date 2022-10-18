# Introduction to Minecraft Modding 

Minecraft is a fun game with a world made of cubes. Over time, dedicated players decided there were not enough types of cubes so they started writing code that modified the base game (mods) to add new content. This website will teach you how to write your own mods to implement any new features you can imagine. 

## Versions

Over time, Mojang/Microsoft releases updates to Minecraft that add new content. Unfortunately, they also change lots of things about how Minecraft's code works internally each update as well. This means that any given mod is only compatible with the version of minecraft it was made for. Porting mods between versions is sometimes trivial but often quite difficult, depending on how much has changed in the vanilla code that the mod must interact with.

This site has tutorials for versions 1.19, 1.18.2, 1.17.1, and 1.16.5. You can switch between them by using the drop down menu at the top of the nav bar on the left of each tutorial page. 

## Mod Loaders

Minecraft does not natively allow you to load code that modifies the game. Helpfully, some very clever people wrote some complicated code that provides a framework that can load user created chunks of code (called mods) that are run along side minecraft's existing code. The programs that do this for you are called mod loaders. They generally provide an additional layer of abstraction that helps you interact with minecraft's code to change the game more easily (called an api). 

Important to note is that players can only use one mod loader at a time so mods written for different mod loaders are incompatable. 

Each mod loader will distribute an installer program that players can run to add that mod loader to their minecraft installation. It will generally create a new profile in the vanilla launcher so you can still easily choose between different versions or mod loaders. You can also use third party launchers, like CurseForge or MultiMC, to make this process easier. 

### Forge

> Exists because a long time ago, mods did hacky things that were incompatible with each other so it was hard to make big mod packs. 

Forge was one of the first mod loaders and is still by far the most popular. It provides a large api that makes it easier to change lots of things. It patches minecraft's code in many places to add event hooks that will call your mod code to make it easy to change lots vanilla behavior while maintaining compatibility with other mods that try to change similar things (or at least not crashing). There are also helpful things like capabilities (fancy abstract data storage) like Forge Energy (RF) for power, a fluid api, additional attributes (swim speed, gravity), and abstractions over object registration. However, since this api is so large and interacts so much with vanilla's code, forge often takes a long time to update to new Minecraft versions. 

Forge has downloads available all the way back to version 1.1.

### Fabric 

> Exists because the dude runs forge's discord server is mean to people who don't learn java and that's rude. 

Fabric started when minecraft was at 1.14 as a competitor to forge, mostly because forge took a long time to update. Fabric has a more modular philosify than forge, they keep the mod loader as light as possible so it can be updated to new versions quickly. They also provide the fabric api that makes it easier to impliment lots of thing as a mod that can be downloaded seperatly. Techniclly, that means that you could write fabric mods without depending on thier api but thats rarely done. Fabric's api is still less all encompassing than forge's so you have to do more things for yourself. Fabric also supports jar-in-jar mods more elegantly than forge which lets you easily bundle dependencies within your own mod file. This two factors combined lead to a culture of obsessively depending on random libraries. 

### Quilt

> Exists because the dude that runs fabric's discord server is mean to trans people and that's rude. 

Quilt is a fork of fabric made because a group of people disagreed with how the fabric community was run. They have their own api (the quilt-standard-library or QSL) and for the time being, maintain a fork of the fabric api that reimplements everything so that fabric mods can run on quilt with minimal changes. Which means that in practice, there's no reason for players to use the fabric loader at all as quilt can load fabric mods and more. If this lures players over, then the quilt team can break compatibility with fabric and perhaps keep most of the players using quilt. They have a lot of cool technical promises as well but thus far there only exists a beta whose selling point is being just as good as fabric and maybe having a more democratic governance system for the project.  

> I'd say that quilt's team has quite the duplicitous scheme going on but I've got to agree transphobia is unpleasant. Plus, if quilt breaks compatibility with fabric then i get to have lots of commissions porting things between them so who am I to complain. 

### Plugins

Plugins are a special type of mod for servers only. Vanilla clients can connect to these modded servers but the types of changes they can make are much more limited. There are many loaders for these that all seem to be forks of each other ([Spigot](https://www.spigotmc.org/), [Bukkit](https://dev.bukkit.org/), [Sponge](https://www.spongepowered.org/), [Paper](https://papermc.io/)). They tend to provide a very abstract api layer over Mojang's code so that developers using them don't have to worry too much about what's really going on. However, this makes them extra difficult to update to new minecraft versions.

I feel that there's really no point in using these plugin apis because the other mod loaders can also make server side only mods (such that vanilla clients can connect to modded servers). However, if you make your server side mod with forge/fabric/quilt, then they have the ability to be used with modded clients as well. The only reason people use plugins is they want to use other plugins that don't have mods that can replace their functionality yet. 

## Distribution

Once you finish writing the code for your mod, you package it into a nice little jar file that people can add to their game by just dropping it in their `minecraft/mods` folder. 

### CurseForge 

CurseForge is the most popular website where people distribute their mods. Developers can write descriptions (with the shittiest text editor in the universe), mark other mods as dependencies, and receive revenue from ads on the site in the form of "curse points" that can be redeemed via PayPal. Players can easily browse through lots of mods and modpacks (with the shittiest search interface in the universe) to collect those they want to play with. CurseForge also has their own Minecraft launcher that automatically installs different versions mod loaders and mod packs, automatically installing any dependencies for the mods you want to play. 

#### Modrinth

Modrinth is an open source competitor to CurseForge that is several orders of magnitude less popular (probably because they don't give ad revenue to mod developers). 

### Github 

Github is a website for sharing source code with other developers. It makes it easy to put the code for your mod online to let other people learn from it. Almost all minecraft mods have thier code freely available on github for the world to enjoy. 

Github uses a version control system called Git. Git lets you easily track changes in your code as you update your mod and add new features, as well as roll back any mistakes easily. This is a ridiculously important tool to learn how to use! It shines most if you end up working with multiple other people on the same project and need to merge your changes together. You should really install the Github Desktop app at some point and play around with it. It may seem strange at first but it will make life so much easier in the long run. 

#### Licensing

When you release your mod, you generally include a license file that tells people what they're allowed to do with your work. For example, 

- can they redistribute your mod? 
- can they make addon mods?
- can they make derivatives like updating your mod to new versions?
- can they use parts of your code in their own mods?
- can they reuse your assets (textures, models, etc) for their own projects?

By default, having no license file makes your work All Rights Reserved, you own the copywrite so nobody's allowed to touch it. You can read more about your options at [choosealicense.org](https://choosealicense.org) but the basics choices are,  

- MIT, which lets anyone do anything they want with your code. (this is what I use for almost everything I release)
- GPL, GNU General Public License, which lets anyone do anything with your code as long as any derivative works they create are also open source under the GPL.
- ARR, All Rights Reserved, nobody is allowed to do anything with your code :(

## Your IDE

The Integrated Development Environment (IDE) is the program you use to write your code. The most popular Java IDEs are Intellij and Eclipse. We'll install Intellij in the [Environment Setup Tutorial](environment-setup) but all the code would work exactly the same with Eclipse or even VS Code.  

These programs are basically text editors but with extra features like code completion (basically really good context aware spell check for code), error detection and utilities for debugging your code. The most important ability of your IDE is being able to look through minecraft's base code to see what you're interacting with and how they implement things. In Intellij, you can just command/control click on a class or method to "go to definition" and see what code it corresponds to. The second most important thing is Hot Swapping. This lets you swap in changes to your code without needing to restart the entirety of minecraft so you can test out changes more quickly (this can be a bit tricky to setup).  

### Gradle

Gradle is the build system used for making minecraft mods. You write a special file called `build.gradle` that tells your computer how to download minecraft's base code and dependencies and then how to build your mod against that into one cohesive program. Whatever IDE you use should include support for gradle so it knows exactly how to interpret that file to do everything it needs to. Gradle is a very powerful tool that can seem a bit confusing at first so generally you'll just stick with the template `build.gradle` provided by your mod loader's example mod. 

## Mappings

Read more about this system on the Forge blog: http://blog.minecraftforge.net/personal/sciwhiz12/what-are-mappings

## Getting Started

Congratulations! Now you're ready to make your own minecraft mod.  

1. Make sure you **learn the Java programming language**. This is what you will be writing in to make your mod and making sure you have a strong understanding before you start will save a lot of headaches. I go over some of the basics in my [Java Tutorial](java-basics) but its far from complete and there are probably more entertaining resources available online anyway. 
2. Read the [Environment Setup Tutorial](environment-setup). It will how you how to install the correct version of the Java, a program to help you write your code, and a template for your mod that will install the minecraft dependencies. 
3. Go through my other tutorials. If this is your first time doing something like this, its probably a good idea to go through them in order. However, if you're confident in your programming abilities, feel free to skip around. Read the [Topics Page](topics) for more details on the content of each tutorial. 
4. Eventually you will reach something that won't have a specific tutorial to help you. Hopefully by then you'll be comfortable enough working with Minecraft's code that you'll be able to experiment on your own and figure out everything you need to know. Good luck :)
