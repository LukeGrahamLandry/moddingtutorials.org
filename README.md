# Modding Tutorials Website

Code for my Minecraft modding tutorial website. View the tutorials online at [moddingtutorials.org](https://moddingtutorials.org). New tutorials are made for 1.19.3, 1.19.2, 1.18.2, and 1.16.5. The code for the tutorial mod is in another repo: [LukeGrahamLandry/modding-tutorials](https://github.com/LukeGrahamLandry/modding-tutorials). Goals of the project are to provide a reference for when I forget things and have good enough SEO that I can get new clients without MMD.

- docs: markdown files built by docusaurus 
- static: files served as is
- src: docusaurus components (the 404 page)

## Build

- run `npm run build` 
- serve the `build` directory
- relies on Cloudflare Pages to use the `_redirects` files

## Scripts 

- fetch.py
    - Downloads my mod readme files (at `/docs/mods`) and parts of the WrapperLib wiki (at `/docs/wrapperlib`). 
    - These are not committed in this repo so the script must be run once before the docusaurus build.
- redirects.py
    - generates additions to the `_redirects` file (used by cloudflare) to convert from old site paths so external links from before docusaurus migration still work 
