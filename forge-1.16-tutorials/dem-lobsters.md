# Dem Lobsters Integration 

[Dem Lobsters](https://www.curseforge.com/minecraft/mc-mods/dem-lobsters) is a mod that allows you to breed colourful lobsters 
and use their shells to craft resources instead of mining. It is similar to Mystical Agriculture. 
You can improve your mod by adding compatibility with Dem Lobsters!

## build.gradle

First, allow your development environment to import the needed classes by adding the following to your build.gradle

    repositories {
        maven {
            url "https://www.cursemaven.com"
        }
    }

    dependencies {
        runtimeOnly fg.deobf("curse.maven:lobsters-549438:FILE_ID")
    }

Replace `FILE_ID` with the file id for the latest build released on curseforge. 
You can find this by opening [the Files page](https://www.curseforge.com/minecraft/mc-mods/dem-lobsters/files), 
clicking on the latest release and looking at the number at the end of the url.

## Lobster Type Builder

Create a new class in your `init` (or `compat`) package. Create a `LobsterTypeInit` class. 

Then create a `LobsterTypeBuilder` for each of your resources that should have an assosiated lobster. 
There are many methods on the builder to set traits about your lobster.

TODO

### Register Lobster Types

Finally register all your `LobsterTypeBuilder`s. This should go in a static `init` method in your `LobsterTypeInit` class that will be called from your mod's main class.

```
public static void init(){
    LobsterTypes.register(LobsterTypeBuilder);
    // repeat for each type
}
```

## Assets

### Texture

You will need to make a texture for your lobster. If you choose to use one of the default models included with Dem Lobsters,
your texture will need to be drawn on the same net. You can look at [Dem Lobster's assets on GitHub] to get the default textures and recolor them. 
Make sure to name your texture correctly based on the resource location used in your `LobsterTypeBuilder`.

### Lang

You will need to add a lang entry (generally in `en_us.json`) for `item.lobsters.NAME_spawn_egg`, `item.lobsters.NAME_shell`, and `entity.lobsters.NAME`.

### Data Generation

Dem Lobsters makes it easy to generate the correct recipes for crafting resources from your shells as well as the item models for your spawn eggs and shells. 
Add the following method to your `LobsterTypeInit` class. 

```
public static void generateData(GatherDataEvent event) {
    LobsterDataGenSetup.addLobsterDataGeneration(event, YOUR_MOD_ID_HERE);
}
```

Add the following line to your `LobsterTypeInit.init` method. 
```
FMLJavaModLoadingContext.get().getModEventBus().addListener(LobsterTypeInit::generateData);
```

You must run the `runData` gradle task before building or running your mod.

### Item Models

**Note: this is only required if you do not use the Data Generation code above. These json files should be automaticlly generated.**

You will need to include model files for spawn eggs and shells for each of your lobster types. The items themselves are registered automaticlly
by Dem Lobsters but you must define the textures to use. Create a `lobsters` folder in your `src/main/resources/assets`. Within this folder, create `models/items`.
This is where you will put these model files.

The model for your spawn egg will be in `NAME_spawn_egg.json` (with `NAME` being the value used in your `LobsterTypeBuilder`).
You generally want to use the vanilla spawn egg template. It will automaticlly be coloured based on the `color` value in your `LobsterTypeBuilder`.

    {
      "parent": "minecraft:item/template_spawn_egg"
    }

The model for your shell will be in `NAME_shell.json` (with `NAME` being the value used in your `LobsterTypeBuilder`).
You generally want to use the same texture as the rest of the lobster shells. It will automaticlly be coloured based on the `color` value in your `LobsterTypeBuilder`.

    {
        "parent": "minecraft:item/generated",
        "textures": {
            "layer0": "lobsters:item/shell"
        }
    }

## Making Dem Lobsters an Optional Dependency 

You probably do not want your mod to crash when Dem Lobsters is not installed. 
That means you should check that Dem Lobsters is installed before trying to load any of its classes. 
You can use `ModList.get().isLoaded("lobsters")` to check if a mod is loaded by modid.

In the constructor of your mod's main class, conditionally call your `LobsterTypeInit.init` method (where you register all your `LobsterTypeBuilder`s). 

    if (ModList.get().isLoaded("lobsters")){
        LobsterTypeInit.init();
    }

### mods.toml

Add the following to your mods.toml

    [[dependencies.yourmodid]]
        modId="lobsters"
        mandatory=false
        versionRange="[1.0,)"
        ordering="BEFORE"
        side="BOTH"

If for some strange reason you want to crash when Dem Lobsters is not installed, change the value of `mandatory` to `true`.

### CurseForge

When you upload your mod's jar file to curseforge. Add [Dem Lobsters](https://www.curseforge.com/minecraft/mc-mods/dem-lobsters) as an optional dependency. 