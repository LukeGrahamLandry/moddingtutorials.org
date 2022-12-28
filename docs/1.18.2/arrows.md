---
sidebar_position: 10
---

# Custom Projectile 

Your projectile is an example of an entity. Entities have a position in the world, are bound to a renderer so the player can see them, have a bounding box to detect collisions, and react to ticks (move around, etc). Each individual entity in the world is an instance of the `Entity` class. There are many classes that extend `Entity` to give more interesting behavior. 

Each entity also has an `EntityType`. This must be registered just like blocks/items. The `EntityType` tells the game which renderer to use and which `Entity` class to use to define your entity's behavior when it is loaded from disk. 

## Init

Start by setting up a deferred register for entities. 

```java
public class EntityInit {
    public static DeferredRegister<EntityType<?>> ENTITY_TYPES = DeferredRegister.create(ForgeRegistries.ENTITIES, FirstModMain.MOD_ID);
}
```

Then you will use it to register an `EntityType` for your custom arrow. As usual, you pass in a string to use as a registry name and a supplier for your entity type. Entity types are created with the `EntityType.Builder` class. This allows you to set a few traits of your entity. 

The builder needs a supplier for your entity class. If you're entity class has multiple constructors, it seems to get confused which you mean so you have to cast it to `EntityType.EntityFactory`. You also give it a `MobCategory` (better description of this will be in the hostile entities tutorial), for projectiles you should use `MISC`. The `sized` method sets the width and height of the bounding box, so how big an area your projectile checks for hitting something (vanilla arrows use 0.5 by 0.5). Finally call the `build` method, the argument here should be the same as the registry used earlier name (idk why but that's what vanilla does. if anyone finds out, pls tell me). 

```java
public static final RegistryObject<EntityType<ExplosiveArrowEntity>> EXPLOSIVE_ARROW = ENTITY_TYPES.register("explosive_arrow",
            () -> EntityType.Builder.of((EntityType.EntityFactory<ExplosiveArrowEntity>) ExplosiveArrowEntity::new, MobCategory.MISC).sized(0.5F, 0.5F).build("explosive_arrow"));
```

Remember to call this registry from the constructor of your main class.

```java
EntityInit.ENTITY_TYPES.register(modEventBus);
```

## Arrow Class

Now we will actually create the class referenced above to define the behavior of the projectile. There's a kinda elaborate tree of classes with different behaviors already implemented, you can read the descriptions below to choose which to extend for your arrow. Each class has its own behavior and keeps the behavior of anything lower down the chain. 

### Vanilla Classes

Entity

- does the absolute minimum, you must define all behavior

Projectile > Entity

- saves its owner 
- has methods for shooting: sets its movement direction 
- has methods for what happens for reacting to impacts
- does **not** have logic for moving or detecting collisions, *you must write this yourself or extend something lower down*. 

AbstractArrow > Projectile > Entity

- movement and collision detection logic in the tick method
- rotates to face direction of movement
- piercing logic (`setPierceLevel`, used by crossbows)
- deals damage on hit based on velocity and `setBaseDamage`
- sticks in the ground and can be picked up
- able to be shot from normal bows by using the ArrowItem class

Arrow > AbstractArrow > Projectile > Entity

- logic for holding potion effects (apply on hit, make particles)

ThrowableProjectile > Projectile > Entity

- movement and collision detection logic in the tick method

ThrowableItemProjectile > ThrowableProjectile > Projectile > Entity

- renders as an item by implementing `ItemSupplier` and registering an entity type with to `ThrownItemRenderer`

### Your Class

I will be extending `AbstractArrow`. Below are the constructors that give you. The `getPickupItem` method returns the item stack to give the player when they walk over your arrow stuck in the ground.

```java
public class ExplosiveArrowEntity extends AbstractArrow {
    public ExplosiveArrowEntity(EntityType<ExplosiveArrowEntity> entityType, Level world) {
        super(entityType, world);
    }

    public ExplosiveArrowEntity(EntityType<ExplosiveArrowEntity> entityType, double x, double y, double z, Level world) {
        super(entityType, x, y, z, world);
    }

    public ExplosiveArrowEntity(EntityType<ExplosiveArrowEntity> entityType, LivingEntity shooter, Level world) {
        super(entityType, shooter, world);
    }

    @Override
    protected ItemStack getPickupItem() {
        return ItemStack.EMPTY;
    }
}
```

To do something when we hit an entity, call the `onHitEntity`. If you want it to do damage normally and respect piercing levels, keep the call to the super method. 

```java
@Override
protected void onHitEntity(EntityRayTraceResult ray) {
    super.onHitEntity(ray);
}
```

To access the entity you hit, use `ray.getEntity()`. I want to create an explosion but still respect piercing so I'll keep the super call. Note that because of invincibility time, if you keep the super call and do extra damage here only the greater of vanilla's damage and your damage will apply (you can change vanilla's damage by with `this.setBaseDamage(amount);`)

```java
@Override
protected void onHitEntity(EntityHitResult ray) {
    super.onHitEntity(ray);
    // this, x, y, z, explosionStrength, setsFires, breakMode
    this.level.explode(this, this.getX(), this.getY(), this.getZ(), 4.0f, true, Explosion.BlockInteraction.BREAK);
}
```

To do something when you hit a block, you can override the following method. Keeping the super call will cause the arrow to stick in the block you hit to be picked up or despawn after 60 seconds. 

```java
@Override
protected void onHitBlock(BlockHitResult ray) {
    super.onHitBlock(ray);
    BlockState theBlockYouHit = this.level.getBlockState(ray.getBlockPos());
}
```

I'm going to leave that method as it is in vanilla and override the `tickDespawn` method (called every tick while its in the ground) to make an explode after 3 seconds. 

```java
@Override
protected void tickDespawn() {
    if (this.inGroundTime > 60){
        this.level.explode(this, this.getX(), this.getY(), this.getZ(), 4.0f, true, Explosion.BlockInteraction.BREAK);
        this.discard();
    }
}
```

## Rendering

To allow players to see your arrow in the world, you must bind it to an `EntityRenderer` that defines its appearance. 

Before we do this, you **must** add this method to your entity class. If you do not do this, the arrow will behave normally and give no helpful error message but it will not render. This simply returns a packet to sync the entity from the server side to the client side and is called automatically whenever the arrow is added to the world. 

```java
// in ExplosiveArrowEntity.java
@Override
public Packet<?> getAddEntityPacket() {
    return NetworkHooks.getEntitySpawningPacket(this);
}
```

Next, create a renderer class for your arrow (create the `client.render` package). I will copy the vanilla `TippedArrowRenderer` and just change a few values. Since I'm extending the `ArrowRenderer` class it will have the same shape as vanilla arrows. The `getTextureLocation` method just returns a resource location to use as the texture for the entity. The path used for the resource location is just the file path to your image in your `src/main/resources/mod_id/assets` directory. 

```java
public class ExplosiveArrowRenderer extends ArrowRenderer<ExplosiveArrowEntity> {
    public static final ResourceLocation TEXTURE = new ResourceLocation(FirstModMain.MOD_ID, "textures/entity/explosive_arrow.png");

    public ExplosiveArrowRenderer(EntityRendererProvider.Context manager) {
        super(manager);
    }

    public ResourceLocation getTextureLocation(ExplosiveArrowEntity arrow) {
        return TEXTURE;
    }
}
```

We will need to make the texture image for our arrow. I will use an [online pixel art editor](https://www.piskelapp.com/p/create/sprite) to recolor the vanilla arrow texture. Textures are a net of all the faces of the 3d object in the game unfolded onto a flat image. You can find all the vanilla assets on github at [InventivetalentDev/minecraft-assets](https://github.com/InventivetalentDev/minecraft-assets). This is what the vanilla arrow texture looks like:

![vanilla arrow texture](/img/arrow_texture.png)

Once you're happy with your texture image, you can make a folder called `entity` in `src/main/resources/mod_id/assets/textures` and put your image file in it. Make sure to name the file the same as used in the texture resource location (for me that's `explosive_arrow.png`). 

You can also have multiple textures and switch between them based on properties of the projectile object passed to `getTextureLocation`. For example, you could check the value of `arrow.tickCount` and cycle between different textures every second. Note that you can only access values present on the client side so you may need to use a `DataParameter` to sync data from the server. This will be covered in more detail in the entities tutorial. Join [the discord server](/discord) to be notified when it is released. 

### Bind Renderer

For the game to know that your new renderer class should be used whenever your arrow exists in the world, you must register it on the client setup event. The forge events system is described in more depth in [the events tutorial](/events).

Start by making a new class called `ClientSetup` in your `client` package with a method listening for the `FMLClientSetupEvent`. Note the `value = Dist.CLIENT` in the annotation on the class because the event only fires on the client side. In this method, we use the `EntityRenderers.register` method to register our renderer. It just needs the entity type reference to the constructor of your renderer class. 

```java
@Mod.EventBusSubscriber(modid = FirstModMain.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ClientSetup {
    @SubscribeEvent
    public static void doSetup(FMLClientSetupEvent event) {
        EntityRenderers.register(EntityInit.EXPLOSIVE_ARROW.get(), ExplosiveArrowRenderer::new);
    }
}
```

## Using Your Arrow

You can add your arrow to the world whenever you want. The next section of this tutorial will cover creating a custom arrow item so vanilla bows can shoot your projectile. You could also create a custom bow (by extending `BowItem`) that specificity shoots the projectile we just made. A tutorial for this is coming soon. Join [the discord server](/discord) to be notified when it is released. 

Example of summoning your arrow entity that could be used anywhere you have access to a player (ie, on item right click):

```java
if (!player.level.isClientSide()){
    ExplosiveArrowEntity arrow = new ExplosiveArrowEntity(EntityInit.EXPLOSIVE_ARROW.get(), player, player.level);
    arrow.setDeltaMovement(0, 1, 0); // directly up
    player.level.addFreshEntity(arrow);
}
```

## Arrow Item

Arrows are just an item like any other with a special method that allows bows to create the correct arrow entity to shoot. Create a class that extends `ArrowItem` and simply override the `createArrow` method to return a new instance of the arrow entity you created above. 

```java
public class ExplosiveArrowItem extends ArrowItem {
    public ExplosiveArrowItem(Properties props) {
        super(props);
    }

    @Override
    public AbstractArrow createArrow(Level world, ItemStack ammoStack, LivingEntity shooter) {
        return new ExplosiveArrowEntity(EntityInit.EXPLOSIVE_ARROW.get(), shooter, world);
    }
}
```

Then register an item for your arrow like normal. 

```java
// in ItemInit.java
public static final RegistryObject<Item> EXPLOSIVE_ARROW = ITEMS.register("explosive_arrow",
            () -> new ExplosiveArrowItem(new Item.Properties().tab(ModCreativeTab.instance)));
```

Remember to go back to your arrow class and tell it to give your item when picked up off the ground. 

```java
// in ExplosiveArrowEntity.java
@Override
protected ItemStack getPickupItem() {
    return new ItemStack(ItemInit.EXPLOSIVE_ARROW.get());
}
```

### Tag

To allow vanilla bows and crossbows to shoot your arrow, it must be in the `arrows` item tag. Tags are a data driven system for categorizing registered objects with similar behavior.

Create the folders `src/main/resources/data/minecraft/tags/items` and within that folder create a file called `arrows.json`. This is a json object that defines the changes you want to make to the tag specified by the file name. The `replace` key being false makes it add to vanilla's arrow list instead of replacing it. The `values` list contains the resource locations of the items you want to add to the arrows category (so a bow can shoot them). 

```json
{
    "replace": false,
    "values": [
        "firstmod:explosive_arrow"
    ]
}
```

### Assets

The arrow item requires model and texture files as well as a lang entry as covered in the [basic items tutorial](basic-items)

