# Torcherino

- previous maintainers: Moze_Intel, sci4me, 3llemes

## Features

- adds "torcherinos" that speed up nearby tile entities and random block ticks (like crop growth).
- right click a torcherino to open gui to control area of effect and speed.
- each torcherino has a lantern and jack-o-lantern variant as well.

### Config 

Edit `minecraft/config/sci4me/Torcherino.cfg`. Defaults will be generated on first load. Settings are applied to all worlds. 
Settings should be the same on the client and server as they are not synced. 

- `random_tick_rate` (int): additional multiplier on random block tick rate caused by torcherinos
- `log_placement` (bool): whether to log when torcherinos are placed in the world. useful for server admins tracking down lag
- `blacklisted_blocks` (list): identifiers of blocks that should not be sped up
- `blacklisted_blockentities` (list): identifiers of block entities that should not be sped up
- `online_mode` (string): When set to ONLINE, Torcherinos only run its owner is currently online. If set to RESTART then Torcherinos will run for anyone who has logged in since the server started. Any value allows them to run whenever their chunk is loaded. 
- `tiers` (list): additional tiers of torcherino to register. 

Tier definition format:

- `name` (string): will be included in registry name. must be unique
- `max_speed` (int): max multiplier on tick speed caused by this tier 
- `xz_range` (int): horizontal radius in blocks for this tier to effect
- `y_range` (int): vertical range in blocks for thier tier to effect

You must provide block state, model, texture, lang, loot table, and recipe files for any non-default tiers you add. 
All generated blocks will be automatically added to the internal blacklist and their identifiers will be as follows:

- torch: `torcherino:NAME_torcherino`
- lantern: `torcherino:NAME_lantern`
- jack-o-lantern: `torcherino:NAME_lanterino`

### API 

Other mods may access part of the config system from their own code. Use [cursemaven](https://www.cursemaven.com) to add the dependency to your dev environment. 
To avoid users crashing when torcherino is not installed, make sure the api is only class-loaded if the `torcherino` mod is present. 

To guarantee stability between minor versions, we recommend you avoid accessing the `TorcherinoImpl` class directly. Instead, retrieve the api instance as follows,

```
TorcherinoAPI api = TorcherinoAPI.INSTANCE;
```

#### Blacklists 

These methods should only be called after blocks are registered. 

Blocks may be added to the blacklist with `blacklistBlock(ResourceLocation)` or `blacklistBlock(Block)`. 
Block entities may be added to the blacklist with `blacklistBlockEntity(ResourceLocation)` or `blacklistBlockEntity(BlockEntityType)`. 
These entries will be applied in addition to the configured blacklists above. 

You can check if something is blacklisted with `isBlockBlacklisted(Block)` or `isBlockEntityBlacklisted(BlockEntityType)`.

#### Tiers 

`ImmutableMap<ResourceLocation, Tier> tiers = api.getTiers()` will provide all currently registered torcherino tiers. `getTier(ResourceLocation)` will provide data on a specific registered tier. 

