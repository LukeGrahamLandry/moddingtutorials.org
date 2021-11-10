# Block Entity

Make a block entity that kills nearby mobs.  

A block entity is a simplified version of an entity that is bound to a specific block the the world. It knows its position, can react to ticks and saves data when the world is reloaded. Some vanilla examples are chests, furnaces and beacons. 

Before 1.17, block entities were referred to as tile entities.

## Init

Start by making a block for your block entity. It will have its own class just like we made for other advanced blocks in the last tutorial. 

    public static final RegistryObject<Block> MOB_SLAYER = BLOCKS.register("mob_slayer",
                () -> new MobSlayerBlock(Block.Properties.copy(Blocks.IRON_BLOCK)));

Then you will need to register your block entity. Make a new class called `TileEntityInit`. We will start by getting a deferred register just like for blocks and items. 

    public class TileEntityInit {
        public static final DeferredRegister<BlockEntityType<?>> TILE_ENTITY_TYPES = DeferredRegister.create(ForgeRegistries.BLOCK_ENTITIES, FirstModMain.MOD_ID);
    }
    
Then register your block entity. The string you pass in is the registry name which can be anything you want (all lower case, no weird characters as usual). Then you need a supplier for a `BlockEntityType` which has a builder to use. The builder takes a supplier to make new instance of your block entity. For this, use a method reference to the constructor of your block entity class (we'll make this class in the next step). Then you need to tell it the types of blocks that your block entity is allowed to be bound to. I'll just have one (the block we made earlier) but you can have multiple, just separate them with commas. Then we call the `build` method of the builder to get the type. 

    public static final RegistryObject<BlockEntityType<MobSlayerTile>> MOB_SLAYER = TILE_ENTITY_TYPES.register("mob_slayer",
                () -> BlockEntityType.Builder.of(MobSlayerTile::new, BlockInit.MOB_SLAYER.get()).build(null));

The null argument passed to the build method is a "data fixer type". Honestly, I have no idea what that means. It seems to not be used for anything and leaving it null has always worked for me. If you happen to know what it does, please let me know, I'm curious. 

Like with the item and block registries, you have to tell minecraft that you're trying to register things. Add this line to the constructor of your main class:

    TileEntityInit.TILE_ENTITY_TYPES.register(modEventBus);

## Block Class

The actual block for your block entity must have a custom class that implements `EntityBlock`. Then, override `newBlockEntity` to return a new instance of your block entity. I'm using the block entity type's `create` method but you could directly call the constructor once you make your block entity class).

    public class MobSlayerBlock extends Block implements EntityBlock {
        public MobSlayerBlock(AbstractBlock.Properties props) {
            super(props);
        }
        
        @Nullable
        @Override
        public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
            return TileEntityInit.MOB_SLAYER.get().create(pos, state);
        }
    }
    

## Tile Class

Now create the block entity class you referenced earlier (make a new `tile` package to keep organized). As you may have guessed, the class will extend `BlockEntity`. Pass your block entity type to the super constructor. 

    public class MobSlayerTile extends BlockEntity {
        public MobSlayerTile(BlockPos pos, BlockState state) {
            super(TileEntityInit.MOB_SLAYER.get(), pos, state);
        }
    }
    

### Tick

#### Setup

To react to ticks, your the block class must override `getTicker`. This will just check that the `BlockEntityType` is the same one we just registered and then return a reference to the `tick` method (which we haven't made yet) of our `MobSlayerTile`.

```
@Nullable
@Override
public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level world, BlockState state, BlockEntityType<T> type) {
    return type == TileEntityInit.MOB_SLAYER.get() ? MobSlayerTile::tick : null;
}
```

The tick method must follow the `BlockEntityTicker` interface. it should look like this:

```
public static <T extends BlockEntity> void tick(Level level, BlockPos pos, BlockState state, T be) {
    MobSlayerTile tile = (MobSlayerTile) be;

    // your code here
}
```

This method will be called each tick (20 times per second).

#### Behaviour 

You can do anything you want here but I want my block entity to kill nearby monsters. I'll start by writing some logic for when to hurt the mobs. 

I'm going to start by making to variables on my `MobSlayerTile` class. I'll need a `timer` field (because I don't want to deal damage every tick, that would be too op) and an `isActive` field (because I want the player to be able to turn it off sometimes). 

```
int timer = 0;
boolean isActive = true;
```

Then in my tick method, I'll check that we're on the server side (because that's where logic like dealing damage should be processed) and that the tile should be active. Then, each tick I'll increment the timer and only if 20 ticks (1 second) has passed since last time, I'll reset the timer and call a `hurtMobs` method (that I haven't defined yet). 
    
    if (!level.isClientSide() && tile.isActive){
        tile.timer++;
        if (tile.timer > 20){
            tile.timer = 0;

            // only do this once per second
            tile.hurtMobs();
        }
    }

I'll start by deciding the top left and bottom right corner of the area I want to target. I'll do this by adding the my chosen range to all the coordinates of the block entity to get the top and subtracting to get the bottom. Then I'll make an `AABB` from these points. This axis aligned bounding box represents a cube centered on my block entity going out `RANGE` blocks in all 3 dimensions. 

Then I'll use the world's `getEntities` method to get all the entities within that area of effect. The first argument is an entity to ignore (arrows use this to not hit themselves) but I want to get everything so I'll leave it null. The second argument is obviously the ``AABB`` to get entities within. Then I'll loop through the list it returns. For each entity, I'll check that it is living (not an arrow, item, etc) and not a player (I don't want my new tile to hurt me!). If it meets my criteria, I'll deal one heart of magic damage. 

    final int RANGE = 5;
    private void hurtMobs() {
        BlockPos topCorner = this.worldPosition.offset(RANGE, RANGE, RANGE);
        BlockPos bottomCorner = this.worldPosition.offset(-RANGE, -RANGE, -RANGE);
        AABB box = new AABB(topCorner, bottomCorner);
    
        List<Entity> entities = this.level.getEntities(null, box);
        for (Entity target : entities){
            if (target instanceof LivingEntity && !(target instanceof Player)){
                target.hurt(DamageSource.MAGIC, 2);
            }
        }
    }

Note: instead of doing that check in the for loop, I could have passed in a `Predicate<Entity>` which would return true only if it was something I want to target. That would probably run faster but not significantly enough to matter and I have a personal preference for how I did it. 

### Processing Block Interactions

I want to be able to toggle my mob slayer on and off by right clicking the block. I'll start by making a function that will preform the toggle. 

    public void toggle(){
        this.isActive = !this.isActive;
    }

Then I need my block to notify my block entity when it is right clicked. I'll override the `use` method as we did in the last tutorial. After checking that I'm on the server side and processing the main hand (so it doesn't get called twice), I'll get the block entity at that position. To be safe, I'll check that it's the right type of block entity but in practice it always will be. I'll cast it to my block entity class and call the `toggle` method. For dramatic effect (and so its easier to tell that our click was processed), I'll make it play a sound as well. 

    @Override
    public InteractionResult use(BlockState state, Level world, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hit) {
        if (!world.isClientSide() && hand == InteractionHand.MAIN_HAND){
            BlockEntity tile = world.getBlockEntity(pos);
            if (tile instanceof MobSlayerTile){
                ((MobSlayerTile) tile).toggle();

                world.playSound(player, player.getX(), player.getY(), player.getZ(), SoundEvents.ANVIL_LAND, SoundSource.PLAYERS, 1.0F, 1.0F);
                return InteractionResult.SUCCESS;
            }
        }

        return super.use(state, world, pos, player, hand, hit);
    }

### NBT Data

Currently, when I save the world and reload it, the `isActive` variable will default back to true. We can override a few methods to save it with the rest of the world's data. 

The format Minecraft uses for most of the data it saves is called NBT ([Named Binary Tag](https://minecraft.fandom.com/wiki/NBT_format)). This is basically a map of keys and values (just like a more limited version of a `HashMap`) that can easily be serialized to a binary representation to store in files. 

In code, the class that is used for this format is `CompoundTag`. There are many types of data you can store in an `CompoundTag`: `boolean`, `int`, `String`, `double`, `float`, `long`, an array of `long`s, `byte`, a `Tag` (like another `CompoundTag` or a `ListTag`). You've got all the primitives and more so with enough effort you can make an nbt representation for any object. The general methods to use are `CompoundTag.putType(key, value)`, `CompoundTag.getType(key)` and `compundNBT.contains(key)`. The key is always a `String` and the value can be any supported type (just change the method name, ie `getString`, etc).

Tile entities use the `save` method to get the data to store as a `CompoundTag` when the world is saved and `load` to read back that nbt into normal variables. I'll use this to simply store my `isActive` field and read it back. Make sure to call the super methods to let Minecraft store the block entity's base data. 

    @Override
    public CompoundTag save(CompoundTag nbt) {
        nbt.putBoolean("active", this.isActive);
        return super.save(nbt);
    }
    
    @Override
    public void load(CompoundTag nbt) {
        super.load(nbt);
        this.isActive = nbt.getBoolean("active");
    }

Note that the nbt keys `id`, `x`, `y`, `z`, `ForgeData`, `ForgeCaps` and the registry name of the block entity type (for me that's `mob_slayer`) are reserved for the default data Minecraft has to store about your block entity. Do not try to use them. 

### Syncing Data

With my block entity, I've been careful to do everything on the server side. If you're doing something more complex, you may have to sync data between the client and the server. There are a few ways to do this. I will cover examples where you need to use these in a later tutorial on doing custom rendering with a block entity. Join [the discord server](https://discord.gg/VbZVnRd) or [the email list](https://buttondown.email/LukeGrahamLandry) to be notified when it is released. 

**On chunk load: **`getUpdateTag()` returns the data that the server wants to send as a `CompoundTag`. `handleUpdateTag(CompoundTag tag)` reads it back on the client side.

**On block update:** gotta use a packet! (but you can use one from vanilla). `getUpdatePacket` is sent from the server, `onDataPacket` is read on the client.

    @Override
    public ClientboundBlockEntityDataPacket getUpdatePacket(){
        CompoundTag nbtTag = new CompoundTag();
        // save data to nbt 
        return new ClientboundBlockEntityDataPacket(this.worldPosition, -1, nbtTag);
    }
    
    @Override
    public void onDataPacket(Connection net, ClientboundBlockEntityDataPacket pkt){
        CompoundTag tag = pkt.getTag();
        // read data
    }

To trigger that you can call `world.notifyBlockUpdate(BlockPos pos, BlockState oldState, BlockState newState, int flags)`

**Custom packet:** a more versatile solution would be to make your own packets that you can send whenever you want (not just for block updates). I will cover packets in a future tutorial. Join [the discord server](https://discord.gg/VbZVnRd) or [the email list](https://buttondown.email/LukeGrahamLandry) to be notified when it is released. 

## Assets

The block to which you bound your block entity is a block like any other. Don't forget to give it a block model, item model, block state definition, loot table and lang entry.

You can also use code to do more complex rendering logic for your block entity. This will be covered in a future tutorial. Join [the discord server](https://discord.gg/VbZVnRd) or [the email list](https://buttondown.email/LukeGrahamLandry) to be notified when it is released. 

## Extension

- Make the mob slayer we made in this tutorial directional. That is, instead of the area of effect being centered on the block, have the block rotateable from like the last tutorial and only attack mobs in the forwards direction.
- Make a block entity that teleports nearby mobs on top of it
    - hint: `entity.setPos(x, y, z);`
