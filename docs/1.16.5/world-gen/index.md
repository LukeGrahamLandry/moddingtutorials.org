---
sidebar_position: 11
---

# World Gen

Since 1.16, the way minecraft handles world generation has been shifting towards being based on json files in data packs rather than making you write code. Eventually I'd like to write my own tutorials on this but for now I'll try to collect a list of resources made by people that understand it much better than me.  

If you have questions specificlly about how world gen works, [the Minecraft Worldgen Discord Server](https://discord.gg/BuBGds9) might have someone who can help.  

## MC Wiki

- [json format for making a custom dimension](https://minecraft.fandom.com/wiki/Custom_dimension)
- [json format for making biomes](https://minecraft.fandom.com/wiki/Biome/JSON_format)
- [other world gen json formats](https://minecraft.fandom.com/wiki/Custom_world_generation). (Noise settings, carvers, surface builders, features, structure sets, jigsaw pools, structure sets)

## Author: TelepathicGrunt

- [Create a new structure that generates in the world](https://github.com/TelepathicGrunt/StructureTutorialMod/tree/1.16.3-Forge-jigsaw). Uses jigsaw so you can make kinda dynamic structures built out of many parts like how villages work. 
- [Add new buildings to villages](https://gist.github.com/TelepathicGrunt/4fdbc445ebcbcbeb43ac748f4b18f342/28122cb039b64c739c11a7432c23d11aefd518ad). Adds new piece to a pool of a jigsaw structure so similar would work for bastions, woodland mansions and many modded structures. Note: *You will still need to add a jigsaw block to your nbt structure piece so that it can connect to the other pieces and spawn. For example, adding to village's houses pool means you need a jigsaw block with "minecraft:building_entrance" in the Name field and the jigsaw block is facing outward towards the street on the bottom edge of the piece.*
- [Add modded crop blocks to village farms](https://gist.github.com/TelepathicGrunt/c02333993a1c35dea26fdb98fead5074). This method can stack with other people attempting to do the same. This works by adding a new processer to the structure piece that randomly replaces some wheat blocks. You could do other block replaces in other structures with the same technique. 
- [Example of a surface builder class](https://pastebin.com/XU4pJJtX) *The way they work is their method is ran for every x/z position in the biome. The idea is that you simply loop from the top terrain height (startHeight) to y = 0 and replace the first few blocks of every surface you meet along the way. Of course, you may want to add noise or change the behavior of the surfacebuilder completely. Register the surfacebuilder to the surface builder registry to be able to either configured it with json files for json biomes. Or you could configure it in code, register it to WorldGenRegisteries.CONFIGURED_SURFACE_BUILDER, and then add it to your coded biome.*
- Ore generation

```java
public static ConfiguredFeature<?,?> CONFIGURED_COAL_ORE;

// register to the Mod event bus
public static void commonSetup(FMLCommonSetupEvent event) {
   event.enqueueWork(() -> {
    // the OreFeatureConfig.FillerBlockType tells it which types of blocks its allowed to replace
    CONFIGURED_COAL_ORE = Feature.ORE.configured(new OreFeatureConfig(OreFeatureConfig.FillerBlockType.NATURAL_STONE, Blocks.COAL_ORE.getDefaultState(), 17)).range(128).squared().count(20)
        
    Registry.register(WorldGenRegistries.CONFIGURED_FEATURE, new ResourceLocation(StructureTutorialMain.MODID, "coal_ore"), CONFIGURED_COAL_ORE);
   }
}

// register to the Forge event bus
public void biomeModification(final BiomeLoadingEvent event) { 
    event.getGeneration().getFeatures(GenerationStage.Decoration.UNDERGROUND_ORES).add(() -> CONFIGURED_COAL_ORE);
    }
```

## Author: Commoble

- [Dynamiclly generated dimensions](https://gist.github.com/Commoble/7db2ef25f94952a4d2e2b7e3d4be53e0). If you just have a a few static dimensions, you're better off using json files to create them. 

## Author: gigaherz

- Brief example of how to make your entity spawn in certain biomes

```java
@SubscribeEvent
public static void biomeLoading(final BiomeLoadingEvent event){
    RegistryKey<Biome> biomeRegistryKey = RegistryKey.getOrCreateKey(Registry.BIOME_KEY, event.getName());
    if (isBiomeAllowed(biomeRegistryKey)){
        MobSpawnInfo.Spawners spawn = new MobSpawnInfo.Spawners(EntityInit.YOUR_ENTITY.get(), weight, minPackSize, maxPackSize);

        event.getSpawns().withSpawner(CLASSIFICATION, spawn);
    }
}
```