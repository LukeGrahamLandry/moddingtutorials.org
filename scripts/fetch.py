import requests, os
from datetime import datetime

wrapperlib = "docs/wrapperlib"
mod_docs = "docs/mods"
static = "static"

my_files = {
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

third_party_gists = {
    "50ap5ud5": {
        "updating-1.16-to-1.17": ["Creative Commons", "https://gist.githubusercontent.com/50ap5ud5/beebcf056cbdd3c922cc8993689428f4/raw/d606c626dd58b0cc2a93a9cc048f739927459fe0/1.16.5%2520to%25201.17%2520Minecraft%2520Modding%2520Primer.md"],
        "updating-1.15-to-1.16": ["Creative Commons", "https://gist.githubusercontent.com/50ap5ud5/f4e70f0e8faeddcfde6b4b1df70f83b8/raw/ff86e2b652fd880ece457dd5228ed563bd439357/1.15.2%2520to%25201.16.5%2520Migration%2520Primer.md"],
    }, 
    "ChampionAsh5357": {
        "updating-1.17-to-1.18": ["Creative Commons Attribution 4.0 International", "https://gist.githubusercontent.com/ChampionAsh5357/73c3bb41d3a8de2d020827e0069314a7/raw/cab8251d590acf8d6b2867567c9b38f7523be54c/117-118-primer.md"],
        "updating-1.19.2-to-1.19.3": ["Creative Commons Attribution 4.0 International", "https://gist.githubusercontent.com/ChampionAsh5357/c21724bafbc630da2ed8899fe0c1d226/raw/a12ba2773225e7231785a839ab7e676fe7833644/1192-1193-primer.md"],
        "updating-1.18-to-1.19.2": ["Creative Commons Attribution 4.0 International", "https://gist.githubusercontent.com/ChampionAsh5357/ef542d1ae4e1a5d096f7f8b51f5e0637/raw/c14876fc6d7304d3616b64860b908ebab2740d72/118-119-primer.md"]
    }, 
    "Darkhax": {
        "mixin-introduction": ['<a href="https://github.com/Darkhax/darkhax-dot-net/blob/gh-pages/LICENSE">Creative Commons Attribution 4.0 International</a>', "https://raw.githubusercontent.com/Darkhax/darkhax-dot-net/gh-pages/_posts/tutorials/2020-7-31-mixins.md"]
    }, 
    "misode": {
        "adding-structures-1.18-1.19": ['<a href="https://github.com/misode/misode.github.io/blob/master/LICENSE">MIT, Copyright (c) 2020 Misode</a>', "https://raw.githubusercontent.com/misode/misode.github.io/master/src/guides/adding-custom-structures.md"]
    }, 
    "williewillus": {
        "updating-1.12-to-1.14": ["CC0", "https://gist.githubusercontent.com/williewillus/353c872bcf1a6ace9921189f6100d09a/raw/ba45cc90ff25278b803c9ba9dc262de3802d0abd/primer.md"]
    }
}

sources = {
    "Darkhaxmixin-introduction": "https://darkhax.net/2020/07/mixins",
    "misodeadding-structures-1.18-1.19": "https://misode.github.io/guides/adding-custom-structures"
}

for path, url in my_files.items():
    with open(path, "w") as f:
        print("Downloading... " + url)
        f.write(requests.get(url).text)

# third party files will be fetched on my computer and committed to git. 
# this lets me look at any changes before publishing them.
# make sure there are no naughty script tags, etc.
is_dev_env = os.getcwd().startswith("/Users/luke/")
if is_dev_env:
    for author, entries in third_party_gists.items():
        if not os.path.exists("docs/mirror/" + author):
            os.makedirs("docs/mirror/" + author)

        for filename, (license, url) in entries.items():
            with open("docs/mirror/{}/{}.md".format(author, filename), "w") as f:
                print("Downloading... " + url)
                if "gist" in url:
                    main_url = "https://gist.github.com/{0}/{1}".format(author, url.split("/")[4])
                else:
                    main_url = sources[author + filename]

                text = requests.get(url).text
                if text.startswith("---"):
                    text = "---".join(text.split("---")[2:])
                text = """
<head>
    <link rel="canonical" href="{0}" />
</head>

<pre>
Source: <a href="{0}">{0}</a> <br></br>
License: {1} <br></br>
Retrieved: {2}
</pre> \n
"""             \
                .format(main_url, license, datetime.today().strftime('%Y-%m-%d')) \
                + text.replace("<a>", "</a>").replace("<Capability>", "`<Capability>`").replace("<Biome>", "`<Biome>`").replace("<mappings channel>", "`<mappings channel>`").replace("<Type>", "`<Type>`")

                f.write(text)
