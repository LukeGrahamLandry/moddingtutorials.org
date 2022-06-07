# Updating from 1.18 to 1.19

Before you do anything, please **make a backup** so you can roll back if something goes wrong. Be careful to follow these steps in order!  

If you have a 1.16 mod that you want to update to 1.19, you must also apply the code changes between 1.16 and 1.18. Consult the [updating from 1.16 to 1.17](/o17/updating) tutorial and the [updating from 1.17 to 1.18](/o18/updating) tutorial. 

## Update build.gradle 

Change to the 1.19 mappings

```
mappings channel: 'official', version: '1.19'
```

Change to minecraft 1.18 and the newer version of forge in the dependencies block 

```
minecraft 'net.minecraftforge:forge:1.19-41.0.1'
``` 

You will have to run the gradle command to generate your IDE run configurations again (genIntellijRuns or genEclipseRuns).

## Update mods.toml

open your src/main/resources/META-INF/mods.toml file.  

change the forge loader version to  

    loaderVersion="[41,)" 

change the required version for the `minecraft` dependency to  

    versionRange="[1.19,1.20)"

and the required version for the `forge` dependency to  

    versionRange="[41,)"

## Code Fixes

There are a few changes to make in your code. For example,

- the `TextComponent` class is gone. instead of using `new TextComponent("string")`, use `Component.literal("String")`
- registry events have changed. If you're automaticlly registering block items, as i do, revisit the relivent section of the [blocks tutorial](basic-blocks)
- Some methods that previously took a `Random` instance, now want a `RandomSource` (it just became an interface). `Block#randomTick(BlockState, ServerLevel, BlockPos, Random)` becomes `Block#randomTick(BlockState, ServerLevel, BlockPos, RandomSource)`
- if you're using an apple silicon computer, you need to add a new mixin, read [apple silicon tutorial](m1) or you will get an `UnsatisfiedLinkError`