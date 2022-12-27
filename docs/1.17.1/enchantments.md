# Enchantments

A tutorial on making enchantments. We will make an enchantment that goes on boots and builds a bridge of blocks under you when you walk. 

## Init

Enchantments are registered the same way as items and blocks. 

Start by making a class called `EnchantmentInit` in your `init` package and setup a deferred register. Then register a new enchantment which references a class we haven't created yet. 


    public class EnchantmentInit {
        public static final DeferredRegister<Enchantment> ENCHANTMENTS = DeferredRegister.create(ForgeRegistries.ENCHANTMENTS, FirstModMain.MOD_ID);
    
        public static final RegistryObject<Enchantment> BRIDGE = ENCHANTMENTS.register("bridge", BridgeEnchantment::new);
    }

Don't forget to actually call this deferred register from the constructor of your main class!

```
EnchantmentInit.ENCHANTMENTS.register(modEventBus);
```

## Enchantment Class

Create a package called `enchants` and a class that extends `Enchantment` (named whatever you used to create the enchantment above). Instead of taking constructor parameters, I'll hard code them since we only use this class for one enchantment. 

```
public class BridgeEnchantment extends Enchantment {
    public BridgeEnchantment() {
        super(rarity, enchantType, slotType);
    }
}
```

### Constructor Values

- `rarity`: is a value of the `Enchantment.Rarity` enum (COMMON, UNCOMMON, RARE or VERY_RARE). Each of the 4 options has a different weight value (ranging from 10 to 1) which defines how likely it is to be chosen by the enchantment table. 
- `enchantType`: is a value of the `EnchantmentCategory` enum. It defines which types of items the enchantment can be applied to. Vanilla has options for each type of armour and tool but we will cover making custom ones shortly. 
- `slotType`: is an array of values of the `EquipmentSlot` enum which defines the slots where the game will look for the enchantment on an entity. If you want to be valid for all slots, use `EquipmentSlot.values()`. `EnchantmentHelper.getEnchantmentLevel(Enchantment, LivingEntity)` is the method that vanilla uses to find the highest level of an enchantment effecting an entity and it respects this slotType value. This means, for example, that even if you edit the nbt of a chest plate to add the frost walker enchantment, the game will not recognize it because it only looks at your feet. 

For this example I'll be using `super(Enchantment.Rarity.RARE, EnchantmentCategory.ARMOR_FEET, new EquipmentSlot[]{EquipmentSlot.FEET});`

### Useful Methods

The `Enchantment` class has several methods that you can override to decide more details about your enchantment. 

#### getMaxLevel

Sets how many levels of your enchantment can be applied to an item. For example, protection is 4 and mending is only 1.

```
@Override
public int getMaxLevel() {
	return 3;
}
```

#### checkCompatibility

Defines other enchantments that cannot be applied at the same time as yours. For example, `InfinityEnchantment` uses this to not be on an item with mending. I don't want mine to go with frost walker so I'll check for that in this method. 

```
@Override
protected boolean checkCompatibility(Enchantment other) {
   return super.checkCompatibility(other) && other != Enchantments.FROST_WALKER;
}
```

#### doPostAttack

Called when a player (and most other entities) with this enchantment (on its helmet, chest, legs, boots, main hand, or off hand) attacks an entity. This will run multiple times if the attacker has multiple items with your enchantment. Vanilla uses this for bane of arthropods to give spiders a brief slowness effect. 

This does not respect the `slotType` set in the constructor. Which means that with the code below, whether you are properly wearing boots with my enchant or just holding them, things you attack will burn. 

```
@Override
public void doPostAttack(LivingEntity attacker, Entity target, int level) {
    target.setRemainingFireTicks(40);
}
```

#### doPostHurt

Called when something with this enchantment is attacked. Same as above, this will run multiple times for multiple items and does not respect the enchantment's `slotType`. Vanilla uses this for the thorns enchantment. 

```
@Override
public void doPostHurt(LivingEntity target, Entity attacker, int p_151367_3_) {
	target.addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 100));
}
```

#### Simple Booleans

Methods you can override to return a boolean that answers the following questions about how you can acquire the enchantment. 

- `isTreasureOnly`: like mending and frost walker. Makes it not show up in the enchantment table or trades. 
- `isTradeable`: will it show up in librarian trades? 
- `isAllowedOnBooks`: will the enchantment table be able to put this on books? 
- `isCurse`: should it be considered a curse? True makes the text on an item red instead of grey. Makes the grindstone not able to remove it. 

## Custom Behavior

Anywhere in your own code you can check for your enchantment on a player (or other entity). The following line will give you the highest level of the enchantment on the player's valid items. if `level` is 0, the player does not have that enchantment. 

```
int level = EnchantmentHelper.getEnchantmentLevel(EnchantmentInit.BRIDGING.get(), player);
```

You can use this for basically anything you want. Often you'll want to do it in response to something happening so you'll listen for an event. 

I'm going to make an inner class in my `BridgingEnchantment` class to react to the tick event (it could be a full class in your `events` package but I like the organization of this better). The  `buildBridge` will fire every tick for each player. The first line makes sure that it only fires on the server side and that it fires at the start of the tick processing (the event is actually fired twice per tick).

```
@Mod.EventBusSubscriber(bus = Mod.EventBusSubscriber.Bus.FORGE)
public static class BridgeBuildingHandler {
    @SubscribeEvent
    public static void buildBridge(TickEvent.PlayerTickEvent event){
        if (event.phase == TickEvent.Phase.END || event.player.level.isClientSide()) return;

        int level = EnchantmentHelper.getEnchantmentLevel(EnchantmentInit.BRIDGE.get(), event.player);

        // your code here
    }
}
```

Next I'll do something based on the level of my enchantment the player has. 

If the player has my enchantment and is holding shift, I'll check the block below them. If it is air, I'll set it to slime instead. This will form a nice bridge to walk on so you can kinda fly while shifting. 

```
if (level > 0 && event.player.isShiftKeyDown()){
    BlockState state = event.player.level.getBlockState(event.player.blockPosition().below());
    if (!state.isAir()) return;
    event.player.level.setBlockAndUpdate(event.player.blockPosition().below(), Blocks.SLIME_BLOCK.defaultBlockState());
}
```

## Applying to Custom Items

If you want to make an enchantment that will only show up when you put an item you made in the enchantment table, you must make your own `EnchantmentCategory`. We use the static `create` method on `EnchantmentCategory` which takes a string name for the type and a predicate that takes in the item being enchanted and returns a boolean representing whether it can accept the enchantment. Then simply make your enchantment class, pass your new `EnchantmentCategory` into the constructor and register it with the deferred register in your `EnchantmentInit` as before. 

This example would allow the enchantment to apply to the teleport staff item we made in the [advanced items tutorial](/advanced-items). 

    public class DistanceEnchantment extends Enchantment {
        static EnchantmentCategory TELEPORT_STAFF_TYPE = EnchantmentCategory.create("teleport_staff", item -> item == ItemInit.TELEPORT_STAFF.get());
    
        public DistanceEnchantment() {
            super(Rarity.COMMON, TELEPORT_STAFF_TYPE, new EquipmentSlot[]{EquipmentSlot.MAINHAND, EquipmentSlot.OFFHAND});
        }
    }

You will also need to override the `getEnchantmentValue` method in your item class to return a value larger than 0. This is the [enchantibility value](https://minecraft.fandom.com/wiki/Enchanting_mechanics#How_enchantments_are_chosen) of your item which is used to determine how many and how rare enchantments are applied an the enchanting table. 

```
// TeleportStaff.java

@Override
public int getEnchantmentValue() {
	return 10;
}
```

## Assets

Your enchantment will need an entry in your lang file, just like items/blocks. 

    "enchantment.firstmod.bridge": "Bridging",

## Practice

- Make the `DistanceEnchantment` created above increase the range of the teleport staff. (For example, by default you can teleport up to 15 blocks, distance level 1 might allow 30 and level 2 could allow 45). This will require editing the `TeleportStaff` class made in the [advanced items tutorial](/advanced-items). 

