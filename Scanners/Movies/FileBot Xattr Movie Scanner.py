import Media, VideoFiles

from filebot import *


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  VideoFiles.Scan(path, files, mediaList, subdirs, root)

  # require alphabetic order
  files.sort()

  # group movie parts as they come in sequence
  prev_movie = None
  prev_part_index = None

  for file in files:
    attr = xattr_metadata(file)
    if attr is None:
      continue

    guid = movie_guid(attr)
    if guid is None:
      continue

    part_index = movie_part_index(attr)
    if prev_part_index and part_index and prev_part_index + 1 == part_index and prev_movie.guid == guid:
      prev_part_index = part_index
      prev_movie.parts.append(file)
      print("[XATTR] %s | Part %s | %s" % (prev_movie, part_index, attr))
      continue


    movie = Media.Movie(
      movie_name(attr).encode('utf-8'),  # use str since Plex doesn't like unicode strings
      movie_year(attr)
    )
    movie.guid = guid

    original_filename = xattr_filename(file)
    if original_filename:
      movie.source = VideoFiles.RetrieveSource(original_filename)

    movie.parts.append(file)
    mediaList.append(movie)

    if part_index == 1:
      prev_movie = movie
      prev_part_index = 1
    else:
      prev_movie = None
      prev_part_index = None

    print("[XATTR] %s | %s | %s | %s" % (movie, movie.guid, movie.source, attr))
