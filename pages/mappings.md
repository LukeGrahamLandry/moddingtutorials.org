coming soon...   
Join [the discord server](/discord) to be notified when it is released. 

## Different Mappings Projects

- MCP
- yarn
- official
- quilt

The names of classes and organization of packages are also obfuscated and remapped. 
In 1.17, forge switched from using the MCP data for this to the official mappings so all the class names changed between these versions. Fabric of course defaults to the Yarn class names but if you choose to use the official mappings, that will apply to the class names as well.  

## Switching Mappings

### Linkie

started as a discord bot, now a website as well 

### Gradle Script

If you need to change the mappings used by your entire project, it would take forever to do manually. Luckily there are gradle scripts that can do this for you. Forge provides the `updateMappings` task to update your method names and `Forge-Class-Remapper` by SizableShrimp can update your class names. How to use both these scripts is covered in [the updating to 1.17 tutorial](/o17/updating).

## Resources
- https://fabricmc.net/wiki/tutorial:mappings
