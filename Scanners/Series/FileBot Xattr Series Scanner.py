import Media, VideoFiles

from filebot import *


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  VideoFiles.Scan(path, files, mediaList, subdirs, root)

  for file in files:
    attr = xattr_metadata(file)
    if attr is None:
      continue

    # single episode | multi episode
    episodes = list_episodes(attr)
    episode_count = len(episodes)

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

      if (episode_count > 1):
        episode.display_offset = (i * 100) / episode_count

      original_filename = xattr_filename(file)
      if original_filename:
        episode.source = VideoFiles.RetrieveSource(original_filename)

      episode.parts.append(file)
      mediaList.append(episode)

      print("[XATTR] %s | %s | %s | %s" % (episode, episode.year, episode.released_at, episode.source))
