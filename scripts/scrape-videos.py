from googleapiclient.discovery import build
import requests, json
from PIL import Image
import time

"""
    Fetches data about a given youtube video from the api.
    Returns {id, title, views, time, channel}
    Saves video thumbnail at img/videos/[id].jpg
"""
def getVideoInfo(video_id):
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
    im = im.resize((180, 100))
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


"""
    Fetches data about a given youtube channel from the api.
    Returns {id, title, views, subscribers}
    Saves channel icon at img/videos/[id].jpg
"""
def getChannelInfo(channel_id):
    info = {}

    print(channel_id)
    info["id"] = channel_id

    print("start channel_request")
    
    api_request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )

    api_response = api_request.execute()

    # print(json.dumps(video_response, indent=4))

    info["title"] = api_response['items'][0]['snippet']['title']
    info["views"] = api_response['items'][0]['statistics']['viewCount']
    info["subscribers"] = api_response['items'][0]['statistics']['subscriberCount']

    print("start img")
    img_url = list(api_response['items'][0]['snippet']["thumbnails"].values())[0]["url"]
    print(img_url)
    img_data = requests.get(img_url).content
    filename = 'img/videos/' + channel_id + '.jpg'
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    
    return info


"""
    Fetches data for a list of videos.
"""
def processVideos(video_urls):
    result = []
    total = 0

    for video_url in video_urls:
        if "watch" in video_url:
            video_id = video_url.split("v=")[1]
        else:
            video_id = video_url.split("be/")[1]

        try:
            video_data = getVideoInfo(video_id)
            result.append(video_data)
            total += int(video_data["views"])
        except:
            print("Failed video: " + video_id)

        time.sleep(1)
    
    print("total views:", total)

    return result


"""
    Fetches data for a list of channels.
"""
def processChannels(channel_ids):
    result = []
    for channel_id in channel_ids:
        result.append(getChannelInfo(channel_id))
        time.sleep(1)
    
    return result


if __name__ == "__main__":
    api_key = "AIzaSyD3YtUIi_m0OHp_fcZxLSInHPr2KWzuJKM"
    youtube = build('youtube', 'v3', developerKey=api_key)

    with open("pages.json", "r") as f:
        site_data = json.loads("".join(f.readlines()))

    data = {
        "paid": processVideos(site_data["videos"]),
        "yt-clients": processChannels(site_data["yt-clients"])
    }

    with open("generated/videos.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    
    youtube.close()
