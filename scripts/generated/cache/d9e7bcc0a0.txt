# Entity Rain Mod - Smells Fishy

- forge 1.18.2
- commissioned by coda

Cause brief entity rain events where different creatures fall from the sky. The default data pack adds a fish rain event. 

## Data Packs

New entity rain events are defined by json files in the `entityrain` folder of data packs. 
The format of these files is as follows, 

- `radius` (int): the number of blocks around each player that entities will spawn (the area will be a square)
- `height` (int): how many blocks above the ground the entities will spawn
- `spawnRate` (int): an entity will spawn near each player every x ticks (on average) while the event is active
- `spawn` (list of EntitySpawnOption): the types of entities that will spawn during this event
- `when` (EventConditions): what situations this event should start under
- `chance` (int): how likely the event is to start. the chance for the event to start each check is (1/chance). the check is made for each possible event whenever it switches between day/night or raining/clear. the event will last until the next check. 
- `replace` (boolean): what happens if another data pack has already defined an event of this name. if true, the existing event will be deleted and this file will be used instead. if false, the contents of `spawn` and `dimensions` will be added to the existing event. the defaults to true.

You can see the default fish rain json data [on github](https://github.com/LukeGrahamLandryMC/smells-fishy-mod/blob/main/src/main/resources/data/smellsfishy/entityrain/fish.json).

### EntitySpawnOption

- `entity` (string): the registry key of the entity type (ie. `minecraft:zombie`)
- `weight` (int): how likely this entity is compared to the others. chance of each entry is (weight / totalWeight) 
- `biomes` (list of string): resource locations of biomes to whitelist (allow this spawn in). **optional**, when not defined the spawn will occur in all biomes. Tags are supported, prefix with `#`
- `biomesIsBlacklist` (boolean): when true, the `biomes` filter is inverted, the spawn will NOT occur in the listed biomes. **optional**, defaults to false

> the data for currently active rain events does not change when the /reload command is used, you must wait for it to start again to see the effects

### EventConditions

- `raining` (boolean): can the event start while its raining
- `notRaining` (boolean): can the event start while its NOT raining
- `day` (boolean): can the event start in the daytime
- `night` (boolean): can the event start in the nighttime
- `dimensions` (list of string): the registry keys of the dimensions the event may happen in (ie. `minecraft:overworld`)
- `biomes` (list of string): resource locations of biomes to whitelist (allow rain to occur in). **optional**, when not defined the event will cause spawns in all biomes. Tags are supported, prefix with `#`
- `biomesIsBlacklist` (boolean): when true, the `biomes` filter is inverted, the entities will NOT be spawned in the listed biomes. **optional**, defaults to false

## Commands

To test your data packs, you can force change the active entity rain event in your current dimension with the following commands (requires OP permissions).  

```
/entityrain start <key>
/entityrain stop
```
