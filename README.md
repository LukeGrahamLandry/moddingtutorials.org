# Modding Tutorials Website

Code for my Minecraft modding tutorial website. View the tutorials online at [moddingtutorials.org](https://moddingtutorials.org). New tutorials are made for 1.19, 1.18.2, 1.17.1 and 1.16.5. The code for the tutorial mod is in another repo: [LukeGrahamLandry/modding-tutorials](https://github.com/LukeGrahamLandry/modding-tutorials). Goals of the project are to provide a reference for when I forget things and have good enough SEO that I can get new clients without MMD.

## Build

- run `python3 build.py` (PYTHON_VERSION=3.7)
- serve the `dist` directory
- relies on Cloudflare Pages to use the `web/_redirects` files

## Content

Each folder has markdown files that are built into html and inserted into a template from /web/templates. 

- forge-1.xx-tutorials (/oxx)
    - version specific forge modding tutorials
    - tutorials for the most recent version are also hosted at / 
- pages (/oxx)
    - tutorials and explanations that don't change between versions
- mod-documentation (/mods)
    - docs for minecraft mods (features, config options, api, etc)
    - supported front matter tags: description, author, version, source, download, contact
    - additional pages fetched from my mod readme files
- articles (/c)
    - take advantage of my good SEO for low traffic minecraft keywords
    - some are funnels for my paid services 
    - detailed opinions about things that people might google like chat reporting 
- vanilla
    - redstone
        - tutorials for creating redstone contraptions 
    - advancements 
        - requirements for completing the harder in game advancements 

## Metadata (web/pages.json)

- videos
    - list of youtube urls to display on commissions page
- yt-clients 
    - list of youtube channel identifiers to display on clients page
- fetched-pages
    - map of urlPrefix to list of markdown urls to download
- descriptions
    - map of page titles to descriptions to insert in meta tags
- tutorial-videos
    - map of urlPrefix to map of page title to youtube video identifier to inject button to load
