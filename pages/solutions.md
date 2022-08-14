# Modding Questions and Answers (from discord)

If there's something you want to learn how to do that i dont have a tutorial for and you can't figure out from vanilla's code, feel free to [join my discord server](https://discord.com/invite/uG4DewBcwV) to ask me. This page is a collection of information I've given people on that server so you can search it more easily. It will only be helpful if you're already comfortable with Java! These answers are for a mix of versions so you will have to do some translating. 

> I might add an index and split it into seperate pages to help the SEO at some point if i feel inspired

## how scale and translate text on a gui? 

> QUESTION: I’m using posestack.scale for the scale and just manually tweaking some math for the x and y to get it to look okay. It works but I’m thinking there must be a better way to translate the positions when doing non standard scales like 0.8**

the thing that makes it weird is that when you scale the matrix it scales any translations you've done as well, including the position you told the text to be at. so really what you want is to draw the text centred at (0,0), then scale it, then translate it to where you actually want it. tho calling the translate/scale methods will move everything, not just the text you're trying to work with. it might work if you,

- PoseStack#pushPose
- render text centered on 0,0 (you'll probably need to check the width and height of the component since i'm guessing you pass in the top left coordinate when you render it)
- scale it
- translate to real position
- PoseStack#popPose
and wrap that up into a method that lets you render whatever text at whatever position at whatever scale

## is it a problem to override depreciated methods on Block/Item?

the depreciated warning istelling you that if you ever need to call that method, you should call it from the blockstate/itemstack instead but if you're making your own block/item you do have to override it on the block/item singleton class itself

## what are the parameters of the Slot constructor (for inventory menus)? and how does the slot know how big to be in the gui?

- Container/Inventory: the container of items the slot should mondify 
- index: the container has a list of itemstacks. this is the index in that list that the slot represents. used when `Container#getItem`, `Container#setItem`, and `Container#removeItem` are called by the `Menu`
- x: the x coordinate of the top left corner of the slot's square on the gui
- y: the y coordinate of the top left corner of the slot's square on the gui

you'll notice you dont have to pass in the width/height because all slots are a square of a set size (you'll notice that all the slots in vanilla inventories are the same size).

## what do i do instead of the genIntellijRuns gradle task if i want to use vscode

you dont have to do the generate runs thing, its just a convince thing for the intellij/eclipse people to run the game from within the ide. can just use gradlew runClient from the command line when you want to run the game
other than that, should be exactly the same as long as you can figure out how to make vscode import a gradle project on your own (there is a plugin for it)

## i was following one of your tutorials and dont have one of the packages you mentioned 

the packages are just for organization, doesn’t actually matter, you can just make it if you feel inspired. please learn java more, ty!

## you say to copy a class from vanilla (ie. tool Tiers or ArmorMaterials), how do i see vanilla classes?

in intellij you can press shift twice to search through vanilla classes (theres a little check box in the top right that says “include non project items” or something that you should click so its not just searching your code), im sure eclipse/vscode can do it to but idk the keyboard shortcut  

also, if you're looking at a reference to a vanilla class/method, you can "Go To Declaration", generally by holding command/control and clicking on it

for doing something that tints based on the biome colour (like grass and leaves) look at the vanilla code for how it gets that biome's colour in BlockColors#createDefault which calls GrassColors#get

## how do i make a geckolib animation sync with an attack

geckolib has a pretty good wiki (https://github.com/bernie-g/geckolib/wiki/Home) for the details of making animations play at all. for an attack animation specificly, you'd have a dataparameter on your entity that syncs an int from server to client and then when your attack starts you set that to the length of your animation (in ticks) and decrement it every tick until its 0 and check it on the client (in your animation predicate) to play your animation while its ticking down. my mimic mod has an example you can look at https://github.com/LukeGrahamLandry/mimic-mod (look in the `MimicEntity` and `MimicAttackGoal` classes)

## how do i make the dev environment work on apple silicon for 1.12

absolutly no clue. deal with the slowness of roseta 2 emulating it or upgrade to a version of minecraft from not 5 years ago i guess. if you happen to figure it out, please tell me how and i'll document it here

## how do i make my tile entity save its nbt data when you break the block and place it down again?

can look at how shulker boxes do it. this is their loot table https://github.com/InventivetalentDev/minecraft-assets/blob/1.18.2/data/minecraft/loot_tables/blocks/shulker_box.json and ShulkerBoxBlock overrides getDrops to set a tag through that loot table in a complicated way  
but i think you should be able to just override getDrops to return a list of just an item stack of the block with whatever data written to the tag 

## when i create a FluidTank from my block entity (for capability), what do i pass into the validator?

the validator is just a predicate for which fluids its allowed to store. so like if you want it to store any type of fluid just use `(f) -> true`, or if it should only store water that would be `(f) -> f.getFluid().is(FluidTags.WATER)` and i think thats like if it is ever allowed to store that type of fluid so dealing with like limiting it to a certain capacity is handled separately 

## my data gen isnt working

make sure you are running the gradle `runData` task (ie `./gradlew runData` from the terminal)

## why does calling `forceAddEffect` crash?

`LivingEntity#forceAddEffect` only exists on the client so if you try to call it from server/common code, it will crash. instead, you should always call `LivingEntity#addEffect`, preferably only on the server side (check that `!level.isClientSide()`) and let minecraft sync it to the client on its own

## how do i make a bunch of versions of the same item but change the colour of part of the texture (like leather armor or spawn eggs)

theres a whole thing for having a greyscale overlay texture and then tinting it. its like the one thing forge docs have lol https://mcforge.readthedocs.io/en/1.16.x/models/color/ thats for 1.16 but i think it should be the same. 

you can store which colour it should use in the item stack's nbt tag and read it back when the game wants to apply the tint so you dont need lots of different items. you can also have different layers of texture, defined in your model json file, if you only want to tint part of the texture a certain colour

## how do i replace my arrow render with a blockbench model 

not something i know of a specific tutorial for but i can give general instructions if you're quite comfortable with java. (its pretty much the same as giving any entity a custom model if you can find a tutorial for that except you can't use a LivingEntityRenderer since your arrow isnt a LivingEntity)

- make sure the bb model is in the Java Modded Entity project type
- export it as a java class & import all the packages it needs
- have an EntityRenderersEvent.RegisterLayerDefinitions event listener and call `event.registerLayerDefinition(YourModelClass.LAYER_LOCATION, YourModelClass::createBodyLayer);` (specificlly 1.17+)
- create a renderer class that renders your new model instead of the arrow one. its render method would call renderToBuffer on your model. 
- bind that renderer to your arrow entity type in FMLClientSetupEvent as befor

## i want to make an entity's health configureable but it doesnt sync when i update the config file (it only syncs when the game restarts)

if just got the config value on the `EntityAttributeCreationEvent` or whatever where you bind the base attributes to the entity type, thats not gonna work because that event happens once at the beginning when entity types are registered, it's not called for every entity. to make it actually update live with the config you'd have to have all the entities checking if it changes and applying attribute modifiers to their health to get it to the right value

## how can I increase the melee attack range for a vanilla mob

mixin to `MeleeAttackGoal#getAttackReachSqr`

## how do I check what dimension a player is in?

`player.getLevel().dimension()` gives you a `ResourceKey<Level>` which can be compared to `Level.OVERWORLD`, `Level.NETHER`,  `Level.END`, etc

## how can i make sleeping skip night in another dimension

I it seems to be handled by the SleepStatus class which players are added to in ServerPlayer#startSleepInBed only if the dimension type has natural set to true but you could probably add people on your own. and then ServerLevel#tick checks the doDaylightCycle game rule and sets the time to day if SleepStatus thinks enough people are sleeping.  so maybe some mixins somewhere in there could do what you want. idk if that helps at all 🤷. There's also a PlayerSleepInBedEvent but i think it mostly lets you block sleeps, not allow them

## im looking to make a custom furnace but i do not know where to start

Look at how vanilla furnaces work. Basiclly, make a tile entity that holds items and crafts things every x ticks, bind a container/screen to it so you can put in items, decide how you want to deal with recipes (hard code them or make your own recipes type and use json files)

## how do i make my projectile render like an item

you could extend `ProjectileItemEntity` or just impliment `IRendersAsItem` and then when you bind a renderer to your entity type, you would do `RenderingRegistry.registerEntityRenderingHandler(EntityInit.PUT_NAME_HERE.get(), (m) -> new SpriteRenderer<>(m, Minecraft.getInstance().getItemRenderer()));`

## why am i getting a "player moved wrongly" error

instead of calling `player.setPos(...)`, try `((ServerPlayerEntity)player).connection.teleport(x, y, z, player.yRot, player.xRot, EnumSet.noneOf(SPlayerPositionLookPacket.Flags.class))` (make sure to do it in the if block that checks !isclientside). thats what the teleport command uses 

## my custom cactus block just breaks when it grows 

If you made your cactus based on the vanilla CactusBlock, it breaks if the canSurvive method returns false. vanilla has that method call canSustainPlant on the block state below it, so you should make sure that your plant is a valid block for your plant to grow on. You can do that by overriding canSustainPlant on your custom cactus block and returning true if the state passed in is of your plant. I think this would work, 

```
@Override
public boolean canSustainPlant(BlockState state, IBlockReader world, BlockPos pos, Direction facing, net.minecraftforge.common.IPlantable plantable) {
    BlockState plant = plantable.getPlant(world, pos.relative(facing));

    if (plant.is(this)){
        return true;
    } else {
        return super.canSustainPlant(state, world, pos, facing, plantable);
    }
}
```

## my custom sugarcane/cactus blocks just continues to grow instead of stopping at 3

for the sugar cane, i would think using the same randomTick method as vanilla's SugarCaneBlock would work. it seems to check that there's less than a 3 tall stack of your plant before growing so unless you changed the number in that for loop / took out the if statement, idk

## how would i make a block drop xp like ores do?

vanilla ones use the OreBlock class which just overrides this method (you can return whatever number you want. can give more based on fortune level but should give 0 if they have silk touch)

```
@Override
public int getExpDrop(BlockState state, net.minecraft.world.IWorldReader reader, BlockPos pos, int fortune, int silktouch) {
    return silktouch == 0 ? RANDOM.nextInt(7) : 0;
}
```

## my non-cube blockbench modeled block makes ajacent faces of blocks not render properly

![](/img/nonfull-block-render-error.png)

minecraft's rendering system culls block faces it thinks are hidden. you need to tell it your block is not a full cube by calling `RenderTypeLookup.setRenderLayer(BlockInit.YOUR_BLOCK.get(), RenderType.cutout())` on the `FMLClientSetupEvent`

## any error with the phrase "not valid resource location"

ResourceLocations cannot have spaces or capital letters

## how to make a spawn egg for custom entity (forge deferred registers)

since items are registered before entities, you should make your own verison of the `SpawnEggItem` class and override `getType` in such a way that you don't have to call .get() on your registry object before its registered

## how do i make a pickaxe that destroys 3x3 area

steal the logic from this https://github.com/Ellpeck/ActuallyAdditions/blob/main/src/main/java/de/ellpeck/actuallyadditions/common/items/ItemDrill.java (its MIT licensed) and port it to your MC version / mod loader

## how can i fix NullPointerException that is produced when summoning my entity

make sure you bind a renderer in the `ClientSetupEvent` and bind attributes (max health specificlly) on the `EntityAttributeCreationEvent` (like `event.put(EntityInit.YOUR_ENTITY.get(), attributes)`)

## how do i make an autosmelt pickaxe (or other conditional modification of lots of loot tables at once)

use global loot modifers! they run whenever minecraft gets items out of a loot table

- docs: https://mcforge.readthedocs.io/en/1.17.x/items/globallootmodifiers/
- example: https://github.com/LukeGrahamLandry/inclusive-enchanting-mod/blob/main/src/main/java/io/github/lukegrahamlandry/inclusiveenchanting/events/SmeltingLootModifier.java

## why doesnt the tick method on my block fire

problem is that the `tick` method on blocks is for random ticks (https://minecraft.fandom.com/wiki/Tick#Random_tick) so its not called every tick. You also need to call `randomTicks()` on your `Block.Properties` to make it react to random ticks at all. To do something every tick you could have a tile entity (ive got a tutorial for that). if you just want a timer to do something a while after you place your block, it might be better to schedule a tick. if you do `world.getBlockTicks().scheduleTick(pos, this, delay)` in your `onPlace` method, it should call `tick` after `<delay>` ticks.

## how do i make my item use the honey bottle gulping animation? 

the HoneyBottleItem has a method that specifies the animation to play while its being used

```
@Override
public UseAnim getUseAnimation(ItemStack pStack) {
    return UseAnim.DRINK;
}
```

and then theres a big switch statement that checks for that and renders it differently in ItemInHandRenderer#renderArmWithItem

## how do i change the slipperiness of every block?

You could use a mixin to change the return value of `Block#getSlipperiness` (there are two versions of that method with different parameters, should do both). Here's a good explanation of mixins: https://darkhax.net/2020/07/mixins  

Alternatively, you could also use an access transformer to make `Block#slipperiness` public and then loop through every block and change the value after the blocks have been registered (ie. on `FMLCommonSetupEvent`)

## how to do i make custom armor models (1.17+)

- model class should extend HumanoidModel and have all the parts that should move with the player named correctly (same as 1.16 so probably already done).
- make sure you're registering the model layer definition on the EntityRenderersEvent.RegisterLayerDefinitions event. (example: https://github.com/LukeGrahamLandry/AmbientAdditions/blob/forge-1.18/src/main/java/coda/ambientadditions/client/ClientEvents.java#L158)
- on your custom item class that extends ArmorItem, you override the initializeClient method and add a IItemRenderProperties instance that has a getArmorModel method that returns an insteance of your custom  model class. here's an example: https://github.com/LukeGrahamLandry/AmbientAdditions/blob/forge-1.18/src/main/java/coda/ambientadditions/common/items/YetiArmWarmersItem.java#L46-L58 

## my FMLClientSetupEvent isnt firing

- make sure the method is static
- make sure the method has the `@SubscribeEvent` annotation
- make sure the class has the `@Mod.EventBusSubscriber(modid = ModMain.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)`. You must use `Bus.Mod`, NOT `Bus.FORGE`

## how do i make key bindings?

- Create a keybind `public static final KeyMapping OPEN = new KeyMapping("key.your_action_name", GLFW.GLFW_KEY_M, "key.categories." + ModMain.MOD_ID);` somewhere
- Call `ClientRegistry.registerKeyBinding(YOUR_KEY);` on `FMLClientSetupEvent` 
- checking `YOUR_KEY.isDown()` or `YOUR_KEY.consumeClick()` on `KeyInputEvent` should work. You'll have to send a packet if you want to react to it on the server side

## What is the int parameter on `Level#setBlock`

the third parameter is a flag about which block updates it should send. flags can be OR-ed (passing in `2 | 4` will have the effect of both)

- 1 will cause a block update
- 2 will send the change to clients
- 4 will prevent the block from being re-rendered
- 8 will force any re-renders to run on the main thread instead 
- 16 will prevent neighbor reactions (e.g. fences connecting, observers pulsing)
- 32 will prevent neighbor reactions from spawning drops
- 64 will signify the block is being moved

i think the fourth parameter is how many more layers of recursive block updates to allow. you can just use the version of the method that doesnt need this fourth parameter and just sets it to a reasonable default (512)

## how do I make a mob say something in the chat when it is killed?

There's an `LivingEntity#onDeath` method to override (make sure you still call the super of it) and then you can loop through `world.getPlayers()` and call `player.sendStatusMessage(new TextComponent("hello world"), false)` 

## how do i make an entity that has multiple textures?

whatever resource location is returned by the `getEntityTexture` method in your renderer will be used as the texture. but theres only ever one instance of the renderer so you cant do the random in its constructor. you have to have the entity know which texture it should have, check that from the `getEntityTexture` method and return the appropriate `ResourceLocation`. Note that you'll want to save which texture it chose in its nbt data (override `addAdditionalSaveData` and `readAdditionalSaveData`) as well as use a `EntityDataAccessor` (previously called `DataParameter`) to sync the chosen texture from the server to the client (forge docs: https://mcforge.readthedocs.io/en/1.18.x/networking/entities/#data-parameters). You can look at vanilla's `Cat` code for an example. 

## does the order that deferred registers are used in the mod's constructor matter?

nope, the whole point is that forge magically does it at the right time for you. 

## how to make an item appear with blue letters under the name like a potion
 
look at the `PotionItem#appendHoverText` which calls `PotionUtils#addPotionTooltip`. Example: `pTooltips.add((new TranslatableComponent("potion.whenDrank")).withStyle(ChatFormatting.DARK_PURPLE));`

## how do i have different behaviour for specific players? 

Each minecraft account has a Universally Unique Identifier. There are websites to get these from a player's username (like https://mcuuid.net). Have a list of people's uuids (ie. `List<UUID> coolPeople = List.of(new UUID[]{UUID.fromString("bcb2252d-70de-4abc-9932-bc46bd5dc62f")});`) and then have an if statement that checks `coolPeople.contains(player.getUUID())`. You could even put that list on pastebin or equivilent and fetch it with an http request so you could update it without changing your mod's code. 

## how to make an http request

its just part of the normal jdk libraries

```
public static String get(String url) {
    try {
        HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
        InputStream responseStream = connection.getInputStream();

        return new BufferedReader(
                new InputStreamReader(responseStream, StandardCharsets.UTF_8))
                .lines()
                .collect(Collectors.joining("\n"));
    } catch (IOException e) {
        e.printStackTrace();
    }
    return null;
}
```

## how to change the enchantment glint colour 

its not easy. here's an overview of i did for 1.18.2, 

I was hoping this would be defined as a hex value in the code but it's actually a texture: minecraft:textures/misc/enchanted_item_glint.png.
This texture is at ItemRenderer.ENCHANT_GLINT_LOCATION but that variable is not actually referenced
at render time so changing it back and forth wouldnt work. Instead, the texture is used as a
RenderStateShard.TextureStateShard to create a RenderType. (the specific one i care about changing
in this case is ARMOR_ENTITY_GLINT). I use a mixin to HumanoidArmorLayer that runs before and after
renderArmorPiece is called. This allows me to access the actual item stack and then react to it in
another mixin to a method that wouldn't have that context available. Then I mixin to ItemRenderer#getArmorFoilBuffer
to change the render type that is used to create the vertex consumer to be rendered.

here's the code, dont forget the mixins and access transformers, https://github.com/LukeGrahamLandry/herobrine-thing/blob/main/src/main/java/ca/lukegrahamlandry/herobrinething/client/WhiteArmorGlintHelper.java 