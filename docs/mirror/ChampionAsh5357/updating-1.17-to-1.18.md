
<head>
    <link rel="canonical" href="https://gist.github.com/ChampionAsh5357/73c3bb41d3a8de2d020827e0069314a7" />
</head>

<pre>
Source: <a href="https://gist.github.com/ChampionAsh5357/73c3bb41d3a8de2d020827e0069314a7">https://gist.github.com/ChampionAsh5357/73c3bb41d3a8de2d020827e0069314a7</a> <br></br>
License: Creative Commons Attribution 4.0 International
</pre> 

# Minecraft 1.17.x -> 1.18.x Mod Migration Primer

This is a high level, non-exhaustive overview on how to migrate your mod from 1.17.x to 1.18.x using Forge.

This primer is licensed under the [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/), so feel free to use it as a reference and leave a link so that other readers can consume the primer.

If there's any incorrect or missing information, please leave a comment below. Thanks!

## TODO

- BlockEntity#save -> BlockEntity#saveAdditional
    - If you are storing BlockEntities somewhere, don't call save. Call saveWithFullMetadata(), saveWithId() or saveWithoutMetadata(), depending on your needs.
- ClientboundBlockEntityDataPacket uses static `create` method
    - Gets CompoundTag from BlockEntity#getUpdateTag unless a function is specified
- Constants$BlockFlags was removed and are now obtained from their vanilla location in `Block`
- FMLNetworkConstants -> NetworkConstants
- RecipeProvider#buildShapelessRecipes -> RecipeProvider#buildCraftingRecipes
- (Forge) ItemModelProvider#generateModels -> ItemModelProvider#registerModels
- @CapabilityInject removed in favor of CapabilityManager#get
- PlayerEvent$Clone#wasDead field -> PlayerEvent$Clone#isWasDeath method
- RenderWorldLastEvent -> RenderLevelLastEvent
- Java 16 -> Java 17
- `ItemOverride` -> `BakedOverride`
- ItemProperties#registerGeneric no longer private
- PlacedFeatures changed again I think
    - Ordering is now in a list instead of nested iirc
- Renames and refactors: https://gist.github.com/TheCurle/d00b4201369d6536d5e7fdd8040862b1
- Registries and TagKeys from Shrimp: https://gist.github.com/SizableShrimp/ddcbe9a9862cc4a0f526c42ae49b2c1d
    - Specify how tags are queried or gotten
    - How registry keys should be obtained from values