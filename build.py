import os
import markdown, json, shutil, requests
from pygments import lexers
from pygments import highlight 
from pygments.formatters import HtmlFormatter
from xml.sax import saxutils as su
import frontmatter

with open("web/pages.json", "r") as f:
    site_data = json.loads("".join(f.readlines()))

lex = lexers.get_lexer_by_name("java")
formatter = HtmlFormatter()

OUTPUT_DIRECTORY = "dist"

class CommissionsHelper:
    @staticmethod
    def processCommissionsPage():
        with open("web/videos.json", "r") as f:
            video_data = json.loads("".join(f.readlines()))

        with open("web/commissions.html", "r") as f:
            commissions_html = "".join(f.readlines())

        commissions_html = commissions_html.replace("$VIDEOS", CommissionsHelper.getVideosHTML(video_data["paid"])).replace("$CHANNELS", CommissionsHelper.getChannelsHTML(video_data["yt-clients"]))

        with open(OUTPUT_DIRECTORY + "/commissions.html", "w") as f:
            f.write(commissions_html)

        
    @staticmethod
    def getViews(video):
        return int(video["views"])

    @staticmethod
    def formatViewNumber(views):
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

    @staticmethod
    def getVideosHTML(videos):
        videos.sort(reverse=True, key=CommissionsHelper.getViews)

        video_html = ""

        for video in videos:
            video_html += '<a class="video" target="_blank" href="https://www.youtube.com/watch?v=' + video["id"] + '"> \n' 
            video_html += '<img src="/img/videos/' +  video["id"] + '.jpg" alt="video thumbnail"> \n'

            video_html += '<b class="title">' + video["title"][0:45] + "</b> \n"
            video_html += "<b>" + CommissionsHelper.formatViewNumber(video["views"]) + ' Views </b> <b class="title"> by ' + video["channel"] + " </b> \n"
            video_html += "</a>\n"
        
        return video_html

    @staticmethod
    def getChannelsHTML(channels):
        channels.sort(reverse=True, key=CommissionsHelper.getViews)

        html = '<link rel="stylesheet" href="/styles/channels.css">\n'

        for channel in channels:
            html += '<span class="channel"> \n' 
            html += '<img src="/img/videos/' +  channel["id"] + '.jpg" alt="video thumbnail"> \n'

            html += '<b class="title">' + channel["title"] + "</b> \n"
            html += '<b class="subs">' + CommissionsHelper.formatViewNumber(channel["subscribers"]) + ' Subscribers </b> \n'
            html += '<b class="views">' + CommissionsHelper.formatViewNumber(channel["views"]) + ' Views </b> \n'
            html += "</span>\n"
        
        return html


# TODO: refactor into a SiteSection implementation
def buildFetchedPages(extra_nav_html):
    with open("web/templates/mod-documentation.html", "r") as f:
        template = "".join(f.readlines())
    
    for directory, pages in site_data["fetched-pages"].items():
        if not os.path.isdir(OUTPUT_DIRECTORY + "/" + directory):
                os.mkdir(OUTPUT_DIRECTORY + "/" + directory)

        for page in pages:
            url = None

            if "repo" in page:
                if not "branch" in page:
                    page["branch"] = "main"

                url = "https://raw.githubusercontent.com/{}/{}/README.md".format(page["repo"], page["branch"])
            
            if url is None:
                print("no page url found " + json.dumps(page))
                continue

            r = requests.get(url)
            if not r.status_code == 200:
                print("error " + str(r.status_code) + " " + url)
                continue

            filename = page["name"].lower().replace(" ", "-")

            meta = "<title>" + page["name"] + "</title>"
            meta += '<link rel="canonical" href="https://moddingtutorials.org/{}/{}"/>'.format(directory, filename)
            meta += "<!-- the text on this page was fetched from " + url + " I'm fairly confident that I'm only getting my own content but if you feel I stole something, please DM me on discord: LukeGrahamLandry#6888 -->"
            
            html_content = """<div style="text-align: center; margin-top: 10px;">"""

            if "curseforge" in page:
                html_content += """
                    <a class="alert orange sm" style="display: inline-block;" href="https://www.curseforge.com/minecraft/mc-mods/$CF" target="_blank">
                    Download Mod
                    </a>
                """.replace("$CF", page["curseforge"])
            
            html_content += """
                <a class="alert black sm" style="display: inline-block;" href="https://github.com/$PATH" target="_blank">
                    Source Code
                </a>
                <a class="alert blue sm" style="display: inline-block;" href="/discord" target="_blank">
                    Contact Author
                </a>
                </div>
            """.replace("$PATH", page["repo"])

            html_content += markdown.markdown(r.text, extensions=['fenced_code'])

            license_html = """
            This content is available under the <a href="$PATH" target="_blank">$NAME mod's license</a>. 
            """.replace("$PATH", "https://github.com/" + page["repo"]).replace("$NAME", page["name"])

            full_content = template.replace("$CONTENT", html_content).replace("$META", meta).replace("$LICENSE", license_html).replace("$NAV", extra_nav_html)

            with open(OUTPUT_DIRECTORY + "/" + directory + "/" + filename + ".html", "w") as f:
                f.write(full_content)

# TODO: refactor so i dont need this referenced in the normal SiteSection, should only be in TutorialSiteSection
defaultNamespace = "o19"

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
                
                self.compileMD(baseroot, target)
            
            for dir in dirs:
                os.mkdir(OUTPUT_DIRECTORY + "/" +  self.urlPrefix + "/" + dir)

                if self.urlPrefix == defaultNamespace:
                    os.mkdir(OUTPUT_DIRECTORY + "/" + dir)

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
        displayName = ""
        for part in title.split("-"):
            displayName += part[0].upper() + part[1:] + " "
        
        return displayName

    def generateMetaTags(self, title, metadata):
        meta = "<title>{}</title> \n".format(self.getDisplayName(title, metadata))
        meta += '<link rel="canonical" href="https://moddingtutorials.org/{}"/> \n'.format(self.getCanonicalPath(title))
        meta += '<meta name="description" content="{}"> \n'.format(self.getDescription(title, metadata))
        return meta

    def handleReplacements(self, html_content, title, metadata):
        return self.template_html.replace("$CONTENT", html_content).replace("$META", self.generateMetaTags(title, metadata))

    def compileMD(self, source_folder_path, filename):
        print("building {}/{} to {}".format(source_folder_path, filename, self.urlPrefix))

        title = ".".join(filename.split(".")[:-1])
        with open(source_folder_path + "/" + filename, "r") as f:
            metadata, md_content = frontmatter.parse(f.read())
        
        html_content = markdown.markdown(md_content, extensions=['fenced_code', "mdx_linkify"])
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
    def __init__(self, sourceDir, urlPrefix, templateFile):
        super().__init__(sourceDir, urlPrefix, templateFile)
    
    def getDescription(self, title, metadata):
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

        if self.urlPrefix == defaultNamespace:
            out_path = "{}/{}.html".format(OUTPUT_DIRECTORY, title)
            with open(out_path, "w") as f:
                f.write(html_content)

# for pages that are the same between MC versions. sets the canonical tag to the root/title instead of root/version/title so google doesn't punish me for duplicate content
class UnversionedTutorialSiteSection(TutorialSiteSection):
    def getCanonicalPath(self, title):
        return title

class ModDocsSiteSection(SiteSection):
    def __init__(self, sourceDir, urlPrefix, templateFile):
        super().__init__(sourceDir, urlPrefix, templateFile)
        self.extra_nav_html = self.generateModDocsIndexHtml()
    
    def generateModDocsIndexHtml(self):
        index_html = ""

        # fetched
        for page in site_data["fetched-pages"][self.urlPrefix]:
            name = page["name"].lower().replace(" ", "-")
            index_html += '<a href="{}" class="post">{}</a>'.format(name, page["name"])
        
        index_html += "<hr/>"

        # md files
        for root, dirs, files in os.walk(self.sourceDir, topdown=True):
            for filename in files:
                if filename == "index.md" or ".md" not in filename:
                    continue
                
                name = filename.split(".")[0]
                displayName = ""
                for part in name.split("-"):
                    displayName += part[0].upper() + part[1:] + " "

                index_html += '<a href="{}" class="post">{}</a>'.format(name, displayName)

            break

        return index_html

    # valid front matter keys: description, author, version, source, download, contact
    def handleReplacements(self, html_content, title, metadata):
        header_html = """
            <div style="text-align: center; margin-top: 10px;">
        """
        
        if "author" in metadata:
            header_html += """
                
                <h1 style="margin-bottom: 0px"> $NAME by $AUTHOR </h1>
            """.replace("$NAME", self.getDisplayName(title, metadata)).replace("$AUTHOR", metadata["author"])

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

        header_html += "<br><br></div>"
        license_html = """This content is available under the <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0 License</a>."""

        full_content = super().handleReplacements(header_html + html_content, title, metadata)
        full_content = full_content.replace("$LICENSE", license_html).replace("$NAV", self.extra_nav_html)
        return full_content


if __name__ == "__main__":
    if os.path.isdir(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)
    shutil.copytree("web", OUTPUT_DIRECTORY)

    # SiteSection("articles", "c", "article.html").processFiles()
    # SiteSection("vanilla", "vanilla", "article.html").processFiles()
    
    versions = ["19", "18", "17", "16"]
    for v in versions:
        TutorialSiteSection("forge-1.{}-tutorials".format(v), "o{}".format(v), "tutorial.html").processFiles()

        UnversionedTutorialSiteSection("pages", "o{}".format(v), "tutorial.html").processFiles()
    
    modDocs = ModDocsSiteSection("mod-documentation", "mods", "mod-documentation.html")
    modDocs.processFiles()
    try:
        buildFetchedPages(modDocs.extra_nav_html)
    except requests.exceptions.ConnectionError:
        print("Failed to buildFetchedPages, you're probably not connected to the internet.")

    CommissionsHelper.processCommissionsPage()
    for v in versions:
        url = "o" + v
        shutil.copy(OUTPUT_DIRECTORY + "/commissions.html", OUTPUT_DIRECTORY + "/" + url + "/commissions.html")
        shutil.copy(OUTPUT_DIRECTORY + "/index.html",  OUTPUT_DIRECTORY + "/" + url + "/index.html")
    
    with open(OUTPUT_DIRECTORY + "/styles/code.css", "w") as f:
        f.write(formatter.get_style_defs())
