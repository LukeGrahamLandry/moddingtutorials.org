
<head>
    <link rel="canonical" href="https://gist.github.com/ChampionAsh5357/ef542d1ae4e1a5d096f7f8b51f5e0637" />
</head>

<pre>
Source: <a href="https://gist.github.com/ChampionAsh5357/ef542d1ae4e1a5d096f7f8b51f5e0637">https://gist.github.com/ChampionAsh5357/ef542d1ae4e1a5d096f7f8b51f5e0637</a> <br></br>
License: Creative Commons Attribution 4.0 International 
</pre> 

# Minecraft 1.18.x -> 1.19.x Mod Migration Primer

This is a high level, non-exhaustive overview on how to migrate your mod from 1.18.x to 1.19.x using Forge.

This primer is licensed under the [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/), so feel free to use it as a reference and leave a link so that other readers can consume the primer.

If there's any incorrect or missing information, please leave a comment below. Thanks!

## 1.19.3 and Onwards

Mojang changed their minor version strategy from 1.19.3 onwards, so to properly update past 1.19.2, please refer to the below primers:

- [1.19.2 -> 1.19.3 by ChampionAsh5357](https://gist.github.com/ChampionAsh5357/c21724bafbc630da2ed8899fe0c1d226)

## TODO

- Registry changes
    - Removal of IForgeRegistryEntry and no more unique registry types
    - NewRegistryEvent and RegisterEvent
    - @ObjectHolder now requires registry to be passed in
- Component is now simply mutable with the ComponentContents changing for literal, translatable, etc.
- IExtensionPoint changes
    - displayTest can now be set through the mods.toml
- DataProvider#run now takes in a CachedOutput rather than a HashCache
- IGlobalLootModifier now takes in and returns an ObjectArrayList rather than a List
- BannerPatterns now have their own registry (also CatVariant, PaintingVariant, and Instrument)
    - BannerPattern should be registered to the registry and put in the `minecraft:no_item_required` tag if they don't have an accompanying `BannerPatternItem`
- Biome Modifiers replacing the BiomeLoadingEvent
- Client refactor: https://gist.github.com/amadornes/cead90457e766f6d4294cb6b812f91dc
    - Renames: https://gist.github.com/SizableShrimp/252bcd6d7bf97276781fce99a00c9eb9
- GLMs now use codecs instead of a serializer interface