// this file is part of MultiHitboxLib under the MIT License 

(function() {
    let generateHitboxDataAction = new Action({
        id: 'generatemultihitboxdata',
        name: 'Generate MultiHitbox Data',
        icon: 'flip_to_back',
        description: 'Generate jsons for MultiHitboxLib to define entity part positioning for complex modded entities',
        category: 'file',
        condition: () => true,
        click: function (event) {
            generateHitboxDataJson();
        }
    });
    
    let GROUP_NAME = "MultiHitbox";
    
    function generateHitboxDataJson(){
        let hitboxGroup = Group.all.filter(check => check.name == GROUP_NAME)[0];
        if (hitboxGroup === undefined){
            Blockbench.showMessageBox({
                buttons: ["ok"],
                confirm: 0,
                title: "Error Generating MultiHitbox Data",
                message: "You must create a group called " + GROUP_NAME
            })
            return;
        }

    
        let output = encode(hitboxGroup);
        if (output.errors.length > 0){
            let msg = "Failed with " + output.errors.length + " errors.";
            output.errors.forEach(element => {
                msg += " (" + element + ")";
            });
            Blockbench.showMessageBox({
                buttons: ["ok"],
                confirm: 0,
                title: "Error Generating MultiHitbox Data",
                message: msg
            })
        } else {
            Blockbench.export({
                extensions: ['json'],
                name: 'multihitboxdata',
                content: JSON.stringify(output.result),
            })
            Blockbench.showQuickMessage('Successfully Generated MultiHitbox Data', 1000);
        }    
    }

    function encode(group){
        let result = [];
        let errors = [];

        group.children.forEach(child => {
            if(child instanceof Group){
                let inner = encode(child);
                result.concat(inner.result);
                errors.concat(inner.errors);
                
            } else {
                let xWidth = Math.abs(child.to[0] - child.from[0]);
                let zWidth = Math.abs(child.to[2] - child.from[2]);
                let isSquare = xWidth == zWidth;
                if (!isSquare){
                    errors.push(child.name + " needs square base, <xWidth=" + xWidth + ", zWidth=" + zWidth + ">");
                }

                let isRotated = child.rotation[0] != 0 || child.rotation[1] != 0 || child.rotation[2] != 0;
                if (isRotated){
                    errors.push(child.name + " may not be rotated, <xRot=" + child.rotation[0] + ", yRot=" + child.rotation[1] + ", zRot="+ child.rotation[2] +">");
                }

                result.push({
                    name: child.name,
                    pos: child.from,
                    width: xWidth,
                    height: Math.abs(child.to[1] - child.from[1])
                });
            }
        });

        return {
            result: result,
            errors: errors
        };
    }
    
    Plugin.register('multihitboxlib', {
        title: 'MultiHiboxLib',
        author: 'nulll',
        icon: 'fa-cubes',
        description: 'Generate jsons for MultiHitboxLib to define entity part positioning for complex modded entities',
        tags: ["Minecraft: Java Edition"],
        version: '1.0.0',
        variant: 'desktop',
    
        onload() {
            MenuBar.addAction(generateHitboxDataAction, 'file.export');
        },
        onunload() {
            generateHitboxDataAction.delete();
        }
    });
    
    })();