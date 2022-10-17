# How to develop a multiplatform Minecraft mod (Forge & Fabric)

Just Do Everything Twice
- waste of time

Multi SourceSet Workspaces
- common code can access minecraft classs and load mixins
- if you need to use a loader specific api, it must be in its specific package. platform code can access common code. there are different tricks for refernecing platform code from common code abstractly 

MultiLoader Template
- service loaders for platform specific implimentations

Archetectury (no api)
- magic annotations for platform specific implimentations

Archetectury API
- also provides an api for frequent tasks. the general idea of this is similar to the fabric api but its structure is different and it provides implimentations for forge and fabric
- technicly you don't have to use thier gradle setup to use thier library

ForgedFabric
- reimpliments the fabric api
- easiest way to port fabric mods to forge
- instead of reinventing the wheel for the millionth time by coming up with a new api specification, just write an implimentation of the most popular one



