#!/usr/bin/env python
from ricecooker.chefs import SushiChef
# from ricecooker.classes.nodes import ChannelNode, TopicNode, DocumentNode
# from ricecooker.classes.files import DocumentFile
from ricecooker.classes import nodes, files, questions, licenses
from ricecooker.config import LOGGER              # Use LOGGER to print messages
from ricecooker.exceptions import raise_for_invalid_channel
# from le_utils.constants import exercises, content_kinds, file_formats, format_presets, languages
from ricecooker.classes.licenses import get_license
import re
import youtube_dl

# Run constants
################################################################################
CHANNEL_NAME = "eKitabu Digital Story Time"                                # Name of channel
CHANNEL_SOURCE_ID = "sushi-chef-ekitabu-dst"
CHANNEL_DOMAIN = "https://www.youtube.com/c/Ekitabuplus"          # Who is providing the content
CHANNEL_LANGUAGE = "en"                                           # Language of channel
CHANNEL_DESCRIPTION = "Interactive resources for eKitabu Digital Story Time"
CHANNEL_THUMBNAIL = "https://i.ytimg.com/vi/Egw81i5iZpY/hqdefault.jpg?sqp=-oaymwEXCNACELwBSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLB3O9XMBZ3BiLPuyESaz26DX8qX6Q"

# Additional constants
################################################################################

PLAYLISTS_URL = "https://www.youtube.com/playlist?list=PLfRU3c2GZU0uTjY6ZmlYDHFdU0U_6Hauw"
AUTHOR = "eKitabu"
LICENSE = get_license(licenses.CC_BY,
        copyright_holder = AUTHOR).as_dict()

# The chef subclass
################################################################################

class DigitalStoryTime(SushiChef):
    channel_info = {
        "CHANNEL_TITLE": CHANNEL_NAME,
        "CHANNEL_SOURCE_DOMAIN": CHANNEL_DOMAIN,  # where content comes from
        "CHANNEL_SOURCE_ID": CHANNEL_SOURCE_ID,  # CHANGE ME!!!
        "CHANNEL_LANGUAGE": LANGUAGE,  # le_utils language code
        "CHANNEL_THUMBNAIL": CHANNEL_THUMBNAIL,  # (optional)
        "CHANNEL_DESCRIPTION": CHANNEL_DESCRIPTION,  # (optional)
    }

    def construct_channel(self, **kwargs):
        channel = self.get_channel(**kwargs)
        # Download the playlist/video information
        try:
            with youtube_dl.YoutubeDL({'skip_download': True}) as ydl:
              info_dict = ydl.extract_info(PLAYLISTS_URL, download=False)
              print (info_dict.keys())

              # Generate topics based off playlist entries in dict
              #for playlist in info_dict['entries']:
  
                  # Get language of playlist (hack)
              #    language = "fr"
              #    if "English" in playlist['title']:
              #        language = "en"
              #    elif "Arabic" in playlist['title']:
              language = "en"
  
              #    playlist_topic = nodes.TopicNode(title=playlist['title'], source_id=playlist['id'], language=language)
              #    channel.add_child(playlist_topic)
  

                  # Generate videos based off video entries in dict
              videos = sorted(info_dict['entries'], key=lambda x: int(re.search("\d+", x['title']).group()))
              print( [v['title'] for v in videos])
              import time
              time.sleep(15)
              for video in videos:
                  #try:
                  #    num, = re.findall("\d+",video['title'])
                  #    title = re.sub(video['title'], num, "")
                  #    title = ("0"+num)[-2:] + " " + title 
                  #except Exception as e:
                  #    print (e)
                  #    print (video['title'])
                  #    print (repr(video['title']))
                  #    raise
                  thumbnail_url = len(video['thumbnails']) and video['thumbnails'][0]['url']

                  channel.add_child(nodes.VideoNode(
                      title = video['title'],
                      source_id = video['id'],
                      license = LICENSE,
                      description = video['description'],
                      derive_thumbnail = not thumbnail_url,
                      files = [files.WebVideoFile(video['webpage_url'])],
                      thumbnail = thumbnail_url,
                      author = AUTHOR,
                      # tags = video['categories'] + video['tags'], # TODO: uncomment this when added
                      ))
        except Exception as e:
            import traceback, sys
            traceback.print_exc(file=sys.stdout)
            raise
    
        raise_for_invalid_channel(channel)  # Check for errors in channel construction

        return channel


if __name__ == "__main__":
    """
    Run this script on the command line using:
        python sushichef.py  --token=YOURTOKENHERE9139139f3a23232
    """
    simple_chef = DigitalStoryTime()
    simple_chef.main()