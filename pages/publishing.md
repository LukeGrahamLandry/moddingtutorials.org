# Releasing Your Mod

When your mod is ready for other people to play it, you'll want them be able to add it to their game rather than only running in a development environment. I'll review your options for distribution websites and give a tutorial on using gradle to automatically publish your mod. 

## Build 

To build your mod's code into a jar file that can be loaded by minecraft, you simply run the `build` gradle task. This can be done from intellij or from the command line. 

```
./gradlew build
```

> Make sure you use `cd` to navigate to your mod project folder before running the command.  
> On windows, do not include the `./` at the beginning of the command.  

When the task is finished running, your built jar file will be in the `build/libs` folder.   

To install the mod, just drop that jar file in `minecraft/mods` and launch the game with forge installed. 

## Distribution Platforms 

There are many websites that will let you upload your mods and make it easy for players to install them. If you want to give players the choice of what distribution platform they prefer, nothing's stopping you from uploading your mods to multiple websites. 

### Github

[Github](https://github.com) is a great place to host your mod's code if you want it to be open source. It also has "Github Releases" which lets you upload files and tag them as the release corresponding to a certain commit. 

Github Releases Advantages:

- Don't have to create a new project on a new website if you're already using Github for version control. 

Github Releases Disadvantages:

- Doesn't have special support for minecraft mods. You can upload files but there's no integrated system for marking which minecraft version and mod loader is supported (you can just write it in the description tho). 

### Curseforge

[Curseforge](https://www.curseforge.com) has been the most popular website for hosting Minecraft mods for a long time.  

Curseforge Advantages:

- Include Minecraft specific meta data (version, mod loader, etc) with your uploaded files 
- If your mod gets a lot of downloads you will earn Curse Points which can be redeemed to paypal 
- Lots of modpacks are developed using the Curseforge platform which only makes it easy to include mods from Curseforge. Your mod will probably reach more players if it can be used in popular modpacks.  
- They have a popular launcher that integrates tightly with their mod and modpack platform. 

Curseforge Disadvantages:

- Their frontend is just bad. Page often load slowly and somewhat regularly its just completely down for a few hours.

### Modrinth 

[Modrinth](https://modrinth.com) is an open source alternative to Curseforge.

Modrinth Advantages:

- Include Minecraft specific meta data (version, mod loader, etc) with your uploaded files 
- **Much** faster and prettier website than Curseforge 
- It's nice to support platforms that prevent one company from having a total monopoly on mod distribution. 
- They have their own modpack format that can be imported by ATLauncher, MultiMC, and Prism Launcher.
- Provides an api for downloading mods that isn't crippled by Curseforge's monetization obsession (this makes it easier for third party apps to integrate with them)

Modrinth Disadvantages:

- Less popular than Curseforge, might not provide as much discoverability for your mod. 
- Still under development, some features you might want from their website aren't ready yet (comments, ad revenue sharing, analytics).

## Gradle Plugins

If you end up making several mods, it will eventually get irritating to have to click through the website's interface to upload a file every time you want to release some new content. Especially if you want to give players the choice of what distribution platform to use so you want to upload to multiple websites. If you get to that point, check out the following gradle plugins. With a bit of configuration, they'll give you a gradle task to automatically upload a new release. 

- https://github.com/shedaniel/unified-publishing
- https://github.com/BreadMoirai/github-release-gradle-plugin

## JustEnoughPublishing

JustEnoughPublishing is a gradle script I wrote that uses the plugins above to release your mod based on a simple json configuration file. Personally I dislike copy pasting the plugin boiler plate across all my projects. Instead, I just put a one line script import in my build.gradle file which will set up everything based on a json file containing the project's settings. This script is less versatile than using the plugins directly so use whichever suits your situation best. 

### Usage

1. import the script (bottom of build.gradle): `apply from: "https://moddingtutorials.org/publish.gradle"`
2. create the config file as specified bellow
3. define your api keys as environment variables and make sure you expose the required gradle properties (more info below)
4. run `gradlew publishMod` whenever you want to publish a new version (can be done in a github action, [example](https://github.com/LukeGrahamLandry/ForgedFabric/blob/1.16/.github/workflows/publish.yml))
 
### Config File
 
Location Options

1. {root}/.github/publish.json 
2. {subproject}/publish.json 
3. {root}/publish.json):

The config file contains a json object with the following fields: 

- versions: array of supported minecraft versions. ie ["1.19.3", "1.19.2"]
- loader: "forge" or "fabric"
- changelogUrl: url will be added to description body
- releaseType: (optional) default is "release", could also be "beta" or "alpha"
- github: (optional)
     - repo: the name of the repository to release to
     - owner: the name of the github account that owns repo
     - branch: the name of the branch this release is based on
     - requiredDependencies: (optional) map of display name to url
- curseforge: (optional)
     - id: the id of the project to publish the file (as a string)
     - requiredDependencies: (optional) list of project slugs

[example](https://github.com/LukeGrahamLandry/ForgedFabric/blob/1.16/.github/publish.json)

### gradle.properties variables

- version: the version number of your mod's current release, should match the entry in your mods.toml

### Secrets

These are your api keys and should **not** be committed to your git repository. They can be set in `USER_HOME_FOLDER/.gradle/gradle.properties` or as environment variables. Each is only required if you defined that platform in your publish.json file. 

- CURSEFORGE_API_KEY: https://authors.curseforge.com/account/api-tokens
- GH_API_KEY: personal token with repo permissions https://github.com/settings/tokens

## Forge Version Checker

- https://forge.gemwire.uk/wiki/Version_Checker