# Environment Setup

How to setup a forge development environment for 1.17.1 with the official mappings. We download java 16, forge and IntelliJ. We also rename our main package and class and update the mods.toml file.

## Downloading

First, download the JDK (java 16 development kit). Go to [oracle.com](https://www.oracle.com/java/technologies/javase/jdk16-archive-downloads.html) and select your operating system. It will ask you to make an account but you can borrow someone else's credentials from [bugmenot.com](http://bugmenot.com/view/oracle.com). Just copy paste them in and if the first doesn't work, try the next one.

Next you need the Forge 1.17.1 MDK (mod development kit) from [files.minecraftforge.net](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.17.1.html). Get the recommended version cause its the most likely to work.
![forge mdk download page](/img/download-forge.png)
When you click the button to download the MDK it will send you to a page with ads. Very important not to click any of them (even if they look like pop ups from your OS), just wait a few seconds until the skip button appears in the top right and click that to download.

Then you need an IDE to write your code. Download intellij from [jetbrains.com](https://www.jetbrains.com/idea/download) and get the community addition because it's free.

## Installing

Double click the JDK download to open it. Just go though the installer and agree to everything. It will probably need an administrator password and take a long time to install.

Then unzip the forge MDK and rename the folder to the name of your mod. You can remove the license, readme and credits files.

Finally, launch intellijj. The first screen should let you choose some settings. You probably want dark theme but for everything else the defaults are fine. Then you want to click 'open a project'. Select the forge folder you just renamed and give it a while to do the indexing (there should be a little loading bar at the bottom of the screen).

## Setup

In the project explorer on the left open `src/main/java` and right click `com.example.examplemod` Choose refactor > rename and call it `tld.nameorwebsite.modid` (so I did ca.lukegrahamlandry.firstmod). Make sure there's no spaces or capital letters. Open ExampleMod.java and right click the name of the class to rename it to ModNameMain. This is your mod's main class. Some of these functions can be removed but it's fine if you leave them.

Make a public static string that holds your mod id. This is how the forge mod loader will recognize your mod. It's generally based on your mod's name, unique and all lowercase with no special characters. You will use this often, don't forget it. It is also very important to change the value in the @Mod annotation at the top of the class to reference your mod id. I took out some of the unnecessary methods from this base class just to clean it up a bit. Here's what it looks like now:

    // imports up here // 
    
    @Mod(FirstModMain.MOD_ID)
    public class FirstModMain {
        public static final Logger LOGGER = LogManager.getLogger();
        public static String MOD_ID = "firstmod";
    
        public FirstModMain() {
            final IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
    
            modEventBus.addListener(this::setup);
    
            // Register ourselves for server and other game events we are interested in
            MinecraftForge.EVENT_BUS.register(this);
        }
    
        private void setup(final FMLCommonSetupEvent event) {
            
        }
    }
    

Open `src/main/resources/META-INF/mods.toml` It has a bunch of key value pairs that mostly set the information shown on the mods list in game. The only one you have to change is the modId (to whatever you had in your main class). You must keep the modLoader and loaderVersion the same but the fields lower down like display name can be whatever you want, they'll be displayed in the mods list ingame. You should also choose a license (I like the MIT license personally). 

    modLoader="javafml"
    loaderVersion="[37,)"
    
    license="MIT"
    
    [[mods]]
    
    modId="firstmod"
    
    
    # ... more fields down here

The `build.gradle` file tells it what dependancies to download (like Minecraft and Forge). Set the group to whatever you named your package (and click the elephant icon in intellij to update these settings).

    group = "ca.lukegrahamlandry.firstmod"
    

Close intellij, open the terminal, navigate to your mod folder and run the command below (on windows use CMD and you don't need the ./ prefix). It will take a while to run.

    cd /path/to/mod/folder
    ./gradlew genIntellijRuns
    

## Run the game

You can open intellij again and run the game by clicking the little green play button in the top right. If you have any problems with that you can also run it with the command below.

    ./gradlew runClient

## Info Files

In the top level of your mod folder you'll find a few extra files about forge. I suggest taking out `changelog.txt` and `credits.txt`. You should replace `license.txt` with a license that has information about how people are allowed to use your code (learn more about license options at [choosealicense.com](https://choosealicense.com/)). Finally replace `readme.txt` with `README.md` so you can use [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) and GitHub will render it properly. This file should contain information about your mod's features, supported versions and perhaps a link to your CurseForge page once you're ready to release your mod. 

## Alternative Setup

**If you are just starting to learn modding and followed the instructions above, this section does not apply to you. Skip ahead to the next tutorial :)**

If you have an existing 1.16 modding environment that you would like to update to 1.17, follow [my updating to 1.17 tutorial](updating).

