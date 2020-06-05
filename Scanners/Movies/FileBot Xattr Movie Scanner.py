import Media, VideoFiles

from filebot import *

VideoFiles.ignore_dirs.remove('bdmv')
excl_dirs = ['backup', 'clipinf', 'playlist']
VideoFiles.ignore_dirs.extend(excl_dirs)

def Scan(path, files, mediaList, subdirs, language=None, root=None):
  VideoFiles.Scan(path, files, mediaList, subdirs, root)

  # require alphabetic order
  files.sort()

  # group movie parts as they come in sequence
  prev_media = None
  prev_part_index = None

  for file in files:
    attr = xattr_metadata(file)
    if attr is None:
      continue

    guid = movie_guid(attr)
    if guid is None:
      continue

    print("[XATTR] %s | %s" % (guid, attr))

    part_index = movie_part_index(attr)
    if prev_part_index and part_index and prev_part_index + 1 == part_index and prev_media.guid == guid:
      prev_part_index = part_index
      prev_media.parts.append(file)
      print("[MEDIA] %s | Part %s" % (prev_media, part_index))
      continue

    media = Media.Movie(
      movie_name(attr).encode('utf-8'),  # use str since Plex doesn't like unicode strings
      movie_year(attr)
    )
    media.guid = guid.encode('utf-8')

    original_filename = xattr_filename(file)
    if original_filename:
      media.source = VideoFiles.RetrieveSource(original_filename.encode('utf-8'))

    media.parts.append(file)
    mediaList.append(media)

    if part_index == 1:
      prev_media = media
      prev_part_index = 1
    else:
      prev_media = None
      prev_part_index = None

    print("[MEDIA] %s | %s | %s | %s" % (media, media.year, media.released_at, media.source))
