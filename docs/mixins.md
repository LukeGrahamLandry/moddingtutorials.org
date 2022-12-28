# Mixins

**this tutorial is incomplete, check out the following resources instead,**

 - [The official mixin docs](https://github.com/SpongePowered/Mixin/wiki)
 - [Mixin Introduction by Darkhax](https://darkhax.net/2020/07/mixins)
 - [Fabric Wiki - tutorial:mixin](https://fabricmc.net/wiki/tutorial:mixin_introduction)

Mixins are a system for directly changing vanilla code. You can inject your own code into vanilla methods to change behaviour for which Forge does not yet have an event. At runtime, your mixins directly modify the bytecode of the classes you target before they are loaded. Although mixins are more versatile than events, they can be a bit tricky to get right and are generally worse for mod compatibility. You should almost always prefer using the Forge event when one exists. 

## build.gradle

There are a few changes that must be made to your build.gradle to let it know to load your mixins. 

## mixins.json

You will define which classes to load as mixins in a special json file. This file will go in your  

## Mixin Class

Create a new package called `mixins` and create a class called 




### Mixin Method


Note that dispite the fact that the target method has a return type, your mixin method returns void. The extra parameter (`CallbackInfo` or `CallbackInfoReturnable`) allows us to effect the return value of the target method. 

### Method Descriptors 

Use the [Minecraft Development Intellij Plugin](https://plugins.jetbrains.com/plugin/8327-minecraft-development) to generate.

#### Remapping

The method name in your descriptor is automatically remapped according to your project's mappings settings. This allows you to use the readable method names instead of the SRG names (ie. `addMix` instead of `func_193357_a`). This means there's an extra step if you are trying to mixin to a method that is not obfuscated and subsequently renamed by the mappings (anything outside of a vanilla class, for example something added by forge or another mod). You must set `remap` to false in your inject annotation. 

    @Inject(method = "...", at = @At(...), remap = true)
    private void injected(...) {
        // whatever code
    }

### Injection Point 

HEAD
RETURN

### Return a Value

If you want to change the return value of the target method (or just cancel the rest of the method call), you must set `cancellable` to true in your mixin method annotation. 

The last perameter of your mixin method will be of the type `CallbackInfoReturnable<T>` with `T` being the type returned by the target method. You can call `setReturnValue(value);` to change the return value of the target method. Note that this does not immediately exit your method the way a `return;` statement would.


    @Inject(method = "...", at = @At(...), cancellable = true)
    private void injected(CallbackInfoReturnable<Float> callback) {
        callback.setReturnValue(3.14F);
    }

### Accessing The Object

#### Shadowing

When you need to access methods or fields on the target class from your mixin code, you can use the `@Shadow` annotation. Create a null field or an empty method that just throws an error. The `@Shadow` annotation will redirect these references to the ones on your target class. 

#### Using `this`

You may want to directly access the object you are mixing into. You may be frustraited to discover that when you use the `this` keyword, it is an instance of your mixin class, not of the target class. You can get around this by casting to `Object` and then to your target class. This often serves the same purpose as shadowing. 

For example, in a method that targets the ItemEntity class, you could use the following code to get the actual object and then any public methods/fields will be available. 

```
ItemEntity item = (ItemEntity) (Object) this; 
```

> Also note that the mixin class is not actually present at runtime. Its bytecode is just added to vanilla's. You should not have static fields on the mixin class that you try to reference from other places in your mod's code. However, the code in your mixin methods can access the rest of your mod's classes.  


## Other Documentation  

The mixin system used by forge is called [SpongeMixin](https://github.com/SpongePowered/Mixin) and is developed by [Mumfrey](https://github.com/Mumfrey). It is also used by Fabric and Sponge so almost any documentation on mixins for those platforms will also apply to Forge. 

If you want to read more about how to use mixins, check out the following: 

 - [The official mixin docs](https://github.com/SpongePowered/Mixin/wiki)
 - [Mixin Introduction by Darkhax](https://darkhax.net/2020/07/mixins)
 - [Fabric Wiki - tutorial:mixin](https://fabricmc.net/wiki/tutorial:mixin_introduction)