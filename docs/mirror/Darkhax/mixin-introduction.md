
<head>
    <link rel="canonical" href="https://darkhax.net/2020/07/mixins" />
</head>

<pre>
Source: <a href="https://darkhax.net/2020/07/mixins">https://darkhax.net/2020/07/mixins</a> <br></br>
License: <a href="https://github.com/Darkhax/darkhax-dot-net/blob/gh-pages/LICENSE">Creative Commons Attribution 4.0 International</a> <br></br>
Retrieved: 2022-12-28
</pre> 



Mixin is a framework for modifying Java bytecode. Through Mixin you will be able to modify the code of Minecraft, Forge, and even other mods. While Mixin can be very useful it is often best to treat it as a last resort or as a temporary solution. If your change would be useful to more than one mod it should probably be a Forge PR instead. It is also important to keep in mind that using Mixin on someone else's mod can be very offensive and is also prone to regular breaking changes.

This tutorial is meant to be a basic introduction to using Mixin in a Forge environment. For in depth information about Mixin refer to the Mixin Javadocs and the [official documentation](https://github.com/SpongePowered/Mixin/wiki).

In this tutorial we will cover
- Setting up your project to use Mixin.
- Modifying Minecraft code.
- Mixin tips, best practices, and limitations.

## Mixin Setup

Mixin requires a bit of setup and configuration before you can use it. The first bit of setup is adding the MixinGradle plugin to your Gradle build script. This is done by defining the plugin as a classpath dependency in the `buildscript` section of your `build.gradle` file. This plugin is not available by default so you will also need to add their maven repo.

```groovy
buildscript {
    repositories {
        maven { url = 'https://maven.minecraftforge.net/' }
        maven { url = 'https://repo.spongepowered.org/repository/maven-public/' }
    }
    dependencies {
        classpath group: 'net.minecraftforge.gradle', name: 'ForgeGradle', version: '5.1.+', changing: true
        classpath group: 'org.spongepowered', name: 'mixingradle', version: '0.7-SNAPSHOT'
    }
}

apply plugin: 'net.minecraftforge.gradle'
apply plugin: 'org.spongepowered.mixin'
```

Now that the plugin is applied to your build script you can configure the plugin. This involves setting up the generation of a a refmap which is used by Mixin to map your changes to different Minecraft environments and telling MixinGradle the name of your Mixin config file. For the refmap, you just need to define the source set to generate mappings for and the name of the file to output to. It is common practice to use `modid.refmap.json`. For the Mixin config file, it is common to use `modid.mixins.json`.

```groovy
mixin {
    add sourceSets.main, "modid.refmap.json"

    config "modid.mixins.json"
}
```

The next step is to create a Mixin config file. This file is used by Mixin to locate your changes and also to define various environmental settings. This file is commonly named `modid.mixins.json` and is placed in the base of your mod's resources folder. The structure of this file is fairly self explanatory. The main thing to note is that the package refers to the base package for where your mixins will be. This package will have certain protections applied so it is often essential to separate it from the rest of your code. This is commonly done by using mixin as a subpackage name.

```json
{
	"required": true,
	"package": "your.package.name.mixin",
	"compatibilityLevel": "JAVA_8",
	"refmap": "modid.refmap.json",
	"mixins": [
	],
	"client": [
	],
	"minVersion": "0.8"
}
```

Depending on your Minecraft version, you will need to change the `compatibilityLevel` accordingly. For 1.16 and lower, use `JAVA_8`. For 1.17, use `JAVA_16`. For 1.18 and higher, use `JAVA_17`.

Finally, you must regenerate your run configurations using `genIntellijRuns` or `genEcliipseRuns` depending on your IDE to allow MixinGradle to configure them.

## ForgeGradle 4+ & Annotation Processors
If you're using ForgeGradle 4 or newer, you will need to add Mixin as an annotation processor. This is a mandatory step as this is required to build a refmap file for your mixin args, allowing them to work outside of your development environment. This is done by making a simple addition to your dependencies block.

```groovy
dependencies {

    annotationProcessor 'org.spongepowered:mixin:0.8.5:processor'
}
```

If you followed these steps properly your mod should now be set up to use mixins. For examples of working mods you can check out [Open Loader](https://github.com/Darkhax-Minecraft/Open-Loader/tree/1.16.1) and [Extra Tags](https://github.com/Tfarcenim/ExtraTags/tree/1.16.x)

## Modifying Code with Mixin

The main benefit of Mixin is that it allows you to write simple changes that look and feel like normal code. In this example our goal will be to change ItemEntity to make all dropped items with the Fire Protection enchantment immune to fire and lava damage. The first step is to create a new class in your mixin package. On top of the normal class declaration you define an `@Mixin` annotation and pass the target class as the value.

```java
@Mixin(ItemEntity.class)
public class MixinItemEntity {
}
```

Once you have created the class go back to your `modid.mixin.json` file and add the class name to the mixins array.

```json
{
	"required": true,
	"package": "your.package.name.mixin",
	"compatibilityLevel": "JAVA_8",
	"refmap": "modid.refmap.json",
	"mixins": [
		"MixinItemEntity"
	],
	"client": [
	],
	"minVersion": "0.8"
}
```

The next step is to identify the code you want to change. In this case I am changing `attackEntityFrom(DamageSource source, float amount)` in ItemEntity. Once you know your target you will recreate the method in your Mixin class. The new method should be modified to be private and to remove the return type if any. Mixin requires these changes for safety and simplicity reasons. You will also need to add a CallbackInfo as the last parameter, or a CallbackInfoReturnable`<Type>` if the method had a return type. This new parameter acts as a surrogate for the traditional return of the method.

```java
@Mixin(ItemEntity.class)
public class MixinItemEntity {
	private void attackEntityFrom(DamageSource source, float amount, CallbackInfoReturnable<Boolean> callback) {
	}
}
```

We now need to add one of the Mixin annotations to this method. While there are several options available the `@Inject` annotation is primarily used. This will allow you to inject your code at various parts of the target method's execution. This annotation has two required values.
- **at** - This defines where to inject our code. We will be using `HEAD` however there are many other options such as `RETURN` which happens before the final return statement.
- **method** - This defines the JVM signature of the method we want to change. If you use IDEA the [Minecraft Development Plugin](https://plugins.jetbrains.com/plugin/8327-minecraft-development) provides a quick way to copy the mixin target. Otherwise you will have to write it by hand or copy it from compiled code.
- **cancellable** - This is only required if you intend to exit the method early or change the return result of the method. In our case we need this as we change the return value to false when we want to prevent the item from being destroyed.
- **remap** - This is only required if you're editing a value which shouldn't be remapped, like a method in Forge or another mod.

```java
@Inject(at = @At("HEAD"), method = "attackEntityFrom(Lnet/minecraft/util/DamageSource;F)Z", cancellable = true)
private void attackEntityFrom(DamageSource source, float amount, CallbackInfoReturnable<Boolean> callback) {
  callback.setReturnValue(false);
}
```

If you run the game now you will see that items can not be destroyed by any damage source. We want to only prevent destruction if the damage source is fire and the item has Fire Protection. We already have the source as a method parameter, but how can we get the ItemStack? This is where shadows come into play. A shadow is a placeholder field or method which is replaced by the real thing at runtime. To create a shadow you simply recreate the field or method in your Mixin class and apply the `@Shadow` annotation. You can then use this method within your Mixin.

```java
@Inject(at = @At("HEAD"), method = "attackEntityFrom(Lnet/minecraft/util/DamageSource;F)Z", cancellable = true)
private void attackEntityFrom(DamageSource source, float amount, CallbackInfoReturnable<Boolean> callback) {
  if (source.isFireDamage() && EnchantmentHelper.getEnchantmentLevel(Enchantments.FIRE_PROTECTION, this.getItem()) > 0) {
    callback.setReturnValue(false);
  }
}

@Shadow
public ItemStack getItem() {
  throw new IllegalStateException("Mixin failed to shadow getItem()");
}
```

## Tips, Best Practices, limitations

**What is the overwrite annotation, is it safe to use?**
The overwrite annotation will completely replace the target code with your version of the method. This can be a very powerful feature however compatibility issues will come up if you decide to use it. I prefer to use Inject and then return early instead of overwriting although in some cases you may want the compatibility errors if the mods are truly incompatible.

**Can I modify a constructor?**
Modifying the constructor is not supported. In some situations there are some hacks you can use to do this however it is generally not a good idea to do so.

**How do I write the method descriptor?**
Method descriptors are similar to java declaration however there are a few key changes. The descriptor uses the format of `name(params)returntype`. 

|  Character  | Description                                                                                              |
|:-----------:|----------------------------------------------------------------------------------------------------------|
|      B      | A byte.                                                                                                  |
|      C      | A char.                                                                                                  |
|      D      | A double.                                                                                                |
|      F      | A float.                                                                                                 |
|      I      | An int.                                                                                                  |
|      J      | A long.                                                                                                  |
|      S      | A short.                                                                                                 |
|      Z      | A boolean.                                                                                               |
| LClassName; | A typed object. Must include the package name. Lnet/minecraft/util/DamageSource;                         |
|    [Type    | An array of a given type. [B is a byte array [Lnet/minecraft/util/DamageSource; is a  DamageSource array |
