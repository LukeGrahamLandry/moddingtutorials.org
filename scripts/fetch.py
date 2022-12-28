import requests

wrapperlib = "docs/wrapperlib"
mod_docs = "docs/mods"
static = "static"

files = {
    wrapperlib + "/installation.md": "https://raw.githubusercontent.com/wiki/LukeGrahamLandry/WrapperLib/Installation.md",
    wrapperlib + "/serialization.md": "https://raw.githubusercontent.com/wiki/LukeGrahamLandry/WrapperLib/Serialization.md",
    wrapperlib + "/networking.md": "https://raw.githubusercontent.com/wiki/LukeGrahamLandry/WrapperLib/Network-Usage.md",
    wrapperlib + "/config.md": "https://raw.githubusercontent.com/wiki/LukeGrahamLandry/WrapperLib/Config-Usage.md",
    wrapperlib + "/keybinds.md": "https://raw.githubusercontent.com/wiki/LukeGrahamLandry/WrapperLib/Keybinds.md",
    wrapperlib + "/saved-data.md": "https://raw.githubusercontent.com/wiki/LukeGrahamLandry/WrapperLib/Saved-Data-Usage.md",
    wrapperlib + "/resources.md": "https://raw.githubusercontent.com/wiki/LukeGrahamLandry/WrapperLib/Resources.md",

    mod_docs + "/torcherino.md": "https://raw.githubusercontent.com/LukeGrahamLandry/Torcherino/1.19/README.md",
    mod_docs + "/tiered-shulkers.md": "https://raw.githubusercontent.com/LukeGrahamLandry/tieredshulkers/1.19/README.md",
    mod_docs + "/entity-rain.md": "https://raw.githubusercontent.com/LukeGrahamLandry/smells-fishy-mod/main/README.md",
    mod_docs + "/find-my-friends.md": "https://raw.githubusercontent.com/LukeGrahamLandry/find-my-friends-mod/forge-1.19/README.md",
    mod_docs + "/inclusive-enchanting.md": "https://raw.githubusercontent.com/LukeGrahamLandry/inclusive-enchanting-mod/forge-1.19/README.md",
    mod_docs + "/tribes.md": "https://raw.githubusercontent.com/LukeGrahamLandry/tribes-mod/forge-1.16.5/README.md",
    mod_docs + "/simple-xp-config.md": "https://raw.githubusercontent.com/LukeGrahamLandry/XpSpawnerControl/1.18/README.md",
    mod_docs + "/travel-staff.md": "https://raw.githubusercontent.com/LukeGrahamLandry/travel_anchors/1.19.x/README.md",
    mod_docs + "/harder-core.md": "https://raw.githubusercontent.com/LukeGrahamLandry/harder-core-mod/main/README.md",
    mod_docs + "/mercenaries.md": "https://raw.githubusercontent.com/LukeGrahamLandry/mercenaries-mod/1.19.2/README.md",
    mod_docs + "/mountables.md": "https://raw.githubusercontent.com/LukeGrahamLandry/mountables-mod/main/README.md",

    static + "/applesilicon.gradle": "https://raw.githubusercontent.com/LukeGrahamLandry/TheMcUtil/main/applesilicon.gradle",
    static + "/multihitboxlib.js": "https://raw.githubusercontent.com/LukeGrahamLandry/TheMcUtil/main/multihitboxlib.js",
    static + "/publish.gradle": "https://raw.githubusercontent.com/LukeGrahamLandry/TheMcUtil/main/publish.gradle",
    static + "/cfstats.js": "https://raw.githubusercontent.com/LukeGrahamLandry/TheMcUtil/main/cf-data-export/cfstats.js"
}

for path, url in files.items():
    with open(path, "w") as f:
        print("Downloading... " + url)
        f.write(requests.get(url).text)
