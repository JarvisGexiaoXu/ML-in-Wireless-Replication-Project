# API client library get it using: pip install google-api-python-client
import googleapiclient.discovery
import pandas as pd
# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = "YOUR OWN API KEY"
# API client
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)
# 'request' variable is the only thing you must change
# depending on the resource and method you need to use
# in your query
topics = ['Politics','Baseball','Rugby','Anime','Boxing','History','Tutorial','Trailers','Food','Reaction']
for topic in topics:
    request = youtube.search().list(
            part = "id,snippet",
            type = 'video',
            regionCode = "US",
            order = "relevance",
            q = topic,
            videoDuration = 'short',
            videoDefinition = 'high',
            maxResults = 50,
            fields="items(id(videoId),snippet(thumbnails.default,title,description))"
    )
    # Query execution
    response = request.execute()
    # Print the results
    print(response)

    # Get thumbnails
    thumbnail_url = response['items'][0]['snippet']['thumbnails']['default']['url']
    title = response['items'][0]['snippet']['title']
    description = response['items'][0]['snippet']['description']
    v_id = response['items'][0]['id']['videoId']

    # use dictionary to store data
    data = {
        'vid':[],
        'title':[],
        'description':[],
        'thumbnail':[],
        'view_counts':[]    
    }
    for item in response['items']:
        vid = item['id']['videoId']

        r = youtube.videos().list(
            part = "statistics",
            id = vid,
            fields = "items(statistics)"
        ).execute()
        try:
            title = item['snippet']['title']
            description = item['snippet']['description']
            v_id = item['id']['videoId']
            thumbnail_url = item['snippet']['thumbnails']['default']['url']
            view_count = r['items'][0]['statistics']['viewCount']
            data['vid'].append(v_id)
            data['title'].append(title)
            data['description'].append(description)
            data['thumbnail'].append(thumbnail_url)
            data['view_counts'].append(view_count)    
        except:
            pass

    print(data)
    pd.DataFrame(data = data).to_csv('./YouTube_dataset/'+topic+'.csv')


# # The following code is used to get thumbnail from the corresponding url 
# from PIL import Image
# import requests
# import matplotlib.pyplot as plt
# import numpy as np

# r = requests.get(url, stream=True)
# img = Image.open(r.raw)
# # Convert thumbnail to np array
# img_np = np.asarray(img)
# print(img_np)
# # Convert np array to thumbnail
# im = Image.fromarray(np.uint8(img_np))
# plt.imshow(img)
# plt.show()
# plt.imshow(im)
# plt.show()
