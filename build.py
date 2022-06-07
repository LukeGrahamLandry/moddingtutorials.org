import os
import markdown, json, shutil, requests
from pygments import lexers
from pygments import highlight 
from pygments.formatters import HtmlFormatter
import re
from xml.sax import saxutils as su
from datetime import datetime

with open("web/pages.json", "r") as f:
    site_data = json.loads("".join(f.readlines()))

lex = lexers.get_lexer_by_name("java")
formatter = HtmlFormatter()

with open("web/template.html", "r") as f:
    template = "".join(f.readlines())

ignore = ["about.md", "support.md", "my-mods.md", "contact.md"]
tutorials = ["java-basics", "environment-setup", "basic-items", "advanced-items", "basic-blocks", "advanced-blocks", "tools-armor", "tile-entities", "enchantments",
             "recipes"]

# html gen from videos.json
if True:
    with open("web/videos.json", "r") as f:
        video_data = json.loads("".join(f.readlines()))

    def getViews(video):
        return int(video["views"])

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

    def getVideosHTML(videos):
        videos.sort(reverse=True, key=getViews)

        video_html = ""

        for video in videos:
            video_html += '<a class="video" target="_blank" href="https://www.youtube.com/watch?v=' + video["id"] + '"> \n' 
            video_html += '<img src="/img/videos/' +  video["id"] + '.jpg" alt="video thumbnail"> \n'

            video_html += '<b class="title">' + video["title"][0:45] + "</b> \n"
            video_html += "<b>" + formatViewNumber(video["views"]) + ' Views </b> <b class="title"> by ' + video["channel"] + " </b> \n"
            video_html += "</a>\n"
        
        return video_html

    def getChannelsHTML(channels):
        channels.sort(reverse=True, key=getViews)

        html = '<link rel="stylesheet" href="/styles/channels.css">\n'

        for channel in channels:
            html += '<span class="channel"> \n' 
            html += '<img src="/img/videos/' +  channel["id"] + '.jpg" alt="video thumbnail"> \n'

            html += '<b class="title">' + channel["title"] + "</b> \n"
            html += '<b class="subs">' + formatViewNumber(channel["subscribers"]) + ' Subscribers </b> \n'
            html += '<b class="views">' + formatViewNumber(channel["views"]) + ' Views </b> \n'
            html += "</span>\n"
        
        return html

def combile_md(source_folder, filename, target_folder, pages_list, can=None):
    with open(source_folder + "/" + filename, "r") as f:
         md_content = "".join(f.readlines())
    html_content = markdown.markdown(md_content, extensions=['fenced_code', "mdx_linkify"])

    # print(html_content)

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
    
    title = ".".join(filename.split(".")[:-1])
    filename_to_write = title + ".html"
    
    # meta tags
    meta = ""
    if True:
        if title in site_data["un_versioned"]:
            meta += "<!-- submit a fix to the content of this page: https://github.com/LukeGrahamLandryMC/modding-tutorials/blob/master/pages/{} -->".format(filename)
        else:
            meta += "<!-- submit a fix to the content of this page: https://github.com/LukeGrahamLandryMC/modding-tutorials/blob/master/{}/{} -->".format(source_folder.split("/")[-1], filename)
        
        displayName = ""
        for part in filename.split(".")[0].split("-"):
            displayName += part[0].upper() + part[1:] + " "
        displayName += "| Minecraft Modding Tutorials"
        
        if title == "index":
            displayName = "Minecraft Forge Modding Tutorials"

        meta += "<title>" + displayName + "</title>"
        path = title
        if target_folder is not None and title not in site_data["un_versioned"]:
            path = target_folder + "/" + path
        else:
            if can is not None and title not in site_data["un_versioned"]:
                path = can + "/" + path
        meta += '<link rel="canonical" href="https://moddingtutorials.org/' + path + '"/>'

        if title in site_data["descriptions"]:
            meta += '<meta name="description" content="' + site_data["descriptions"][title] + '">'

    full_content = template.replace("$CONTENT", html_syntax_highlighted).replace("$META", meta).replace("$TUTORIALS", json.dumps(pages_list)).replace("\$CHANNELS", getChannelsHTML(video_data["yt-clients"]))

    generateSlashRedirectFix(target_folder, title)

    if target_folder is None:
        with open(filename_to_write, "w") as f:
            f.write(full_content)
    else: 
        with open(target_folder + "/" + filename_to_write, "w") as f:
            f.write(full_content)

def buildSite():
    default_section_url = "o18"

    for section_data in site_data["sections"]:
        for root, dirs, files in os.walk(section_data["folder"], topdown=False):
            if not os.path.isdir(section_data["url"]):
                os.mkdir(section_data["url"])

            for rooti, dirsi, filesi in os.walk("pages", topdown=False):
                for namei in filesi:
                    if (".md" in namei):
                        print(section_data["url"], namei)
                        combile_md(rooti, namei, section_data["url"], section_data["files"])

                        if section_data["url"] == default_section_url:
                            combile_md(rooti, namei, None, section_data["files"], default_section_url)

            for name in files:
                if (".md" in name):
                    print(section_data["url"], name)
                    combile_md(root, name, section_data["url"], section_data["files"])

                    if section_data["url"] == default_section_url:
                        combile_md(root, name, None, section_data["files"], default_section_url)

    for root, dirs, files in os.walk("web", topdown=True):
        for dir in dirs:
            if (not os.path.isdir(dir)):
                os.mkdir(dir)

        rel_dir = os.path.relpath(root, os.getcwd() + "/web")

        if (not os.path.isdir(rel_dir)):
            os.mkdir(rel_dir)

        for file in files:
            if ".py" in file or ".json" in file:
                continue

            shutil.copy("web/" + rel_dir + "/" + file, rel_dir + "/" + file)

    with open("code.css", "w") as f:
        f.write(formatter.get_style_defs())

    shutil.copy("o16/index.html", "index.html")

    with open("web/my-mods.html", "r") as f:
        my_mods_html = "".join(f.readlines())

    my_mods_html = my_mods_html.replace("$VIDEOS", getVideosHTML(video_data["paid"])) # .replace("$FORGE1.15", getVideosHTML(video_data["1.15"]))

    with open("my-mods.html", "w") as f:
        f.write(my_mods_html)

    with open("web/commissions.html", "r") as f:
        commissions_html = "".join(f.readlines())

    commissions_html = commissions_html.replace("$VIDEOS", getVideosHTML(video_data["paid"])).replace("$CHANNELS", getChannelsHTML(video_data["yt-clients"])) # .replace("$FORGE1.15", getVideosHTML(video_data["1.15"]))

    with open("commissions.html", "w") as f:
        f.write(commissions_html)

    with open("web/index.html", "r") as f:
        index_html = "".join(f.readlines())

    for section_info in site_data["sections"]:
        url = section_info["url"]
        shutil.copy("my-mods.html", url + "/my-mods.html")
        shutil.copy("commissions.html", url + "/commissions.html")
        with open(url + "/index.html", "w") as f:
            f.write(index_html)

    shutil.copy(default_section_url + "/index.html", "index.html")


def generateSlashRedirectFix(directory, filename):
    # ugly hack

    if directory is None:
        if (not os.path.isdir(filename)):
            os.mkdir(filename)
        with open(filename + "/index.html", "w") as f:
            f.write('<link rel="canonical" href="https://moddingtutorials.org/' + filename + '"/>')
            f.write('cloudflare pages can not deal with trailing slashes properly. redirecting to <a href="/' + filename + '">' + filename + '</a> <script> window.location.href = "/' + filename + '";</script>')

    else:
        if (not os.path.isdir(directory + "/" + filename)):
            os.mkdir(directory + "/" + filename)
        with open(directory + "/" + filename + "/index.html", "w") as f:
            f.write('<link rel="canonical" href="https://moddingtutorials.org/' + directory + "/" + filename + '"/>')
            f.write('cloudflare pages can not deal with trailing slashes properly. redirecting to <a href="/' + directory + "/" + filename + '">' + filename + '</a> <script> window.location.href = "/' + directory + "/" + filename + '";</script>')


def buildFetchedPages():
    drop_down_list = """
        <option hidden selected> Change Site Section </option>
        <option value="/o18"> Forge Modding Tutorials </option>
        <option value="/commissions"> Mod Commissions </option>
    """

    for directory, pages in site_data["fetched-pages"].items():
        if not os.path.isdir(directory):
                os.mkdir(directory)

        page_index = ""
        for page in pages:
            name = page["name"].lower().replace(" ", "-")
            page_index += '<a href="{}" class="post">{}</a>'.format(name, page["name"]) 

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
            
            html_content = markdown.markdown(r.text, extensions=['fenced_code'])

            if "curseforge" in page:
                html_content += '<br> <a href="https://www.curseforge.com/minecraft/mc-mods/' + page["curseforge"] + '" class="btn btn-primary" style="width: 100%;"> Download Mod On Curse Forge </a>'

            full_content = template.replace("$CONTENT", html_content).replace("$META", meta).replace("$INDEX", page_index)

            with open(directory + "/" + filename + ".html", "w") as f:
                f.write(full_content)

            generateSlashRedirectFix(directory, filename)

buildSite()
buildFetchedPages()

# export PATH=$PATH:/opt/buildhome/.local/bin && pip3 install requests && pip3 install markdown && pip3 install pygments && pip3 install mdx_linkify && python3 build.py
# PYTHON_VERSION 3.7

# https://cf.way2muchnoise.eu/