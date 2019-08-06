import Media, VideoFiles

from filebot import *


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  VideoFiles.Scan(path, files, mediaList, subdirs, root)

  for file in files:
    attr = xattr_metadata(file)
    if attr is None:
      continue

    episodes = list_episodes(attr)
    for i, attr in enumerate(episodes):
      guid = series_guid(attr)
      if guid is None:
        continue

      episode = Media.Episode(
        str(series_name(attr)),
        episode_season_number(attr),
        episode_number(attr),
        str(episode_title(attr)),
        series_year(attr)
      )

      date = episode_date(attr)
      if date:
        episode.released_at = date.strftime('%Y-%m-%d')

      if (len(episodes) > 1):
        episode.display_offset = (i * 100) / len(episodes)

      print(episode)
      episode.parts.append(file)
      mediaList.append(episode)




# python "FileBot Xattr Series Scanner.py" /path/to/files
if __name__ == "__main__":
  import os

  for arg in sys.argv:
    for root, folders, files in os.walk(arg):
      for name in files:
        file = os.path.join(root, name)
        attr = xattr_metadata(file)
        if attr:
          episodes = list_episodes(attr)
          for episode in episodes:
            guid = series_guid(episode)
            if guid:
              print "%s\t%s\t%s" % (guid, episode, file)
