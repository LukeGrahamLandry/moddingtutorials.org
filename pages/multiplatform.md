# How to Develop a Multiplatform Minecraft Mod (Forge & Fabric)

Just Do Everything Twice
- waste of time

Multi SourceSet Workspaces
- common code can access minecraft classes and load mixins
- if you need to use a loader specific api, it must be in its specific package. platform code can access common code. there are different tricks for referencing platform code from common code abstractly 

MultiLoader Template
- service loaders for platform specific implementations

Archetectury (no api)
- magic annotations for platform specific implementations

Archetectury API
- also provides an api for frequent tasks. the general idea of this is similar to the fabric api but its structure is different and it provides implementations for forge and fabric
- technically you don't have to use their gradle setup to use their library

ForgedFabric
- reimplements the fabric api
- easiest way to port fabric mods to forge
- instead of reinventing the wheel for the millionth time by coming up with a new api specification, just write an implementations of the most popular one
- work in progress. support added as i need it for commissions 
