# Advanced Items

A tutorial on making items with unique custom behaviours. We will make a food that gives a potion effect, a furnace fuel and an item that teleports you forward when right clicked.

## Food

In your ItemInit class copy the code for a basic item and change the names.

    public static final RegistryObject<Item> FRUIT = ITEMS.register("fruit",
                () -> new Item(new Item.Properties().tab(ModCreativeTab.instance)));
    

Then on the Item.Properties, call the food function. This takes in a Food created with a Food.Builder. The Food.Builder has a variety of functions that let you set different properties of the food. For example, nutrition lets you set how much hunger it restores. When you're done call build to create the Food object.

    new Item.Properties().tab(ModCreativeTab.instance)
                        .food(new FoodProperties.Builder().nutrition(4).saturationMod(2).build()
    

To make your food grant a potion effect when eaten, call the `effect` function of your `FoodProperties.Builder` (before you call `build()`). This takes a supplier for an `MobEffectInstance` which takes the effect you want to give, the duration (in ticks so 20 is one second), and the amplifier (0 is level I). The effect method also takes the likelihood your effect will be applied (1.0F is always and 0F is never). So this code will have a 50% chance to give fire resistance I for 10 seconds.

    .effect(() -> new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 200, 0), 0.5F)

You can also call `.alwaysEat()` if you want to be able to eat the food even when your hunger is full (like golden apples).

## Fuel

Again, start by copying the basic item code and change the names. This time change the supplier from an Item to a new class you will create soon.

    public static final RegistryObject<Item> FUEL = ITEMS.register("fuel",
                () -> new FuelItem(new Item.Properties().tab(ModCreativeTab.instance)));
    

Make a new package called items and create the FuelItem class you referenced when making the item. It should extend Item and have a constructor that takes both an Item.Properties to pass on to the super constructor and an int to use as burn time. Don't forget to make a field to save that burn time.

    public class FuelItem extends Item {
    	private final int burnTicks;
        public FuelItem(Properties properties, int burnTimeInTicks) {
            super(properties);
            this.burnTicks = burnTimeInTicks;
        }
    }
    

Then override the `getBurnTime` method. As arguments, this takes the `ItemStack` being used as fuel and the recipe type (SMELTING, SMOKING or SMITHING) both of which we will ignore. It returns the burn time in ticks. It will return the int we saved from the constructor. 

    @Override
    public int getBurnTime(ItemStack itemStack, @Nullable RecipeType<?> recipeType) {
        return this.burnTicks;
    }
    

Now go back to ItemInit, import this class and update the constructor when you create your fuel item to include the burn time. Items generally take 200 ticks to smelt so 3200 should cook 16 items (twice as much as coal).

    new FuelItem(<...>, 3200)

## Right click behaviour

Start the same way as for a fuel. In ItemInit, copy paste basic item, rename and change the class. Make a new class in your items package that extends item and uses the default constructer.

    // ItemInit.java
    
    public static final RegistryObject<Item> TELEPORT_STAFF = ITEMS.register("teleport_staff",
                () -> new TeleportStaff(new Item.Properties().tab(ModCreativeTab.instance)));
    
    // items/TeleportStaff.java
    
    public class TeleportStaff extends Item {
        public TeleportStaff(Properties properties) {
            super(properties);
        }
    }
    

To do something when it's right clicked, override use. It takes in the world which lets you effect blocks and stuff, the player that used it and whether it was main or offhand.

    @Override
    public InteractionResultHolder<ItemStack> use(Level world, Player player, InteractionHand hand) {
    	return super.use(world, player, hand);
    }

So in that method we can use a function built into the item class to do a raycast in the direction the player is looking and save the first thing it hits in a variable. Then we can set the player's position to that position. That will teleport the player forward.

    BlockHitResult ray = getPlayerPOVHitResult(world, player, ClipContext.Fluid.NONE);
    BlockPos lookPos = ray.getBlockPos();
    player.setPos(lookPos.getX(), lookPos.getY(), lookPos.getZ());

If you tried it now you'd notice that when you try to teleport straight down it you get your feet stuck in the block. This is because we told it to literally set your feet to the same place as the block. We can update the line creating lookPos to offset the position based on the direction you're looking at the block.

    BlockPos lookPos = ray.getBlockPos().relative(ray.getDirection());

Currently the range of the teleport is just the players mining range. To fix that, we can make our own version of this getPlayerPOVHitResult method. If you command click (MacOS Intellij, idk what it is for windows) on the method you can jump to its declaration in the Item class. Its a bunch of confusing math but we can just copy it into our class and try to figure it out. 

You can see its getting the position of the player's eyes, then calculating the direction you're looking and multiplying that by this a float called d0. So if you change that, you change the length of the vector and thus the range. If there's no block close in front of you, you'll just teleport the full distance. Let's just name our new function something different so we can be sure we aren't messing up any other behaviors. Don't forget to switch the use method to be using our new `rayTrace`.

    protected static BlockRayTraceResult rayTrace(Level world, Player player, ClipContext.Fluid fluidMode) {
            double range = 15;
    
            float f = player.getXRot();
            float f1 = player.getYRot();
            Vector3d vector3d = player.getEyePosition(1.0F);
            float f2 = Mth.cos(-f1 * ((float)Math.PI / 180F) - (float)Math.PI);
            float f3 = Mth.sin(-f1 * ((float)Math.PI / 180F) - (float)Math.PI);
            float f4 = -Mth.cos(-f * ((float)Math.PI / 180F));
            float f5 = Mth.sin(-f * ((float)Math.PI / 180F));
            float f6 = f3 * f4;
            float f7 = f2 * f4;
            Vector3d vector3d1 = vector3d.add((double)f6 * range, (double)f5 * range, (double)f7 * range);
            return world.clip(new ClipContext(vector3d, vector3d1, ClipContext.Block.OUTLINE, fluidMode, player));
        }

If you want to limit how often the item can be used you can add a cool down. The second argument is the time they have to wait before using it again in ticks (1/20 of a second). You can also make teleporting reset how far you've fallen so you can use the item to escape fall damage.

    player.getCooldowns().addCooldown(this, 60);
    
    player.fallDistance = 0F;
    

You can also play a sound. This will play the enderman's teleport sound that the player's position. The last two arguments are volume and pitch. 

    world.playSound(player, player.getX(), player.getY(), player.getZ(), SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 1.0F, 1.0F);
    

If we want to give the players some help understanding our mod, we can add a tool tip when they hover over the item in their inventory. So override appendHoverText and add to the tooltip. The TextComponent class is just a string that Minecraft can render.

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level worldIn, List<Component> tooltip, TooltipFlag flagIn) {
        tooltip.add(new TextComponent("teleports you where you're looking"));
    
        super.appendHoverText(stack, worldIn, tooltip, flagIn);
    }

If you want less clutter for the player, you can only show this when they're holding shift. So make a new package called util and a class called KeyboardHelper. Everything here will be static, we can get the game window so we can get user input. Then make some functions to check if they're holding shift, space, or control respectively. For shift and control we are checking both the left and right one. Don't forget to import all these classes. Note: this class can only be used on the client side, [Learn More](sides).

    public class KeyboardHelper {
        private static final long WINDOW = Minecraft.getInstance().getWindow().getWindow();

        @OnlyIn(Dist.CLIENT)
        public static boolean isHoldingShift() {
            return InputConstants.isKeyDown(WINDOW, GLFW.GLFW_KEY_LEFT_SHIFT) || InputConstants.isKeyDown(WINDOW, GLFW.GLFW_KEY_RIGHT_SHIFT);
        }

        @OnlyIn(Dist.CLIENT)
        public static boolean isHoldingControl() {
            return InputConstants.isKeyDown(WINDOW, GLFW.GLFW_KEY_LEFT_CONTROL) || InputConstants.isKeyDown(WINDOW, GLFW.GLFW_KEY_RIGHT_CONTROL);
        }

        @OnlyIn(Dist.CLIENT)
        public static boolean isHoldingSpace() {
            return InputConstants.isKeyDown(WINDOW, GLFW.GLFW_KEY_SPACE);
        }
    }

Then you can change your appendHoverText method to check if the player is holding shift.

    if (KeyboardHelper.isHoldingShift()){
        tooltip.add(new TextComponent("teleports you where you're looking"));
    }
    

If you want it to use durability you can get the item stack being used, increase how damaged it is (because its stored as how much damage has been taken not how much durability remains). Note that setting the damage doesn't make it break when it hits 0. So we have to check if its zero and if so make the stack empty.

    ItemStack stack = player.getItemInHand(hand);
    stack.setDamageValue(stack.getDamageValue() + 1);
    if (stack.getDamageValue() >= stack.getMaxDamage()) stack.setCount(0);
    

Then you can go back to ItemInit. Dont forget to import your special item class. If you did the durability thing you have to set the durability to something in the `Item.Properties`. Giving it durability automatically makes the max stack size one (normally set by the `stacksTo` method on the properties builder).

    new Item.Properties().tab(ModCreativeTab.instance).durability(50)
    

## Other Methods

The `Item` class has many other methods you can override for interesting behaviour. Here's just a few of them

- `useOn`: called when right clicked targeting a block
- `interactLivingEntity`: called when right clicked targeting an entity
- `hurtEnemy`: called when the player hits an entity while holding the item
- `onCraftedBy`: called when taken out of a crafting slot. 
- `inventoryTick`: called once every tick (20 times per second) while it is in someone's inventory. 
- `isValidRepairItem`: can the second item be used to repair the first item in an anvil

## Assets

You can setup the textures, models and lang file exactly the same as for basic items. Just remember to change the names of the file and any time you use the name of the item.

## Run the game

If you run the game the items show up in the creative tab and have textures. You can eat the food and sometimes get fire resistance. My fuel coal can be used in a furnace and smelts 16 items. Finally the staff will teleport you and lose durability.

## Related Tutorials 

- [Tools & Armor](tools-armor): allow your item to be used as a tool or worn as armor
- [Arrows](arrows): allow bows to use your item as ammo
- Custom Bow tutorial coming soon. Join [the discord server](https://discord.gg/uG4DewBcwV) or [the email list](https://buttondown.email/LukeGrahamLandry) to be notified when it is released. 

## Practice

- Make an item that replaces any block you right click with dirt

    - hint: `world.setBlock(pos, Blocks.VANILLA_NAME.defaultBlockState());`

- Make an item that gives poison to any entity you right click

    - hint: `entity.addEffect(new MobEffectInstance(MobEffects.VANILLA_NAME, duration, amplifier));`

- Make an item that propels the player in the direction they're looking

    - hint: `player.setDeltaMovement(x, y, z);`

- Make an item that places a torch automatically while in the inventory of a player in darkness

    - hint: `Math.max(world.getBrightness(LightType.BLOCK, pos), world.getBrightness(LightType.SKY, pos)) > 7`
