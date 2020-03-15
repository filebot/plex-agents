import re, Media, VideoFiles

from filebot import *


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  VideoFiles.Scan(path, files, mediaList, subdirs, root)

  for file in files:
    attr = xattr_metadata(file)
    if attr is None:
      continue

    print("[XATTR] %s" % attr)

    # single episode | multi episode
    episodes = list_episodes(attr)
    multi_episode_count = len(episodes)

    for i, attr in enumerate(episodes):
      guid = series_guid(attr)
      name = series_name(attr)
      special = episode_special_number(attr)

      media = Media.Episode(
        name.encode('utf-8'),                           # use str since Plex doesn't like unicode strings
        0 if special else episode_season_number(attr),
        special if special else episode_number(attr),
        episode_title(attr).encode('utf-8'),            # use str since Plex doesn't like unicode strings
        series_year(attr)
      )

      date = episode_date(attr)
      if date:
        media.released_at = date.strftime('%Y-%m-%d')

      if (multi_episode_count > 1):
        media.display_offset = (i * 100) / multi_episode_count

      original_filename = xattr_filename(file)
      if original_filename:
        media.source = VideoFiles.RetrieveSource(original_filename.encode('utf-8'))

      media.parts.append(file)
      mediaList.append(media)

      print("[MEDIA] %s | %s | %s | %s" % (media, media.year, media.released_at, media.source))
