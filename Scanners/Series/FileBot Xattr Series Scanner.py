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
    multi_episode_count = len(episodes)

    for i, attr in enumerate(episodes):
      special = episode_special_number(attr)

      episode = Media.Episode(
        str(series_name(attr)),
        0 if special else episode_season_number(attr),
        special if special else episode_number(attr),
        str(episode_title(attr)),
        series_year(attr)
      )

      date = episode_date(attr)
      if date:
        episode.released_at = date.strftime('%Y-%m-%d')

      if (multi_episode_count > 1):
        episode.display_offset = (i * 100) / multi_episode_count

      original_filename = xattr_filename(file)
      if original_filename:
        episode.source = VideoFiles.RetrieveSource(original_filename)

      episode.parts.append(file)
      mediaList.append(episode)

      print("[XATTR] %s | %s | %s | %s | %s" % (episode, episode.year, episode.released_at, episode.source, attr))
