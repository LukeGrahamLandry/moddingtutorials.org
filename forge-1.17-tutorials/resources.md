# Additional Resources

There are some useful concepts that i havent had time to write tutorials for yet but are reasonably well documented online already. This page has a collection of resources that will prove helpful. These may be less detailed than my tutorials and thus require a strong understanding of Java. 

## Packets

Packets allow you to send information over the network between server code and client code. 

- https://mcforge.readthedocs.io/en/1.17.x/networking/simpleimpl/

## Key Bindings

You can add new key bindings that players can rebind in the vanilla menu and react when they are pressed. You can only read the key on the client side so you will probably have to send a packet back to the server. 

- https://forge.gemwire.uk/wiki/Key_Bindings/1.17

## Global Loot Modifers

Global loot modifiers allow you to run code when items are dropped from loot tables to change the drops for lots of things at once without having to manually edit a bunch of json files. 

- https://mcforge.readthedocs.io/en/1.17.x/items/globallootmodifiers/

## Block Entity Renderer

Some blocks (like chests or beacons) that have complex rendering or animations will have specialized rendering code instead of simple model json files. 

- https://mcforge.readthedocs.io/en/1.17.x/blockentities/ber/

A very similar system can be used to render complex items as well 

- https://mcforge.readthedocs.io/en/1.17.x/rendering/bewlr/

## Item Property Overrides

Allows you to pass information to your model json file when rendering an item. Bows use this for the drawing back animation. 

- https://mcforge.readthedocs.io/en/1.17.x/models/itemproperties/
- https://forge.gemwire.uk/wiki/Item_Properties/1.17

## Tinting Textures

If you want many variations of a block or item texture that just changes the colours, you can apply tints from code. Vanilla uses this for spawn eggs, leather armor, leaves, etc. 

- https://mcforge.readthedocs.io/en/1.17.x/models/color/
- https://forge.gemwire.uk/wiki/Tinted_Textures/1.17

## Capabilities

Capabilities allow attaching data to lots of different entities, tile entities or item stacks while allowing easy compatability between them. They're basiclly an over complicated version of Java's Interfaces designed to make mod compatability easier. Forge gives you a few for storing items, fluids and RF but you can make your own as well. 

- https://forge.gemwire.uk/wiki/Capabilities/1.17 
- https://mcforge.readthedocs.io/en/1.17.x/datastorage/capabilities/

## World Saved Data

World saved data allows you to save nbt data on a specific world that you can read back later. 

- https://mcforge.readthedocs.io/en/1.17.x/datastorage/saveddata/

## Particles 

Particles are an easy way for you to render a 2d sprite at a specific location in the world. 

- https://mcforge.readthedocs.io/en/1.17.x/effects/particles/

## Sounds

Make your mod more exciting by adding noise!

- https://mcforge.readthedocs.io/en/1.17.x/effects/sounds/

## Potions 

- https://forge.gemwire.uk/wiki/Effects/1.17
- https://forge.gemwire.uk/wiki/Potions/1.17 

## Commands

To create a command you'll have to listen to the `RegisterCommandsEvent` and call `event.getDispatcher().register(LiteralArgumentBuilder)`

- https://gist.github.com/sciwhiz12/8b258d493c764d2cf009e121bdc654d3

## Access Transformers

Access transformers allow you to make vanilla code `public` and removing the `final` modifier. Generally try to avoid using this and do things through the proper api instead but sometimes there's no other way. 

- https://mcforge.readthedocs.io/en/1.17.x/advanced/accesstransformers/

## Mixins

Mixins allow you to directly modify vanilla's bytecode. Generally try to avoid using this and do things through the proper api instead but sometimes there's no other way. Since mixin is a seperate library, it doesnt change much with minecraft versions so old tutorials (or even ones for fabric) are still useful. 

- http://darkhax.net/2020/07/mixins
- https://github.com/SpongePowered/Mixin/wiki/Mixins-on-Minecraft-Forge

## Dependencies

You can add integration with other mods and have them as a required or optional dependency. If a mod doesnt provide an api for what you are trying to do, note that it is possible to mixin to another mod's code (tho thats dangerous as modded code will likey change frequently). 

- https://forge.gemwire.uk/wiki/Dependencies/1.17