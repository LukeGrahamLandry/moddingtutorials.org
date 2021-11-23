import os
import markdown, json, shutil
from pygments import lexers
from pygments import highlight 
from pygments.formatters import HtmlFormatter
import re
from xml.sax import saxutils as su

with open("web/pages.json", "r") as f:
    site_data = json.loads("".join(f.readlines()))

lex = lexers.get_lexer_by_name("java")
formatter = HtmlFormatter()

with open("web/template.html", "r") as f:
    template = "".join(f.readlines())

ignore = ["about.md", "support.md", "my-mods.md", "contact.md"]
tutorials = ["java-basics", "environment-setup", "basic-items", "advanced-items", "basic-blocks", "advanced-blocks", "tools-armor", "tile-entities", "enchantments",
             "recipes"]

def combile_md(source_folder, filename, target_folder, index_html, pages_list, versions_html, can=None):
    with open(source_folder + "/" + filename, "r") as f:
         md_content = "".join(f.readlines())
    html_content = markdown.markdown(md_content, extensions=['fenced_code'])

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

    full_content = template.replace("$CONTENT", html_syntax_highlighted).replace("$META", meta).replace("$INDEX", index_html).replace("$TUTORIALS", json.dumps(pages_list)).replace("$VERSIONS", versions_html)

    if target_folder is None:
        with open(filename_to_write, "w") as f:
            f.write(full_content)

        # ugly hack
        if (not os.path.isdir( title)):
            os.mkdir(title)
        with open(title + "/index.html", "w") as f:
            f.write('<link rel="canonical" href="https://moddingtutorials.org/' + title + '"/>')
            f.write('cloudflare pages can not deal with trailing slashes properly. redirecting to <a href="' + title + '">' + title + '</a> <script> window.location.href = "/' + title + '";</script>')
    else: 
        with open(target_folder + "/" + filename_to_write, "w") as f:
            f.write(full_content)

        # ugly hack
        if (not os.path.isdir(target_folder + "/" + title)):
            os.mkdir(target_folder + "/" + title)
        
        with open(target_folder + "/" + title + "/index.html", "w") as f:
            f.write('<link rel="canonical" href="https://moddingtutorials.org/' + target_folder + "/" + title + '"/>')
            f.write('cloudflare pages can not deal with trailing slashes properly. redirecting to <a href="' + target_folder + "/" + title + '">' + title + '</a> <script> window.location.href = "/' + target_folder + "/" + title + '";</script>')

versions_select = {}
default_section_url = "o16"

for section_data in site_data["sections"]:
    for root, dirs, files in os.walk(section_data["folder"], topdown=False):
        if not os.path.isdir(section_data["url"]):
            os.mkdir(section_data["url"])

        index_html = ""
        for page_name in section_data["files"]:
            displayName = ""
            for part in page_name.split("-"):
                displayName += part[0].upper() + part[1:] + " "
        
            index_html += '<a href="/' + section_data["url"] + "/" + page_name + '" class="post">' + displayName + '</a>'

        versions_html = ""
        for s in site_data["sections"]:
             versions_html += '<option value="' + s["url"] + '"'
             if s["url"] == section_data["url"]:
                 versions_html += " selected"
             versions_html += '>' + s["title"] + "</option>"

        versions_select[section_data["url"]] = versions_html

        for rooti, dirsi, filesi in os.walk("pages", topdown=False):
            for namei in filesi:
                if (".md" in namei):
                    print(section_data["url"], namei)
                    combile_md(rooti, namei, section_data["url"], index_html, section_data["files"], versions_html)

                    if section_data["url"] == default_section_url:
                        combile_md(rooti, namei, None, index_html, section_data["files"], versions_html, default_section_url)

        for name in files:
            if (".md" in name):
                print(section_data["url"], name)
                combile_md(root, name, section_data["url"], index_html, section_data["files"], versions_html)

                if section_data["url"] == default_section_url:
                    combile_md(root, name, None, index_html, section_data["files"], versions_html, default_section_url)

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

with open("web/videos.json", "r") as f:
    video_data = json.loads("".join(f.readlines()))

def getViews(video):
    return int(video["views"])

def getVideosHTML(videos):
    videos.sort(reverse=True, key=getViews)

    video_html = ""

    for video in videos:
        video_html += '<a class="video" href="https://www.youtube.com/watch?v=' + video["id"] + '"> \n' 
        video_html += '<img src="/img/videos/' +  video["id"] + '.jpg" alt="video thumbnail"> \n'

        video["views"] = int(video["views"])
        if video["views"] >= 1000000:
            views = str(video["views"] / 1000000)[0:3] + "M"
        elif video["views"] >= 1000:
            views = str(video["views"] // 1000) + "K"
        else:
            views = str(video["views"])

        video_html += '<b class="title">' + video["title"][0:45] + "</b> \n"
        video_html += "<b>" + views + ' Views </b> <b class="title"> by ' + video["channel"] + " </b> \n"
        video_html += "</a>\n"
    
    return video_html

with open("web/my-mods.html", "r") as f:
    my_mods_html = "".join(f.readlines())

my_mods_html = my_mods_html.replace("$VIDEOS", getVideosHTML(video_data["paid"])) # .replace("$FORGE1.15", getVideosHTML(video_data["1.15"]))

with open("my-mods.html", "w") as f:
     f.write(my_mods_html)

with open("web/index.html", "r") as f:
    index_html = "".join(f.readlines())

for url, versions_html in versions_select.items():
    shutil.copy("my-mods.html", url + "/my-mods.html")
    with open(url + "/index.html", "w") as f:
        f.write(index_html.replace("$VERSIONS", versions_html))

shutil.copy(default_section_url + "/index.html", "index.html")

# export PATH=$PATH:/opt/buildhome/.local/bin && pip3 install markdown && pip3 install pygments && python3 build.py
