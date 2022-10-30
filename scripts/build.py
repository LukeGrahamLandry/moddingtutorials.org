from email import header
import os
import markdown, json, shutil
from pygments import lexers
from pygments import highlight 
from pygments.formatters import HtmlFormatter
from xml.sax import saxutils as su
import frontmatter

from fetch import FetchedPageCache

lex = lexers.get_lexer_by_name("java")
formatter = HtmlFormatter()
with open("scripts/pages.json", "r") as f:
    site_data = json.loads("".join(f.readlines()))

OUTPUT_DIRECTORY = "dist"

other_fetched_urls = []

"""
    Performs replacements on files passed to processFiles. 

    Arguments: stats from youtube's api by web/scrape-videos.py (input ids are from web/pages.json)
    - paid_videos: [{id, title, views, time, channel}]
    - client_channels: [{id, title, views, subscribers}]

    Replacements:
    - \$VIDEOS is replaced by thumbnails & stats generated from paid_videos
    - \$CHANNELS is replaced by icons & stats generated from client_channels
    - $FETCHED_URLS is replaced by a list of all urls fetched so far during the build (from the FetchedPageCache)
"""
class CommissionsHelper:
    def __init__(self, paid_videos, client_channels):
        self.paid_videos = paid_videos
        self.client_channels = client_channels

    def processFiles(self, *files):
        for filename in files:
            self.processFile(filename)
    
    def processFile(self, filename):
        print("CommissionsHelper processing " + filename)

        with open(OUTPUT_DIRECTORY + "/" + filename, "r") as f:
            content = "".join(f.readlines())

        content = content \
            .replace("\$VIDEOS", self.getVideosHTML()) \
            .replace("\$CHANNELS", self.getChannelsHTML()) \
            .replace("$FETCHED_URLS", "\n".join(urlCache.getCachedUrls()) + "\n" + "\n".join(other_fetched_urls))

        with open(OUTPUT_DIRECTORY + "/" + filename, "w") as f:
            f.write(content)

    def getViews(self, video):
        return int(video["views"])
    
    def formatViewNumber(self, views):
        views = int(views)
        if views >= 1000000000:
            views = str(round(views / 1000000000, 2)) + "B"
        elif views >= 1000000:
            views = str(round(views / 1000000, 1)) + "M"
                
        elif views >= 1000:
            views = str(views // 1000) + "K"
        else:
            views = str(views)
        
        return views

    def getVideosHTML(self):
        self.paid_videos.sort(reverse=True, key=self.getViews)

        video_html = ""

        for video in self.paid_videos:
            video_html += '<a class="video" target="_blank" href="https://www.youtube.com/watch?v=' + video["id"] + '"> \n' 
            video_html += '<img src="/img/videos/' +  video["id"] + '.jpg" alt="video thumbnail"> \n'

            video_html += '<b class="title">' + video["title"][0:45] + "</b> \n"
            video_html += "<b>" + self.formatViewNumber(video["views"]) + ' Views </b> <b class="title"> by ' + video["channel"] + " </b> \n"
            video_html += "</a>\n"
        
        return video_html
    
    def getChannelsHTML(self):
        self.client_channels.sort(reverse=True, key=self.getViews)

        html = '<link rel="stylesheet" href="/styles/channels.css">\n'

        for channel in self.client_channels:
            html += '<span class="channel"> \n' 
            html += '<img src="/img/videos/' +  channel["id"] + '.jpg" alt="video thumbnail"> \n'

            html += '<b class="title">' + channel["title"] + "</b> \n"
            html += '<b class="subs">' + self.formatViewNumber(channel["subscribers"]) + ' Subscribers </b> \n'
            html += '<b class="views">' + self.formatViewNumber(channel["views"]) + ' Views </b> \n'
            html += "</span>\n"
        
        return html


class SiteSection:
    def __init__(self, sourceDir, urlPrefix, templateFile):
        self.sourceDir = sourceDir
        self.urlPrefix = urlPrefix
        self.templateFile = templateFile
        with open("web/templates/" + templateFile, "r") as f:
            self.template_html = "".join(f.readlines())

    def processFiles(self):
        target_output_dir = OUTPUT_DIRECTORY + "/" + self.urlPrefix
        if not os.path.isdir(target_output_dir):
            os.mkdir(target_output_dir)
        
        baseroot = None
        for root, dirs, files in os.walk(self.sourceDir, topdown=True):
            if baseroot is None:
                baseroot = root

            subdirectory = root.replace(baseroot + "/", "").replace(baseroot, "")
            
            for filename in files:
                if ".md" not in filename:
                    continue

                target = filename
                if subdirectory != "":
                    target = subdirectory + "/" + filename
                
                self.processMarkdownFile(baseroot, target)
            
            for dir in dirs:
                self.makeSubfolder(dir)
    
    def makeSubfolder(self, dir):
        os.mkdir(OUTPUT_DIRECTORY + "/" +  self.urlPrefix + "/" + dir)

    def highlightCode(self, html_content):
        code_parts = html_content.split("<code>")
        html_syntax_highlighted = code_parts[0]
        del code_parts[0]

        for part in code_parts:
            code = part.split("</code>")[0]
            code = su.unescape(code)
            end = part.split("</code>")[1]

            styled_code = highlight(code, lex, formatter)
            
            styled_code = styled_code.split('<div class="highlight"><pre>')[1]
            styled_code = styled_code.split('</div>')[0]

            html_syntax_highlighted += '<code class="highlight">'
            html_syntax_highlighted += styled_code
            html_syntax_highlighted += "</code>"
            html_syntax_highlighted += end
        
        return html_syntax_highlighted

    def getCanonicalPath(self, title):
        path = "{}/{}".format(self.urlPrefix, title)
        if self.urlPrefix is None or self.urlPrefix == "":
            path = "{}".format(title)
        return path

    def getDescription(self, title, metadata):
        if "description" in metadata:
            return metadata["description"]

    def getDisplayName(self, title, metadata):
        if "title" in metadata:
            return metadata["title"]
        
        displayName = ""
        for part in title.split("-"):
            displayName += part[0].upper() + part[1:] + " "
        
        return displayName

    def generateMetaTags(self, title, metadata):
        meta = "<title>{}</title> \n".format(self.getDisplayName(title, metadata))
        meta += '<link rel="canonical" href="https://moddingtutorials.org/{}"/> \n'.format(self.getCanonicalPath(title))
        
        description = self.getDescription(title, metadata)
        if description is not None:
            meta += '<meta name="description" content="{}"> \n'.format(description)
        return meta

    def handleReplacements(self, html_content, title, metadata):
        return self.template_html.replace("$CONTENT", html_content).replace("$META", self.generateMetaTags(title, metadata))

    def processMarkdownFile(self, source_folder_path, filename, extraMetadata={}, tab_length=4):
        print("building {}/{} to {}".format(source_folder_path, filename, self.urlPrefix))

        title = ".".join(filename.split(".")[:-1])
        with open(source_folder_path + "/" + filename, "r") as f:
            self.compileMD(title, f.read(), extraMetadata=extraMetadata, tab_length=tab_length)

    def compileMD(self, title, raw_markdown_text, extraMetadata={}, tab_length=4):
        metadata, md_content = frontmatter.parse(raw_markdown_text)
        metadata = {**metadata, **extraMetadata}
        
        html_content = markdown.markdown(md_content, extensions=['fenced_code', "mdx_linkify"], tab_length=tab_length)
        html_content = self.highlightCode(html_content)
        html_content = self.handleReplacements(html_content, title, metadata)

        self.writeFile(title, html_content)
    
    def writeFile(self, title, html_content):
        out_path = "{}/{}.html".format(self.urlPrefix, title)
        if self.urlPrefix is None or self.urlPrefix == "":
            out_path = "{}.html".format(title)
        out_path = OUTPUT_DIRECTORY + "/" + out_path
            
        with open(out_path, "w") as f:
            f.write(html_content)


class TutorialSiteSection(SiteSection):
    defaultNamespace = "o19"

    def __init__(self, sourceDir, urlPrefix, templateFile):
        super().__init__(sourceDir, urlPrefix, templateFile)
    
    def getDescription(self, title, metadata):
        description = super().getDescription(title, metadata)
        if description is not None:
            return description
        
        if title in site_data["descriptions"]:
            return site_data["descriptions"][title]

    def getDisplayName(self, title, metadata):
        displayName = super().getDisplayName(title, metadata)

        displayName += "| Minecraft Modding Tutorials"
        if title == "index":
            displayName = "Minecraft Forge Modding Tutorials"

        return displayName

    def writeFile(self, title, html_content):
        super().writeFile(title, html_content)

        if self.urlPrefix == TutorialSiteSection.defaultNamespace:
            out_path = "{}/{}.html".format(OUTPUT_DIRECTORY, title)
            with open(out_path, "w") as f:
                f.write(html_content)

    def handleReplacements(self, html_content, title, metadata):
        if self.urlPrefix in site_data["tutorial-videos"] and title in site_data["tutorial-videos"][self.urlPrefix]:
            video_id = site_data["tutorial-videos"][self.urlPrefix][title]
            html_content = """
                <div class="alert video-wrapper" onclick="showYoutubeVideo(this, '$VIDEO')">
                    There is a video version of this tutorial. Click here to watch!
                </div>
            """.replace("$VIDEO", video_id) + html_content
        
        return super().handleReplacements(html_content, title, metadata)

    def makeSubfolder(self, dir):
        super().makeSubfolder(dir)

        if self.urlPrefix == TutorialSiteSection.defaultNamespace:
            os.mkdir(OUTPUT_DIRECTORY + "/" + dir)
    
# for pages that are the same between MC versions. sets the canonical tag to the root/title instead of root/version/title so google doesn't punish me for duplicate content
class UnversionedTutorialSiteSection(TutorialSiteSection):
    def getCanonicalPath(self, title):
        return title


# TODO: could change so that FetchedSiteSection also handles a directory with another method for the fetched pages then ModDocsSiteSection FetchedSiteSection > SiteSection
class ModDocsSiteSection(SiteSection):
    def __init__(self, pages, sourceDir, urlPrefix, templateFile):
        super().__init__(sourceDir, urlPrefix, templateFile)
        self.pages = pages
        self.extra_nav_html = self.generateModDocsIndexHtml()
    
    def generateModDocsIndexHtml(self):
        index_html = ""

        # fetched
        for page in self.pages:
            name = page["name"].lower().replace(" ", "-")
            url = "/" + self.urlPrefix + "/" + name
            if page["branch"] == "wiki":
                url = "/" + self.urlPrefix + "/" + page["repo"].split("/")[1] + "/Home"
            index_html += '<a href="{}" class="post">{}</a> \n'.format(url, page["name"])
        
        # index_html += "<hr/> \n"

        # md files
        for root, dirs, files in os.walk(self.sourceDir, topdown=True):
            for filename in files:
                if filename == "index.md" or ".md" not in filename:
                    continue
                
                name = filename.split(".")[0]
                displayName = ""
                for part in name.split("-"):
                    displayName += part[0].upper() + part[1:] + " "

                index_html += '<a href="{}" class="post">{}</a> \n'.format("/" + self.urlPrefix + "/" + name, displayName)

            break

        return index_html

    def handleReplacements(self, html_content, title, metadata):
        header_html = self.getHeaderHtml(title, metadata)
        
        full_content = super().handleReplacements(header_html + html_content, title, metadata)
        full_content = full_content.replace("$LICENSE", self.getLicense(metadata)).replace("$NAV", self.getExtraNavHTML(title, metadata))
        return full_content

    def getHeaderHtml(self, title, metadata):
        header_html = """
            <div style="text-align: center; margin-top: 10px;">
        """
        
        if "version" in metadata:
            header_html += """
                <span style="font-size: 1rem"> version $VERSION </span> <br>
            """.replace("$VERSION", metadata["version"])

        if "download" in metadata:
            header_html += """
                <a class="alert orange sm" style="display: inline-block;" href="$LINK" target="_blank">
                    Download Mod
                </a>
            """.replace("$LINK", metadata["download"])
        
        if "source" in metadata:
            header_html += """
                <a class="alert black sm" style="display: inline-block;" href="$LINK" target="_blank">
                    Source Code
                </a>
            """.replace("$LINK", metadata["source"])

        if "contact" in metadata:
            header_html += """
                <a class="alert blue sm" style="display: inline-block;" href="$LINK" target="_blank">
                    Contact Author
                </a>
            """.replace("$LINK", metadata["contact"])

        if "author" in metadata and metadata["author"] != "LukeGrahamLandry":
            header_html += """
                Author: $AUTHOR 
            """.replace("$NAME", self.getDisplayName(title, metadata)).replace("$AUTHOR", metadata["author"])


        header_html += "<br><br></div> \n"

        return header_html

    def getExtraNavHTML(self, title, metadata):
        return self.extra_nav_html
    
    def getLicense(self, metadata):
        return """This content is available under the <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0 License</a>."""


class FetchedModDocsSiteSection(ModDocsSiteSection):
    def processFiles(self):
        if not os.path.isdir(OUTPUT_DIRECTORY + "/" + self.urlPrefix):
            os.mkdir(OUTPUT_DIRECTORY + "/" + self.urlPrefix)
        
        for page in self.pages:
            if page["branch"] == "wiki":
                continue

            url = self.getUrl(page)
            if url is None:
                print("no page url found " + json.dumps(page))
                continue
                
            print("building {} to {}".format(url, self.urlPrefix))

            title = page["name"].lower().replace(" ", "-")
            
            self.compileMD(title, urlCache.get(url), {
                "contact": "/discord", 
                "source_url": url, 
                "author": "LukeGrahamLandry", 
                "source": "https://github.com/" + page["repo"],
                "download": "https://www.curseforge.com/minecraft/mc-mods/" + page["curseforge"] + "/files",
                "mod_name": page["name"]
            })

    def generateMetaTags(self, title, metadata):
        return super().generateMetaTags(title, metadata) + \
            "<!-- the text on this page was fetched from " + metadata["source_url"] + " I'm fairly confident that I'm only getting my own content but if you feel I stole something, please DM me on discord: LukeGrahamLandry#6888 --> \n"

    def getUrl(self, page_data):
        if "url" in page_data:
            url = page_data["url"]
        elif "repo" in page_data:
            if not "branch" in page_data:
                page_data["branch"] = "main"

            url = "https://raw.githubusercontent.com/{}/{}/README.md".format(page_data["repo"], page_data["branch"])
        else:
            url = None
        
        return url
        
    def getLicense(self, metadata):
        return """This content is available under the <a href="$PATH" target="_blank">$NAME mod's license</a>.""" \
            .replace("$PATH", metadata["source"]).replace("$NAME", metadata["mod_name"])


class WikiModDocsSiteSection(FetchedModDocsSiteSection):
    def __init__(self, pages, sourceDir, urlPrefix, templateFile):
        super().__init__(pages, sourceDir, urlPrefix, templateFile)

    def processFiles(self):
        if not os.path.isdir(OUTPUT_DIRECTORY + "/" + self.urlPrefix):
            os.mkdir(OUTPUT_DIRECTORY + "/" + self.urlPrefix)

        for page in self.pages:
            if page["branch"] != "wiki":
                continue
            repo = page["repo"]

            url = "https://github.com/{}/wiki".format(repo)
            other_fetched_urls.append(url)
            os.system("git clone \"{}\"".format( "https://github.com/{}.wiki.git".format(repo)))
            self.current_repo_name = repo.split("/")[1]
            self.makeSubfolder(self.current_repo_name)
            folder = repo.split("/")[1] + ".wiki"

            with open(OUTPUT_DIRECTORY + "/_redirects", "a") as f:
                f.write("/{0}/{1} /{0}/{1}/Home\n".format(self.urlPrefix, self.current_repo_name))

            with open(folder + "/_Sidebar.md", "r") as f:
                md_content = "".join(f.readlines())
            nav_html = markdown.markdown(md_content, extensions=['fenced_code', "mdx_linkify"], tab_length=3)

            baseroot = None
            for root, dirs, files in os.walk(folder, topdown=True):
                if baseroot is None:
                    baseroot = root

                subdirectory = root.replace(baseroot + "/", "").replace(baseroot, "")
                
                for filename in files:
                    if ".md" not in filename:
                        continue

                    target = filename
                    if subdirectory != "":
                        target = subdirectory + "/" + filename
                    
                    print("building {}/{} to {}".format(url, filename, self.urlPrefix))

                    meta = {
                        "contact": "/discord", 
                        "source_url": url + "/" + filename.split(".")[0], 
                        "source": "https://github.com/" + repo,
                        "mod_name": repo.split("/")[1],
                        "nav_html": nav_html,
                        "page_title": page["name"]
                    }
                    if "curseforge" in page:
                        meta["download"] = "https://www.curseforge.com/minecraft/mc-mods/" + page["curseforge"] + "/files"

                    self.processMarkdownFile(baseroot, target, extraMetadata=meta, tab_length=3)
            
            for dir in dirs:
                self.makeSubfolder(dir)
            
            shutil.rmtree(folder)
    
    def getHeaderHtml(self, title, metadata):
        if title == "Home":
            title = "Wiki"
        
        return super().getHeaderHtml(title, metadata) + "<h1>{}</h1>".format(self.getDisplayName(title, metadata), title)

    def getExtraNavHTML(self, title, metadata):
        return "<br><b>" + metadata["page_title"]  + " Wiki </b>" + metadata["nav_html"] + "<b style=\"display: block; margin-bottom: 20px;\">Luke's Mods</b>" + super().getExtraNavHTML(title, metadata)

    def writeFile(self, title, html_content):
        out_path = "{}/{}/{}.html".format(self.urlPrefix, self.current_repo_name, title)
        if self.urlPrefix is None or self.urlPrefix == "":
            out_path = "{}.html".format(title)
        out_path = OUTPUT_DIRECTORY + "/" + out_path
            
        with open(out_path, "w") as f:
            f.write(html_content)
    
    def getCanonicalPath(self, title):
        path = "{}/{}/{}".format(self.urlPrefix, self.current_repo_name, title)
        return path

    def getDisplayName(self, title, metadata):
        return metadata["page_title"] + ": " + super().getDisplayName(title, metadata)


if __name__ == "__main__":
    urlCache = FetchedPageCache("scripts/generated/cache")
    
    if os.path.isdir(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)
    shutil.copytree("web", OUTPUT_DIRECTORY)

    # SiteSection("articles", "c", "article.html").processFiles()
    # SiteSection("vanilla", "vanilla", "vanilla.html").processFiles()
    
    versions = ["19", "18", "17", "16"]
    for v in versions:
        TutorialSiteSection("forge-1.{}-tutorials".format(v), "o{}".format(v), "tutorial.html").processFiles()
        UnversionedTutorialSiteSection("pages", "o{}".format(v), "tutorial.html").processFiles()
    
    modDocs = ModDocsSiteSection(site_data["fetched-pages"]["mods"], "mod-documentation", "mods", "mod-documentation.html")
    modDocs.processFiles()
    FetchedModDocsSiteSection(site_data["fetched-pages"]["mods"], "mod-documentation", "mods", "mod-documentation.html").processFiles()
    WikiModDocsSiteSection(site_data["fetched-pages"]["mods"], "mod-documentation", "mods", "mod-documentation.html").processFiles()
    
    with open("scripts/generated/videos.json", "r") as f:
        video_data = json.loads("".join(f.readlines()))
        CommissionsHelper(video_data["paid"], video_data["yt-clients"]).processFiles("commissions.html", "credits.html")
    
    toCopyToAllSections = ["commissions", "credits", "index"]
    for v in versions:
        for page in toCopyToAllSections:
            shutil.copy("{}/{}.html".format(OUTPUT_DIRECTORY, page), "{}/o{}/{}.html".format(OUTPUT_DIRECTORY, v, page))

    with open(OUTPUT_DIRECTORY + "/styles/code.css", "w") as f:
        f.write(formatter.get_style_defs())


# fetch the well written ones from forge community wiki
# sides, registries, access transformers, mods.toml, events, biome modifiers, block states, sounds, tinted textures
# use beutiful soup to get content and remove script and style tags
# keep license meta and add canonical 
# have a header like "<a>this content is from the Forge Community Wiki. Last Modified: date, License: MIT </a>"
# take out my footer links 
# https://docs.minecraftforge.net/en/1.19.x/misc/updatechecker/#update-json-format (MIT)
# https://github.com/Darkhax/darkhax-dot-net/blob/gh-pages/_posts/tutorials/2020-7-31-mixins.md (CC attribution)
