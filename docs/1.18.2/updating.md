# Updating from 1.17.1 to 1.18.2

Before you do anything, please **make a backup** so you can roll back if something goes wrong. Be careful to follow these steps in order!  

If you have a 1.16 mod that you want to update to 1.18, you must also apply the code changes between 1.16 and 1.17. Consult the [updating from 1.16 to 1.17](/1.18.2/updating-to-1.17) tutorial. 

First open the terminal / CMD and navigate to your mod folder with the command `cd /path/to/mod/folder`. 

## Update Gradle

Update to the newer version of gradle. Navigate to your mod folder and run this terminal command. (on windows remove the `./` prefix).

```
./gradlew wrapper --gradle-version=7.3
```

## Finish Updating build.gradle 

Change the java version to 17.

```
java.toolchain.languageVersion = JavaLanguageVersion.of(17)
```

Change to the 1.18 mappings

```
mappings channel: 'official', version: '1.18.2'
```

Change to minecraft 1.18 and the newer version of forge in the dependencies block 

```
minecraft 'net.minecraftforge:forge:1.18.2-40.1.48'
``` 

You will have to run the gradle command to generate your IDE run configurations again (genIntellijRuns or genEclipseRuns).

## Update to Java 17

Download the java 17 JDK. (you may be able to do this through your ide or just google for it)

In intellij this is how you make sure your project is set to use it:

1. File > Project Structure  
    Use the "Project SDK" dropdown menu to select java 17

2. View > Tool Windows > Gradle > Wrench Icon > Gradle Settings  
    Use the "Gradle JVM" dropdown menu to select java 17

## Update mods.toml

open your src/main/resources/META-INF/mods.toml file.  

change the forge loader version to  

    loaderVersion="[38,)" 

change the required version for the `minecraft` dependency to  

    versionRange="[1.18,1.19)"

and the required version for the `forge` dependency to  

    versionRange="[38,)"

> note, this states that your mod will run properly on 1.18, 1.18.1 and 1.18.2, that may or may not be what you want. 

## Code Fixes

### Package Names 

The package names for some important forge classes have changed (the `fmllegacy` package no longer exists). You can try to your mod to find any errors. You should be able to just delete any invalid package imports from the top of your files and use your IDE to reimport them. 

Alternatively, intellij users can use the following migration map to do it automatically: https://gist.github.com/gigaherz/aef4327298473307ae92a6e754fce0d2 

First, download that xml file and put it in migration folder (location will depend on operating system and intellij version)  

- windows: `%APPDATA%\JetBrains\IdeaIC2021.2\migration`
- linux: `~/.config/JetBrains/IdeaIC2021.2/migration`
- mac: `~/Library/Application Support/JetBrains/IdeaIC2021.2/migration`

Then if you restart intellij and go to Refactor > Migrate, select `FMLLagacy refactorings` from the drop down and click run. It will take some time to scan your code and then you can click Do Refactor. 

### Code Changes

There are a few other changes to make in your code. For example,

- on your block entities, do **not** override `save`. Instead, override `saveAdditional` (which now returns `void`)
- info about changes to tags and registries: https://gist.github.com/SizableShrimp/ddcbe9a9862cc4a0f526c42ae49b2c1d
- info about changes to entity model rendering : https://gist.github.com/gigaherz/7115024820f55717bc40a6e2247c6aca
- info about changes to tool system: https://gist.github.com/gigaherz/691f528a61f631af90c9426c076a298a
- heres a tool that can help you update world gen data packs: https://misode.github.io/upgrader/

Overview: https://gist.github.com/ChampionAsh5357/73c3bb41d3a8de2d020827e0069314a7 