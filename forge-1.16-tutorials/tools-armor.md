# Tools and Armor

In this tutorial we make a simple set of tools and armor. We also make an armor piece that reacts to ticks and being attacked.

## Tools

Tools are simply items that use special classes instead of the basic `Item`.

### Material

Start by defining the base stats for your tier of tools. The mining level (0 is wood, 4 is netherite), durability, mining speed, damage, [enchantability](https://minecraft.fandom.com/wiki/Enchanting_mechanics#How_enchantments_are_chosen), and an `Ingredient` which defines which items may be used to repair your tools in an anvil.

You must do this in a class that implements `IItemTier`. The simplest way to do this is to just copy vanilla's `ItemTier` enum and just redefine the tiers. Put this class in your `util` package. You can change the values used to initialize your tier to suit your liking and make multiple by separating them with commas. 

    public enum ModItemTier implements IItemTier {
        PINK(3, 3000, 10.0F, 5.0F, 5, () -> {
            return Ingredient.of(ItemInit.SMILE.get());
        }),
        EXAMPLE(1, 1, 1.0F, 1.0F, 1, () -> {
            return Ingredient.of(Items.STICK);
        });
    
        private final int level;
        private final int uses;
        private final float speed;
        private final float damage;
        private final int enchantmentValue;
        private final LazyValue<Ingredient> repairIngredient;
    
        ModItemTier(int level, int durability, float miningSpeed, float damage, int enchantability, Supplier<Ingredient> repairIngredient) {
            this.level = level;
            this.uses = durability;
            this.speed = miningSpeed;
            this.damage = damage;
            this.enchantmentValue = enchantability;
            this.repairIngredient = new LazyValue<>(repairIngredient);
        }
    
        public int getUses() {
            return this.uses;
        }
    
        public float getSpeed() {
            return this.speed;
        }
    
        public float getAttackDamageBonus() {
            return this.damage;
        }
    
        public int getLevel() {
            return this.level;
        }
    
        public int getEnchantmentValue() {
            return this.enchantmentValue;
        }
    
        public Ingredient getRepairIngredient() {
            return this.repairIngredient.get();
        }
    }

### Init

Now you have to register your tools in `ItemInit` just like any other item. Each type of tool has its own class (`SwordItem`, `PickaxeItem`, etc). The item constructor takes a reference to the `IItemTier` you defined earlier, a damage value to add to the base damage from the tier, an attack speed value which is added to a default of 4 to get the final speed of the item's swings (so should probably be negative, -2 is faster than -1) and finally an `Item.Properties` just like your other items. 

    public static final RegistryObject<Item> PINK_SWORD = ITEMS.register("pink_sword",
                () -> new SwordItem(ModItemTier.PINK, 3, -2.4F, new Item.Properties().tab(ModCreativeTab.instance)));
    
        public static final RegistryObject<Item> PINK_PICKAXE = ITEMS.register("pink_pickaxe",
                () -> new PickaxeItem(ModItemTier.PINK,1, -1.0F, new Item.Properties().tab(ModCreativeTab.instance)));
    
        public static final RegistryObject<Item> PINK_AXE = ITEMS.register("pink_axe",
                () -> new AxeItem(ModItemTier.PINK, 6, -3.4F, new Item.Properties().tab(ModCreativeTab.instance)));
    
        public static final RegistryObject<Item> PINK_SHOVEL = ITEMS.register("pink_shovel",
                () -> new ShovelItem(ModItemTier.PINK, 1, -1.0F, new Item.Properties().tab(ModCreativeTab.instance)));
    
        public static final RegistryObject<Item> PINK_HOE = ITEMS.register("pink_hoe",
                () -> new HoeItem(ModItemTier.PINK, 0, -1.0F, new Item.Properties().tab(ModCreativeTab.instance)));


### Advanced Tools

Since they are simply items, you can make your own classes that extend the basic tool classes to give them unique behaviour. You can use the same methods discussed in the [advanced items tutorial](/advanced-items). Here are some methods that might be interesting:

- `mineBlock`: called when the player breaks a block with the item. You should make sure to call the super method to reduce durability.
- `isCorrectToolForDrops`
- `getDestroySpeed` (big numbers are faster)
- `hurtEnemy`

### Assets

The assets are the same as any other item (model, texture, lang) except that the model parent should be `item/handheld` instead of `item/generated`. This will make it rotate properly in your hand to look like you're holding a tool. 

## Armor

Similar to tools, a piece armor is simply an item that uses `ArmorItem` instead of the basic `Item`. 

### Material

Start by defining the stats for your armor in a class that implements `IArmorMaterial`. 

The `name` string you use **must **start with your mod id, then a colon, then anything. The durability number is multiplied by the numbers in the `HEALTH_PER_SLOT` array to get the durability for each piece. `protection` is an array of the protection values of each piece (in the order boots, leggings, chest plate, helmet). A full armor bar is when those numbers add up to 20. It needs an [enchantability](https://minecraft.fandom.com/wiki/Enchanting_mechanics#How_enchantments_are_chosen) just like tools and a `SoundEvent` to play when you equip the item. I'm just using a vanilla sound but later we'll learn how to add a custom one. Then you need a [toughness](https://minecraft.fandom.com/wiki/Armor#Armor_toughness) which increases how much protection it gives against stronger attacks (only used by diamond and netherite in vanilla). Then knockback resistance (only used by netherite, when all pieces add up to 1 that's no knockback) and finally a supplier for a repair ingredient to use in the anvil.  

    public enum ModArmorMaterial implements IArmorMaterial {
        PINK(FirstModMain.MOD_ID + ":pink", 20, new int[]{4, 7, 9, 4}, 50, SoundEvents.ARMOR_EQUIP_DIAMOND, 3.0F, 0.1F, () -> { 
            return Ingredient.of(ItemInit.SMILE.get()); 
        });
    
        private static final int[] HEALTH_PER_SLOT = new int[]{13, 15, 16, 11};
        private final String name;
        private final int durabilityMultiplier;
        private final int[] slotProtections;
        private final int enchantmentValue;
        private final SoundEvent sound;
        private final float toughness;
        private final float knockbackResistance;
        private final LazyValue<Ingredient> repairIngredient;
    
        ModArmorMaterial(String name, int durability, int[] protection, int enchantability, SoundEvent sound, float toughness, float knockbackResistance, Supplier<Ingredient> repairIngredient) {
            this.name = name;
            this.durabilityMultiplier = durability;
            this.slotProtections = protection;
            this.enchantmentValue = enchantability;
            this.sound = sound;
            this.toughness = toughness;
            this.knockbackResistance = knockbackResistance;
            this.repairIngredient = new LazyValue<>(repairIngredient);
        }
    
        public int getDurabilityForSlot(EquipmentSlotType slot) {
            return HEALTH_PER_SLOT[slot.getIndex()] * this.durabilityMultiplier;
        }
    
        public int getDefenseForSlot(EquipmentSlotType slot) {
            return this.slotProtections[slot.getIndex()];
        }
    
        public int getEnchantmentValue() {
            return this.enchantmentValue;
        }
    
        public SoundEvent getEquipSound() {
            return this.sound;
        }
    
        public Ingredient getRepairIngredient() {
            return this.repairIngredient.get();
        }
    
        @OnlyIn(Dist.CLIENT)
        public String getName() {
            return this.name;
        }
    
        public float getToughness() {
            return this.toughness;
        }
    
        public float getKnockbackResistance() {
            return this.knockbackResistance;
        }
    }

### Init

Register your armor items like normal using the `ArmorItem` class. It needs a reference to your `IArmorMaterial`, and `EquipmentSlotType` (`HEAD`, `CHEST`, `LEGS`, or `FEET`) and an `Item.Properties`. 

    public static final RegistryObject<Item> PINK_HELMET = ITEMS.register("pink_helmet",
                () -> new ArmorItem(ModArmorMaterial.PINK, EquipmentSlotType.HEAD, new Item.Properties().tab(ModCreativeTab.instance)));
    
        public static final RegistryObject<Item> PINK_CHESTPLATE = ITEMS.register("pink_chestplate",
                () -> new ArmorItem(ModArmorMaterial.PINK, EquipmentSlotType.CHEST, new Item.Properties().tab(ModCreativeTab.instance)));
    
        public static final RegistryObject<Item> PINK_LEGGINGS = ITEMS.register("pink_leggings",
                () -> new ArmorItem(ModArmorMaterial.PINK, EquipmentSlotType.LEGS, new Item.Properties().tab(ModCreativeTab.instance)));
    
        public static final RegistryObject<Item> PINK_BOOTS = ITEMS.register("pink_boots",
                () -> new ArmorItem(ModArmorMaterial.PINK, EquipmentSlotType.FEET, new Item.Properties().tab(ModCreativeTab.instance)));

### Assets

In `/src/main/resources/assets/modid/textures` make a new folder called `models` and in that one called `armor`. Here you will put the texture map for your armor. It's sort of a weird format, they look like this: 
![](/img/template_layer_1.png)

![](/img/template_layer_2.png)

Use those exact templates because the positioning is important, they should be 512 by 256 (but it's the 1:2 ratio that matters). The first one must be named `name_layer_1.png` and is for the helmet and chest plate. The second must be named `name_layer_2.png` and is leggings and boots. Of course, replace `name` with the string you used in your armor material (without the `modid:` prefix). So for me it's `pink_layer_1.png` and `pink_layer_2.png`. 

The other assets (model json & lang) are the same as for normal items. 
![](/img/armor.png)

## Advanced Armor

Let's make a fresh piece of armor to experiment with. I'll use the same material as before because I'm lazy but you should make a new one if you want unique stats and appearance. Instead of being a normal `ArmorItem` this will be a new class that extends `ArmorItem`.

    public static final RegistryObject<Item> FLAMING_CHESTPLATE = ITEMS.register("flaming_chestplate",
                () -> new FlamingArmorItem(ModArmorMaterial.PINK, EquipmentSlotType.CHEST, new Item.Properties().tab(ModCreativeTab.instance)));


​    

### Tick

Make a class for your `ArmorItem` and override the `onArmorTick` method. I'll give the wearer 10 seconds of fire resistance (since its done every tick, they'll be immune to fire damage while wearing the armor). It's probably a good idea to make sure you're only doing this on the server side. 

    public class FlamingArmorItem extends ArmorItem {
        public FlamingArmorItem(IArmorMaterial material, EquipmentSlotType slot, Properties properties) {
            super(material, slot, properties);
        }
    
        @Override
        public void onArmorTick(ItemStack stack, World world, PlayerEntity player) {
            if (!world.isClientSide()){
                player.addEffect(new EffectInstance(Effects.FIRE_RESISTANCE, 200));
            }
        }
    }

If you want to only do something while they're wearing the full set, you can add a condition in your tick method that checks that each piece of armor matches what it should be. 

    boolean fullSet = player.getItemBySlot(EquipmentSlotType.HEAD).getItem() == ItemInit.PINK_HELMET.get() && <CHEST> && <LEGS> && <FEET>;
    if (fullSet){
    	// do something cool here
    }

If all the pieces are from your special class keep in mind that this tick method will be called for each piece. You may want to check the `EquipmentSlotType` of the item stack that's passed in (by calling `stack.getEquipmentSlot()`) to avoid repeating behaviour depending what you're doing. 

### On Attacked

The `ArmorItem` class doesn't offer a method to override for this but we can use events instead. Events are a way to let forge know that it should call one of your methods when something specific in the game happens. This system is described in more depth in [the events tutorial](/events).

In your `util` package make an interface called `IDamageHandlingArmor` with a single method called `onDamaged`. This will take the entity being attacked, the armor slot being processed, the damage source (which gives you the type of damage and the attacker if applicable). The default implementation will simply return the same damage amount so nothing will change

    public interface IDamageHandlingArmor {
        default float onDamaged(LivingEntity entity, EquipmentSlotType slot, DamageSource source, float amount){
            return amount;
        }
    }


Start by making a package called `events`. Then make a new class called `ArmorHandlers` with the `EventBusSubscriber` annotation. 

    @Mod.EventBusSubscriber(bus = Mod.EventBusSubscriber.Bus.FORGE)
    public class ArmorHandlers {
    
    }

Then, in that class make a new method that listens for the `LivingDamageEvent`. This is done by making a public, static, void method with the `@SubscribeEvent` annotation. The parameter type defines which event it will listen for. 

This method will get the attacked entity from the event object and loop through each piece of armor it is wearing. For each piece it will check if the item implements our interface and call the `onDamaged` method if it does. It saves the value returned by that method and sets the damage about on the event. This allows our custom armor to directly effect the damage by changing the return value. 

    @SubscribeEvent
     public static void armorAttackHandler(LivingDamageEvent event){
            for (ItemStack armor : event.getEntityLiving().getArmorSlots()){
    			if (armor.getItem() instanceof IDamageHandlingArmor){
                	float newDamage = ((IDamageHandlingArmor)armor.getItem()).onDamaged(event.getEntityLiving(), armor.getEquipmentSlot(), event.getSource(), event.getAmount());
                    event.setAmount(newDamage);
            	}
            }
        }

Then make your `FlamingArmorItem` class implement `IDamageHandlingArmor` and override the `onDamaged` method. 

Mine will get the attacker from the damager source. If the attacker is living (which doubles as a null check), I'll deal half the damage I would have taken as fire damage, set it on fire for 4 seconds, and reduce the amount of damage I take by half. Otherwise, if there was no attacker (like if it was fall damage), I'll just take the  damage I would normally. 

    public class FlamingArmorItem extends ArmorItem implements IDamageHandlingArmor{
    // ...other code here...
    
    	@Override
        public float onDamaged(LivingEntity entity, EquipmentSlotType slot, DamageSource source, float amount) {
            Entity attacker = source.getEntity();
            if (attacker instanceof LivingEntity){
                attacker.hurt(DamageSource.ON_FIRE, amount / 2);
                attacker.setSecondsOnFire(4);
                return amount / 2;
            } else {
                return amount;
            }
        }

Again, note that `onDamaged` is called for each armor piece you you may want to add a check on the slot to avoid reacting to an attack multiple times.

Note that the `LivingDamageEvent` does not fire for every attack, only those that would deal enough damage to get through your armor. If you want to react to all attacks, you can use the `LivingAttackEvent` instead. However this does not allow you to change the amount of damage to be dealt. You can only completely cancel the attack (by calling `event.setCanceled(true);` from your event handler).

### Piglins 

You can override `makesPiglinsNeutral` to return true if you want your armor to act like gold and have piglins ignore the wearer. 

    @Override
    public boolean makesPiglinsNeutral(ItemStack stack, LivingEntity wearer) {
        return true;
    }

### Related Tutorials 

- You can make armor with complex 3d models made in BlockBench. This will be covered in a future tutorial. [Join the discord server](https://discord.gg/VbZVnRd) to be notified when it is released. 
