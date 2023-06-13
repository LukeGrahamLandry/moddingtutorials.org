---
sidebar_position: 1
---

# Environment Setup

How to setup a forge development environment for 1.19.2 with the official mappings. We download java 17, forge and IntelliJ. We also rename our main package and class and update the mods.toml file.

## Downloading

First, download the JDK (java 17 development kit). Go to [adoptium.net](https://adoptium.net/temurin/releases/) and select your operating system. Choose installer for easier start as it configures system path for you, or install zip and configure java path later in your IDE (IntelliJ). Adoptium Temurin is a free implementation of JDK, you do not need any account to download and use it.

Next you need the Forge 1.19 MDK (mod development kit) from [files.minecraftforge.net](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.19.html). Get the recommended version cause its the most likely to work.
![forge mdk download page](/img/download-forge.png)
When you click the button to download the MDK it will send you to a page with ads. Very important not to click any of them (even if they look like pop ups from your OS), just wait a few seconds until the skip button appears in the top right and click that to download.

Then you need an IDE to write your code. Download intellij from [jetbrains.com](https://www.jetbrains.com/idea/download) and get the community addition because it's free.

## Installing

Double click the JDK download to open it. Just go though the installer and agree to everything. It will probably need an administrator password and take a long time to install.

Then unzip the forge MDK and rename the folder to the name of your mod. You can remove the license, readme and credits files.

Finally, launch intellijj. The first screen should let you choose some settings. You probably want dark theme but for everything else the defaults are fine. Then you want to click 'open a project'. Select the forge folder you just renamed and give it a while to do the indexing (there should be a little loading bar at the bottom of the screen).

## Setup

In the project explorer on the left open `src/main/java` and right click `com.example.examplemod` Choose refactor > rename to change your package name to something unique so you don't conflict with other mods. The convention is to named it based on a domain you own, reversed like `tld.website.modid`, so I did `ca.lukegrahamlandry.firstmod`. Make sure there's no spaces or capital letters. Open ExampleMod.java and right click the name of the class to rename it to ModNameMain. This is your mod's main class. Some of these functions can be removed but it's fine if you leave them.

Make a variable that holds your mod id. This is how the forge mod loader will recognize your mod. It's generally based on your mod's name, unique and all lowercase with no special characters. You will use this often, don't forget it. It is also very important to change the value in the `@Mod` annotation at the top of the class to reference your mod id. I took out some of the unnecessary methods from this base class just to clean it up a bit. Here's what it looks like now:

```java
// imports up here // 

@Mod(FirstModMain.MOD_ID)
public class FirstModMain {
    public static final Logger LOGGER = LogManager.getLogger();
    public static final String MOD_ID = "firstmod";

    public FirstModMain() {
        final IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();

        modEventBus.addListener(this::setup);
    }

    private void setup(final FMLCommonSetupEvent event) {
        
    }
}
```   

Open `src/main/resources/META-INF/mods.toml` It has a bunch of key value pairs that mostly set the information shown on the mods list in game. The only one you have to change is the modId (to whatever you had in your main class). You must keep the modLoader and loaderVersion the same but the fields lower down like display name can be whatever you want, they'll be displayed in the mods list in game. You should also choose a license, go to https://choosealicense.com for more information. 

```toml
modLoader="javafml"
loaderVersion="[41,)"

license="ARR"

[[mods]]

modId="firstmod"

# ... more fields down here
```

The `build.gradle` file tells it what dependancies to download (like Minecraft and Forge). Set the group to whatever you named your package (and click the elephant icon in intellij to update these settings).

```java
group = "ca.lukegrahamlandry.firstmod"
```    

Close intellij, open the terminal, navigate to your mod folder and run the command below (on windows use CMD and you don't need the ./ prefix). It will take a while to run.

```
cd /path/to/mod/folder
./gradlew genIntellijRuns
```

## Run the game

You can open intellij again and run the game by clicking the little green play button in the top right. If you have any problems with that you can also run it with the command below.

```
./gradlew runClient
```

## Info Files

In the top level of your mod folder you'll find a few extra files about forge. I suggest taking out `changelog.txt` and `credits.txt`. You should replace `license.txt` with a license that has information about how people are allowed to use your code (learn more about license options at [choosealicense.com](https://choosealicense.com/)). Finally replace `readme.txt` with `README.md` so you can use [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) and GitHub will render it properly. This file should contain information about your mod's features, supported versions and perhaps a link to your CurseForge page once you're ready to release your mod. 

## Alternative Setup

- If you are using an Apple Silicon (m1) computer, read the [Apple Silicon tutorial](/m1)
- If you have an existing 1.18, 1.17, or 1.16 modding environment that you would like to update to 1.19, follow [my updating tutorial](updating).

## Later versions

> TODO: update this page with the right version numbers for 1.19.2. I think the rest of the tutorials are already correct. 

This tutorial is for 1.19.2, NOT 1.19.3 or 1.19.4. Mojang changed how they deal with breaking changes in minor versions so some stuff will be different. I'll probably update it at some point but for now see these resources for an overview of changes.

- 1.19.3: https://gist.github.com/ChampionAsh5357/c21724bafbc630da2ed8899fe0c1d226
- 1.19.4: https://gist.github.com/ChampionAsh5357/163a75e87599d19ee6b4b879821953e8
