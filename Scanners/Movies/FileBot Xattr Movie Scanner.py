import Media, VideoFiles

from filebot import *


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  VideoFiles.Scan(path, files, mediaList, subdirs, root)

  for file in files:
    attr = xattr_metadata(file)
    if attr is None:
      continue

    guid = movie_guid(attr)
    if guid is None:
      continue

    movie = Media.Movie(
      str(movie_name(attr)),  # use str() since Plex doesn't like unicode strings
      movie_year(attr)
    )
    movie.guid = guid

    original_filename = xattr_filename(file)
    if original_filename:
      movie.source = VideoFiles.RetrieveSource(original_filename)

    movie.parts.append(file)
    mediaList.append(movie)

    print("[XATTR] %s | %s | %s" % (movie, movie.guid, movie.source))
