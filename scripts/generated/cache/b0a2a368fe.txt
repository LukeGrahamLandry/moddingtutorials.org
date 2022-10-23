# Simple XP Config

- Forge 1.16.5
- Commissioned by *viiizee* & *spiderking23*

Makes sources of experience points more configureable. The first time you open a world, it will generate the default config files which do not change vanilla behaviour. 

## Spawner Mobs

- edit the file `world/serverconfig/xpspawnercontrol-server.toml`

Allows you to stop mobs spawned by mob spawners from dropping experience. The config file has two values. 

- `isBlacklist`: Whether the entity list is a blacklist (true) or a whitelist (false) of removing experience drops
- `entityList`: A list of all of the entity registry names which this mod will affect (uses json formating, e.g. ["minecraft:zombie"])

This functionality is a direct port of [Xp Spawner Control](https://www.curseforge.com/minecraft/mc-mods/xp-spawner-control) (1.12, GPL) by bright_spark

## Block Breaking

- edit the file `world/serverconfig/blockxpdrops.json`
- you must restart the world after editing the config file to see changes

Lets you add xp drops to certain blocks. These xp drops will not apply when you are using silk touch. 

This will work for any modded method of breaking blocks that fires forge's `BlockEvent.BreakEvent`;

The file is a list of json objects representing xp drop rules.
- `blocks`: list of the registry names of blocks this rule should apply to. required
- `amount`: the amount of xp to drop. required
- `chance`: the probability for that xp to drop when a block meeting the conditions is broken. A decimal number where 1 means always and 0 means never (defaults to 1). 
- `state`: an object with the block state properties that must be true for this rule to apply. Only supports integer properties (like crops `age`, cauldren/composter `level`, cake `bites`, turtle `eggs`). This can be left off to ignore the blockstate. 
- `ignoreCancel`: defaults to false. when true, xp will be dropped even if the break event is canceled by another mod (useful for Dynamic Trees). 
- 
Example that makes grown crops drop xp sometimes:

```json
[
  {
    "blocks": ["minecraft:potatoes", "minecraft:carrots", "minecraft:wheat"],
    "amount": 5,
    "chance": 0.33,
    "state": {
      "age": 7
    }
  },
  {
    "blocks": ["minecraft:nether_wart", "minecraft:beetroots"],
    "amount": 3,
    "chance": 0.5,
    "state": {
      "age": 3
    }
  }
]
```

## Crop Growth Modifiers 

- edit the file `world/serverconfig/cropgrowthmodifiers.json`
- you must restart the world after editing the config file to see changes

Lets you prevent crops from growing under certain conditions. 

This will work for any modded crop blocks that fire, and respect the results of, forge's `BlockEvent.CropGrowEvent.Pre` and `BonemealEvent`.

The file is a list of json objects representing crop growth rules. 
- `blocks`: list of the registry names of blocks this rule should apply to. required
- `chance`: the chance that the block will be allowed to grow if this rule applies. 1 is always, 0 is never. defaults to 0.
- `effectBoneMeal`: whether this rule should apply when bonemeal is used. defaults to true. (when false, the rule only applies to natural growth)
- `minY`: the rule will apply to crops above this y level
- `maxY`: the rule will apply to crops below this y level
- `minTemp`: the rule will apply to crops in biomes above this temperature
- `maxTemp`: the rule will apply to crops in biomes below this temperature

The following example will make potatoes never grow naturally below y=60 or above y=100. Cactus will grow at 30% speed below y level 40. 
> Note that the max and min refer to making the rule apply and preventing the crop growth. So the crop may grow only above the maxY for the this to apply. When block y=minY, the rule will apply (and in this case stop the growth)

```json
[
  {
    "blocks": ["minecraft:potatoes"],
    "chance": 0,
    "maxY": 60,
    "minY": 100,
    "effectBoneMeal": true
  },
  {
    "blocks": ["minecraft:cactus"],
    "chance": 0.3,
    "maxY": 40
  }
]
```