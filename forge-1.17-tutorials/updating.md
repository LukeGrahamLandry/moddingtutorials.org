# Updating from 1.16 to 1.17

Before you do anything, please **make a backup** so you can roll back if something goes wrong. Be careful to follow these steps in order!  

First open the terminal / CMD and navigate to your mod folder with the command `cd /path/to/mod/folder`. 

## Mappings

First make sure you are using the official mappings. Find the mappings line in your build.gradle and if it already has `channel: 'official'`, you can skip this step. Read [the mappings tutorial](mappings) if you want a more detailed explanation of how they work.

1. run the command in the terminal / CMD `./gradlew updateMappings -PUPDATE_MAPPINGS="1.16.5" -PUPDATE_MAPPINGS_CHANNEL="official"`. this will change your code to use the new mappings (on windows, remove the `./` prefix)
2. go back to your build.gradle file and change the mappings line to `mappings channel: 'official', version: '1.16.5'`

## Update Gradle

Update to the newer version of gradle. Navigate to your mod folder and run this terminal command. (on windows remove the `./` prefix).

```
./gradlew wrapper --gradle-version=7.1.1 --distribution-type=bin
```

Open your build.gradle and change the version of ForgeGradle in the first dependancies block to 5.1+.

```
classpath group: 'net.minecraftforge.gradle', name: 'ForgeGradle', version: '5.1.+', changing: true
```

Make sure you're using forge's more recent maven url.

```
maven { url = 'https://maven.minecraftforge.net' }
```

## Change Class Names

Add this line to your build.gradle. It should be near the top, under the other plugins
```
apply from: 'https://raw.githubusercontent.com/SizableShrimp/Forge-Class-Remapper/main/classremapper.gradle'
```

Run this command in the terminal / CMD (on windows, remove the `./` prefix)
```
./gradlew -PUPDATE_CLASSNAMES=true updateClassnames
```

When thats done running, you can remove the apply plugin line from your build.gradle if you want.  

> This script is by SizableShrimp and released under the Creative Commons Zero v1.0 Universal license. just incase the repository is no longer up, I have a mirror you can use at https://raw.githubusercontent.com/LukeGrahamLandry/modding-tutorials/forge-1.17.1/classname_update_script.gradle

## Finish Updating build.gradle 

Change the java version to 16.

```
java.toolchain.languageVersion = JavaLanguageVersion.of(16)
```

Change to the 1.17 mappings

```
mappings channel: 'official', version: '1.17.1'
```

Change to minecraft 1.17 and the newer version of forge in the dependencies block 

```
minecraft 'net.minecraftforge:forge:1.17.1-37.0.104'
``` 

You will have to run the gradle command to generate your IDE run configurations again (genIntellijRuns or genEclipseRuns).

## Update to Java 16

Download the java 16 JDK. 

In intellij this is how you make sure your project is set to use it:

1. File > Project Structure  
    Use the "Project SDK" dropdown menu to select java 16

2. Wrench Icon > Gradle Settings  
    Use the "Gradle JVM" dropdown menu to select java 16

## Update mods.toml

open your src/main/resources/META-INF/mods.toml file.  

change the forge loader version to  

    loaderVersion="[37,)" 

change the required version for the `minecraft` dependency to  

    versionRange="[1.17.1,1.18)"

and the required version for the `forge` dependency to  

    versionRange="[37,)"

## Code Fixes

You will probably have to remove some unused package imports that try to reference nonexistant packages from 1.16. Many of Vanilla's package names have changed. The class names update gradle script will have added imports for the new packages but may not have removed the old ones. So if you mod won't build because of these, just remove the broken import lines, you may have to look through all your .java files to find them.

The package names for some important forge classes have changed (`fml` -> `fmllegacy`). You can try to your mod to find any errors. You should be able to just delete any invalid package imports from the top of your files and use your IDE to reimport them. Effected Classes: RegistryObject

There are a few other changes to make in your code. For example,

- ForgeRegistries.TILE_ENTITIES -> ForgeRegistries.BLOCK_ENTITIES
- the `harvestTool` and `harvestLevel` block properties methods do not exist. You must use tags instead (described in the [basic blocks tutorial](basic-blocks))
- the `getBurnTime(ItemStack)` method on items is now `getBurnTime(ItemStack, @Nullable RecipeType<?>)`
- xRot and yRot on players/other entities are now private. you must use the getter and setter methods. 
- the `hasTileEntity` method does not exist, the block should implement `EntityBlock` instead
- instead of a tile entity implementing `ITickableTileEntity`, use the following code:

```
// on the Block class
@Nullable
@Override
public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level world, BlockState state, BlockEntityType<T> type) {
    return type == TileEntityInit.MOB_SLAYER.get() ? MobSlayerTile::tick : null;
}

// on the BlockEntity class

public static <T extends BlockEntity> void tick(Level level, BlockPos pos, BlockState state, T be) {
    MobSlayerTile tile = (MobSlayerTile) be;

    // your code here
}
```

- a bunch of stuff with entity models and rendering has changed. I'll add info about this as my tutorials get to it