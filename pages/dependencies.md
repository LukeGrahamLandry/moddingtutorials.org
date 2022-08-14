## Adding Dependencies to build.gradle

Sometimes you'll want gradle to load other libraries or mods so you can access their code.  

### Dependencies Block

```
dependencies {
    <function> <descriptor>
}
```

The function tells gradle when it should load the dependency.

- **Use `implementation` to compile against the dependency and have the mod present when you run the game from your development environment. This is probably what you want most of the time.**
- If you want a mod present when you run the game from your development environment but do not want to compile against its code, use `runtimeOnly`. Useful if you just want other mods present in game without referencing their code. For example, JEI to see recipes or an RF generator mod for testing. 
- If you want to compile against the dependency but don't want it present when you run the game from your development environment, use `compileOnly`. When you do this you must be careful about when the dependency is class loaded so it doesnt crash without it. Useful for optional dependencies when you want to test that your mod works without them present. 

The descriptor tells it what dependency to load. But you must define urls to repositories where it can download the files for the dependencies you declare. 

Wrapping the descriptor string in the `fg.deobf` function will tell forge to deobfuscate that jar which lets you use compiled mods in your development environment. 

### Repository Sources

#### Project Repo

Many mods specifically intended to be libraries used by other developers will provide their own public maven repository for you to use. Make sure to read the specific project's documentation (curseforge description, github readme, wiki, etc) and see how they recommend depending on them. For example, Geckolib has an [installation wiki page](https://github.com/bernie-g/geckolib/wiki/Installation) that shows how to reference their cloudsmith maven repository. If the project you want to depend on doesn't provide something just use one of the options below that will work regardless. 

#### Curseforge

If you want to get a mod directly from curseforge you can use [cursemaven.com](https://www.cursemaven.com). 

```
repositories {
    maven {
        url "https://cursemaven.com"
    }
}

dependencies {
    implementation fg.deobf('curse.maven:Descriptor-ProjectID>:FileID')
}
```

- The Descriptor can be any string you want. It's just there to help you tell which dependency is which. Making it the modid of the mod you're depending on is probably a good plan.
- The Project ID can be found on the About Project section of the project
- To get a File ID, go to the download page of file you want to use, and the file ID will be in the URL.

Here's an example that adds Repurposed Structures: https://github.com/LukeGrahamLandry/mercenaries-mod/blob/main/build.gradle#L150-L152

#### Github

If you want to get a mod from directly from github you can use [jitpack.io](https://jitpack.io). It will be a bit slow the first time because they have to checkout and build the project before they can serve it to you. You can go to [their website](https://jitpack.io) and trigger a build of the correct version of your repository ahead of time so its ready when you need it. Note that the main artifact built will be the normal mod jar so you must tell ForgeGradle to deobfuscate it for use in your development environment. 

```
repositories {
    maven { url 'https://jitpack.io' }
}

dependencies {
    implementation fg.deobf('com.github.UserName:RepoName:Version')
}
```

The version should be the tag name of a github release. If the repository doesn't have any releases published, you can use the short commit hash (which you can find on the commits page) instead of the version. You can also use `branchname-SNAPSHOT` to get the latest version. 

#### Your Computer

If you want to temporarily depend on a jar file without dealing with finding a maven repo to host it, you can load it directly from your computer's file system. This has a big disadvantage in that anyone who wants to work with your mod's code has to go find the right jar files and put them in the right places. If you want to help others contribute to your project, go with one of the other maven repository sources above. 

```
repositories {
    flatDir {
        dirs '/path/to/libs/folder'
    }
}

dependencies {
    implementation fg.deobf('tld.packagedomain.mod:Name:Version')
}
```

The descriptor above will first search for `/path/to/libs/folder/Name-Version.jar` and then if that isn't found  `/path/to/libs/folder/Name.jar`.

> If you use `Name-Version` instead of `Name:Version`, it will still find the same jar file but the fg.deobf function will crash because it tries to name the remapped artifact based on the version which it only gets by splitting the artifact descriptor on `:`

## mods.toml

You should add an entry to the bottom of your mods.toml file. This will give users a more meaningful crash message when they try to start the game without the required mod. Base it off the format of the `minecraft` and `forge` dependencies in the default mods.toml from the mdk. 

- You can depend on a specific version range of the mod
- You can mark the dependency as optional so it doesn't crash without it
- You can mark which side the dependency applies on (SERVER or CLIENT or BOTH)
- You can say whether the dependency mod should be loaded before or after your mod. 

## Shading

Shading a dependency allows you to bundle it into your mod's built jar file so players don't need to install it separately.


On fabric you could just use the `include` function but old versions of forge make it way more work. Forge 1.19 and later alleges to natively support the JarJar library for including other mod jars within yours so you can take a look at [the Jar-In-Jar forge community wiki page](https://forge.gemwire.uk/wiki/Jar-in-Jar) instead (**ONLY FOR 1.19+**). This should even work for jars that forge needs to load as mods. For older versions, read on!

Shading has a few disadvantages:

- extra effort to setup
- makes your jar file larger
- players my end up with multiple copies of the same library if its used by multiple mods (doesn't actually break anything just feels wasteful)
- prevents library authors from getting income from curse points if players don't have to severalty download their mod
- challenging to get right since shaded jars are not loaded as mods. It's intended for java libraries whose code you need to access rather than other mods that need to access forge events or mixins (which should be downloaded separately).

Example doing it for Geckolib:

- geo wiki: https://github.com/bernie-g/geckolib/wiki/Shadowing
- shade docs: https://imperceptiblethoughts.com/shadow/introduction/
- geo example: https://gist.github.com/AzureDoom/3f0df105ac480c058a486879ebc86520

## Mixins

Mixin is a powerful framework that allows you to directly modify Minecraft's byte code at runtime. You can use mixins to modify the byte code of other mods, just like you would vanilla Minecraft. It's not very safe to do this however since mods are likely to change drastically between versions with no warning. This means that although your mixin works fine for the version of your dependency you test with, if the mods updates to add a new feature, the method you target may disappear or the code within may change enough that whatever you're doing no longer works properly. It will probably be lots of effort to keep your mixins functional over an extended period of time. A more future proof option may be to find your dependency on github and make a pull request that adds an API that makes whatever you're doing easy. 

My [mixins tutorial](mixins) is incomplete. See other resources:

 - [The official mixin docs](https://github.com/SpongePowered/Mixin/wiki)
 - [Mixin Introduction by Darkhax](https://darkhax.net/2020/07/mixins)
 - [Fabric Wiki - tutorial:mixin](https://fabricmc.net/wiki/tutorial:mixin_introduction)


Remember that your inject annotation must have `remap=false` when targeting methods added by other mods (or forge itself). This is because mixin automatically tries to remap everything according to your project's mappings settings but will get confused because the other mod won't have a remapped name since it was never obfuscated. 

### Mixin Plugins

- mixin plugin that stops it from attempting to apply the mixin if the targeted mod isn't present
- api: https://github.com/SpongePowered/Mixin/blob/master/src/main/java/org/spongepowered/asm/mixin/extensibility/IMixinConfigPlugin.java
- example: https://github.com/Tfarcenim/CuriousJetpacks/blob/1.16.x/src/main/java/tfar/curiousjetpacks/MixinPlugin.java (with `plugin": "tfar.curiousjetpacks.MixinPlugin"` in mixins json)

### Fixing Error With Other Mod's Mixins

Mixin can get a bit confused when you depend on a mod that needs to add its own mixins but uses different [mappings](http://blog.minecraftforge.net/personal/sciwhiz12/what-are-mappings/) than you do. To fix this, in your build.gradle, add the following to your `client` and `server` definitions within the `run` block.

```
property 'mixin.env.remapRefMap', 'true'
property 'mixin.env.refMapRemappingFile', "${projectDir}/build/createSrgToMcp/output.srg"
```

## Final Thoughts

Please don't be one of those people that makes a bullshit library mod just to farm ad income on curse forge. It's so fucking annoying. It makes it that much more of a pain in the ass for other people to work with your mod's code (they have to setup two projects to actually be able to change anything). It's also a waste of time for players that don't use the curse forge launcher since they have to go install the library as well. This extra time adds up if every mod author makes the genius discovery that you earn a couple extra cents if you split up all your mods into several. Take a look at [serilum's mods](https://www.curseforge.com/members/serilum/projects), I'll give you a hint, despite having almost a hundred projects, they only have one mod there. The majority of the functionality is in the library and they use many tiny mods to enable features instead of just having a fucking config like a sane person.

## Credits

Some of this info is adapted from the following sources: 

- https://forge.gemwire.uk/wiki/Dependencies
- https://www.cursemaven.com
- https://jitpack.io 
