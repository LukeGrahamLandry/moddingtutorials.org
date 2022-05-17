# Recipes

In this tutorial we learn about the json recipe formats used by crafting tables, furnaces, smithing tables and stone cutters. We also use an event handler to manipulate the anvil's outputs. 

## Setup

In src/main/resources/data/mod_id (make sure to replace that with your own mod id) make a new folder called recipes. 

Each recipe you make will be defined by a json file you put in that folder. The convention is to name these files after the output item but it doesn't matter. Each recipe json will have a `type` key which defines which crafting blocks will check the recipe and which other keys your json must use to define the recipe. 

## Shaped (Crafting Table)

The `pattern` list defines the shape of your recipe. Each character represents a different type of item. 

The `key` map assigns a character to each item you use in the recipe. You can set the `item` to the resource location of a vanilla or modded item. You can define a `tag` instead which will allow any item from the given tag to fulfill the recipe (for example, chests can be crafted with any type of wooden plank).

The result's `item` field tells it what item to output. It can also add a `count ` field to `result` if you want it to give more than one. 

    {
        "type": "minecraft:crafting_shaped",
        "pattern": [
            "###",
            " / ",
            " / "
        ],
        "key": {
            "#": {
                "item": "firstmod:smile"
            },
            "/": {
              "tag": "minecraft:planks"
          }
        },
        "result": {
            "item": "firstmod:pink_pickaxe"
        }
    } 

## Shapeless (Crafting Table)

Ingredients is a list of items to use to craft. The result tells it the item to output and how many. The arrangement of items in the crafting table will not effect the output of the recipe. 

    {
      "type": "minecraft:crafting_shapeless",
      "ingredients": [
        {
          "item": "minecraft:ender_pearl"
        },
        {
          "item": "firstmod:smile"
        }
      ],
      "result": {
        "item": "minecraft:diamond",
        "count": 3
      }
    } 

## Furnace

The ingredient item is the input and the result is the output. You can also set the amount of experience points it should give the player and how long it takes to cook (in ticks). 

    {
        "type": "minecraft:smelting",
        "ingredient": {
            "item": "firstmod:smile_block"
        },
        "result": "firstmod:smile",
        "experience": 1.0,
        "cookingtime": 100
    } 

You can use the same json format with other `type` keys to make recipes for the other types of furnace. Vanilla has conventions for which types of items each furnace can process and how long they should take but you are not required to follow them. 

- `"minecraft:smoking"`: Smoker, used for food, typically twice as fast as a normal furnace
- `"minecraft:campfire_cooking"`: Camp fire, used for food, typically three times slower than a normal furnace
- `"minecraft:blasting`: Blast furnace , used for ores, typically twice as fast as a normal furnace

## Smithing

The `base` ingredient goes in the first slot of the smithing table and the `addition` goes in the second to create the `result`.

    {
      "type": "minecraft:smithing",
      "base": {
        "item": "minecraft:wooden_axe"
      },
      "addition": {
        "item": "minecraft:cobblestone"
      },
      "result": {
        "item": "minecraft:stone_axe"
      }
    }

## Stone Cutter

The `ingredient` defines the input (item or tag) and the `result` defines the output item (you can also set the `count` key to something). 

Vanilla uses the stone cutter for more efficient crafting of stone items but you are not limited to that. Unlike other recipe types, you are able to define multiple recipe json files for the same input because the stone cutter has multiple output slots so it can show all possibilities. 

    {
      "type": "minecraft:stonecutting",
      "ingredient": {
        "item": "firstmod:smile_block"
      },
      "result": "minecraft:stone_stairs",
      "count": 2
    }

## Anvil 

### Repair 

If you want to repair a custom item in an anvil, there are two methods on your item class to override. `isRepairable` is self explanatory. `isValidRepairItem` takes in the item stacks on the left and right of the anvil and returns true if the right is a valid repair item (only called if the left is your item).

```
@Override
public boolean isRepairable(ItemStack stack) {
    return true;
}

@Override
public boolean isValidRepairItem(ItemStack tool, ItemStack material) {
    return material.getItem() == ItemInit.SMILE.get();
}
```

### Combine

You can also make anvil recipes to craft things similarly to the smithing table. However, these are not data driven, they must be done from code. You do this by listening for the `AnvilUpdateEvent`, manually checking the inputs and changing the output. The forge events system is described in more depth in [the events tutorial](/events).

The first step is always to make a class in your `event` package with the `EventBusSubscriber` annotation. 

```
@Mod.EventBusSubscriber(bus = Mod.EventBusSubscriber.Bus.FORGE)
public class AnvilHandler {

}
```

I'm going to start by making two classes that describe the types of recipes we might want to make with the anvil. The first will describe repairing an item, it will take in the item we want to repair, the material we will repair it will, the amount of durability to return, the number of levels it should cost, and how many of the material it should cost. Vanilla does some math to figure out how many times it has to repair the item to determine these last 3 values but I'm lazy so we'll just make the player manually repair the item multiple times (improving this is left as an exercise to the reader).

We will start by making a class that defines a recipe much like a smithing table. You tell it the two input items and the output item. 

```
static class CombineRecipe {
    public final Item left;
    public final Item right;
    public final Item out;
    protected CombineRecipe(Item left, Item right, Item out){
        this.left = left;
        this.right = right;
        this.out = out;
    }
}
```

Next I'll make a list that will hold all my anvil combining recipes. I'll make a public method that adds all the recipes I want to these lists. 

```
private static ArrayList<CombineRecipe> combineRecipes = new ArrayList<>();

public static void initAnvilRecipes()
    combineRecipes.add(new CombineRecipe(Items.BEEF, Items.COAL, Items.COOKED_BEEF);
}
```

This init method must be called from somewhere when the game starts but it must be after modded items have been initialized so they can be referenced by our recipes. I'll call it on the `FMLCommonSetupEvent` with the following method in my **main class**. Note that the event listener for this is added by the line `modEventBus.addListener(this::setup);` in my constructor.  

```
private void setup(final FMLCommonSetupEvent event) {
	AnvilHandler.initAnvilRecipes();
}
```

Finally make a method that listens for the `AnvilUpdateEvent` and loops through our list to apply our recipes. For each thing in the liss it will check that both the left and right slots in the anvil match the inputs we expect and then set the correct output and level cost. 

Note that since vanilla expects the item on the left to be a tool, it will always consume the entire stack. This means that you should set the size of the output stack and how much of the right stack to require (`setMaterialCost`) based on the size of the left stack. I'm also setting the experience cost of the craft based on this but remember that the value of levels does not increase linearly (level twenty is worth much more than 20 level ones). This way its more efficient to craft one at a time than a whole stack, you may want to do a more clever calculation to prevent this. 

```
@SubscribeEvent
public static void handleRepair(AnvilUpdateEvent event){
    combineRecipes.forEach((data) -> {
        if (event.getLeft().getItem() == data.left && event.getRight().getItem() == data.right){
            event.setOutput(new ItemStack(data.out, event.getLeft().getCount()));
            event.setCost(event.getLeft().getCount());
            event.setMaterialCost(event.getLeft().getCount());
        }
    });
}
```

## Brewing Stand

Brewing stand recipes are not data driven, they must be done from code. Also note that there is no requirement that the inputs and outputs actually be potions. 

This should be done on the `FMLCommonSetupEvent` so that items will already be registered so you can directly reference them. Make sure to properly listen for the event! `BrewingRecipeRegistry` has a list of all the combinations that are checked by the brewing stand. You can use the `addRecipe` method to add to it. 

The first argument is an ingredient that will go in the bottom water bottle slots (this should not be stackable because of how vanilla's code works). The second argument is an ingredient that goes in the top slot (like netherwart). The final argument is the item stack to output when the recipe is finished. 

```
private void setup(final FMLCommonSetupEvent event) {
    BrewingRecipeRegistry.addRecipe(Ingredient.of(Items.DIAMOND_AXE), Ingredient.of(ItemInit.SMILE.get()), new ItemStack(Items.NETHERITE_AXE));
}
```

Of course, this can also be used to create recipes for your own custom potions once they've been registered. This will be covered in the Effects tutorial. Join [the discord server](https://discord.gg/uG4DewBcwV) or [the email list](https://buttondown.email/LukeGrahamLandry) to be notified when it is released.  