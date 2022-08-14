import requests, json

with open("web/pages.json", "r") as f:
    site_data = json.loads("".join(f.readlines()))

try:
    github_html = requests.get("https://github.com/LukeGrahamLandry/modding-tutorials").text
    commit_count = github_html.split("<span class=\"d-none d-sm-inline\">")[2].split("</strong>")[0].split("\n                    <strong>")[1]
except:
    print("commit count error")
    commit_count = "xx"

short_name = "MC Modding " + site_data["sections"][0]["title"] + " Version 1." + commit_count
# Minecraft Forge 1.18.1 Modding Tutorial Version 1.37 by LukeGrahamLandry#6888 (moddingtutorials.org), updated 2021/12/21
full_name = "Minecraft {} Modding Tutorial by LukeGrahamLandry#6888 (moddingtutorials.org), Version 1.{} updated {}".format(site_data["sections"][0]["title"], commit_count, datetime.now().strftime("%Y/%m/%d"))
print("start build pdf: ", full_name)

# https://realpython.com/creating-modifying-pdf/