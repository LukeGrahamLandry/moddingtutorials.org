from googleapiclient.discovery import build
import requests, json
from PIL import Image

with open("pages.json", "r") as f:
    site_data = json.loads("".join(f.readlines()))

data = {
    "paid": []
}

# probably shouldn't have my api key public like this
# but it should only be able to access the youtube api v3 so it doesn't really matter
api_key = "AIzaSyD3YtUIi_m0OHp_fcZxLSInHPr2KWzuJKM"
youtube = build('youtube', 'v3', developerKey=api_key)

def getInfo(video_id):
    info = {}

    print(video_id)
    info["id"] = video_id

    print("start thumbnail")
    
    thumnail_url = "http://img.youtube.com/vi/" + video_id + "/0.jpg"

    img_data = requests.get(thumnail_url).content
    filename = 'img/videos/' + video_id + '.jpg'
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    
    im = Image.open(filename)
    im = im.crop((0, 45, im.size[0], im.size[1] - 45))
    im.save(filename)

    print("start video_request")
    
    video_request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )

    video_response = video_request.execute()

    # print(json.dumps(video_response, indent=4))

    info["title"] = video_response['items'][0]['snippet']['title']
    info["views"] = video_response['items'][0]['statistics']['viewCount']
    info["time"] = video_response["items"][0]["snippet"]["publishedAt"] 

    print("start c_request")

    channel_id = video_response["items"][0]["snippet"]["channelId"]

    c_request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )

    c_response = c_request.execute()
    # print(json.dumps(c_response, indent=4))

    info["channel"] = c_response['items'][0]['snippet']['title']

    return info

for video_url in site_data["videos"]:
    if "watch" in video_url:
        video_id = video_url.split("v=")[1]
    else:
        video_id = video_url.split("be/")[1]

    data["paid"].append(getInfo(video_id))

for name, playlist_id in site_data["playlists"].items():
    data[name] = []

    p_request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 50
    )
    p_response = p_request.execute()
    playlist_items = []
    while p_request is not None:
        p_response = p_request.execute()
        playlist_items += p_response["items"]
        p_request = youtube.playlistItems().list_next(p_request, p_response)

    for vid in playlist_items:
        vid_id = vid["snippet"]["resourceId"]["videoId"]
        data[name].append(getInfo(vid_id))

youtube.close()

with open("videos.json", "w") as f:
    f.write(json.dumps(data, indent=4))