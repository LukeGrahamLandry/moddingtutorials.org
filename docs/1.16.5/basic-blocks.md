---
sidebar_position: 4
---

# Basic Blocks

In this tutorial we will register a simple block with a texture and a loot table. It will be a similar process to basic items.

## Concepts 

Blocks are very similar to items. They must be registered so the game knows about them. Each type block is an instance of the `Block` class (not each physical block in the world). Basic traits of your block can be set with a properties object but more complex behaviour will require your own class that extends `Block`. 

## New Block

In your init package make a new class called BlockInit. The code here is mostly the same as in ItemInit. Just make sure to say Block instead of Item everywhere. The string you pass the register function is the block's registry name which will be used for naming asset files later.

```java
public class BlockInit {
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, FirstModMain.MOD_ID);

    public static final RegistryObject<Block> SMILE_BLOCK = BLOCKS.register("smile_block",
            () -> new Block());
}
```

The Block constructer in the supplier takes a Block.Properties object made by calling the `Block.Properties.of`  method. This takes a Material which sets a few characteristics about your block like whether its flammable, how it reacts to pistons, default sounds, whether it blocks player motion, and what tools can mine it by default. Vanilla has many options to chose from, just let your IDE autocomplete from `Material`.

Then your `Properties` object has many other methods you can call to set different traits, just like we did with items. `strength` lets you pass in how long it takes to break and how resistant to explosions it is. `harvestLevel` sets what level of tool you need to mine it (0 is wood, 4 is netherite) and `harvestTool` lets you set what type of tool you need. You have to call `requiresCorrectToolForDrops` if it should be like stone and drop nothing without the tool. If you want it to be a light source you can use lightLevel with a lambda expression that maps a blockstate to a value from 1 to 16. There are many more like `friction` (used by ice), `speedFactor` (used by soul sand) and `jumpFactor` (used by honey). So that supplier might looks something like this:

```java
() -> new Block(Block.Properties.of(Material.STONE).strength(4f, 1200f).harvestLevel(2).harvestTool(ToolType.PICKAXE).requiresCorrectToolForDrops().lightLevel((state) -> 15))
```

You can also use `AbstractBlock.Properties.copy(ANOTHER_BLOCK)` to avoid writing things out repeatedly. All vanilla blocks can be accessed with `Blocks.INSERT_NAME_HERE` so you can copy properties from one of them if you feel like it. Or avoid redundancy by referencing `YOUR_BLOCK.get()`

## Block Item

You need a BlockItem to place your block. You can register it manually like your other items but that's tedious so lets make it automatic. We will use the events system to run some code when the game registers all the other items. You can just copy this code for now or read the [events tutorial](/events) for a more detailed explanation of how events work.

At the top of your class add this line to allow it to subscribe to events.

```java
@Mod.EventBusSubscriber(bus = Mod.EventBusSubscriber.Bus.MOD)
public class BlockInit {
    // ...previous code here...
}
```

Then make a static function with the `SubscribeEvent` annotation. Its argument will be the Item RegistryEvent so it fires when items are supposed to be registered.

In that function get the Item registry and loop through all the blocks. For each block, we make an Item.Properties that puts it in our creative tab. Then we make a BlockItem with those properties to place our block. We register the BlockItem with the same registry name as the block.

```java
@SubscribeEvent
public static void onRegisterItems(final RegistryEvent.Register<Item> event) {
    final IForgeRegistry<Item> registry = event.getRegistry();

    BLOCKS.getEntries().stream().map(RegistryObject::get).forEach( (block) -> {
        final Item.Properties properties = new Item.Properties().tab(ItemInit.ModCreativeTab.instance);
        final BlockItem blockItem = new BlockItem(block, properties);
        blockItem.setRegistryName(block.getRegistryName());
        registry.register(blockItem);
    });
}
```

Instead of doing it this way you could manually register a BlockItem for each of your blocks in your ItemInit class but that's really tedious so I'd advise doing it this way. There might be some blocks you make later where you'll what a unique block item. All you'd have to do is add an if statement to check for that block and create the new BlockItem differently. 

## Main Class

In the constructor of your main class add this line to call the register method of your DeferredRegister (same as for items).

```java
BlockInit.BLOCKS.register(modEventBus);
```

## Assets

In your project folder go to `src/main/resources/assets/mod id`. Make a new folder called blockstates and in your models folder make a new folder called block. In textures make a new folder called blocks and put the png image you want to use for your block's texture. Then go out to `src/main/resources/data/mod id` and make a folder called loot_tables and in that make a folder called blocks.

In blockstates make a file called block_name.json (replace block_name with whatever string you passed in as your registry name). Since this is a simple block, we just need one varient that points to a model. Make sure you change firstmod to your mod id and smile_block to the registry name of your block.

```json
{
    "variants": {
        "": {
            "model": "firstmod:block/smile_block"
        }
    }
} 
```

This is the simplest possible blockstate definition. More complex blocks can have different sides (like grass), rotation (like furnaces and chests), age (like crops or ice) and you can define your own custom properties. The possibilities are endless and will likely be discussed more in depth in another tutorial. 

In models/block make a file called block_name.json. This is the file you'd change if you want different sides of the block to look different (like a grass block) but since I don't, I'll just point to one texture (make sure to change smile_block to the name of your image file).

```json
{
    "parent": "block/cube_all",
    "textures": {
        "all": "firstmod:blocks/smile_block"
    }
} 
```

In models/item make a block_name.json file that just parents off your block model

```json
{
    "parent": "firstmod:block/smile_block"
} 
```

In lang/en_us.json add a line that gives your block a name. Remember to change the mod id and block registry name.

```json
"block.firstmod.smile_block": "Smiley Block"
```

In loot_tables/blocks make block_name.json. This sets what drops when you break the block. This is a simple loot table that just drops the block's item but it could be anything.

```json
{
    "type": "minecraft:block",
    "pools": [
        {
            "rolls": 1.0,
            "entries": [
                {
                    "type": "minecraft:item",
                    "name": "firstmod:smile_block"
                }
            ]
        }
    ]
} 
```

Loot tables are also how drops from entities are determined and what you find in chests. They deserve a tutorial of their own but in the mean time, take a look at [vanilla's loot tables](https://github.com/InventivetalentDev/minecraft-assets/tree/1.16.5/data/minecraft/loot_tables/blocks) and [the wiki](https://minecraft.fandom.com/wiki/Loot_table) for inspiration.

You should end up with a file structure like this:

```
- src/main/resources/
    - assets/modid/
        - blockstates/  
            - block_name.json  
        - models/block/  
            - block_name.json  
        - textures/blocks/
            - block_name.png  
    - data/modid/  
        - loot_tables/blocks  
            - block_name.json  
```

### Data Generators 

If your mod has a lot of blocks that just use their own basic texture, it can be tedious (and error prone) to repeatedly copy the model/blockstate/loot_table json file, just changing a single line each time. Luckily, Minecraft provides a way to generate these files from code. This will be covered in detail in a future tutorial. Join [the discord server](/discord) to be notified when it is released. 

## Run the game

If we run the game, we can see that the block shows up in our creative tab. We can place it and break it with an iron pickaxe
