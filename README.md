# FileBot Xattr Metadata Scanners & Plug-ins

Enhance Plex with support for [FileBot Xattr Metadata](https://www.filebot.net/forums/viewtopic.php?f=3&t=324).


## Install

1. Download [plex-agents.zip](https://github.com/filebot/plex-agents/archive/master.zip)
2. Copy the `Scanners` and `Plug-ins` folders into the [`Plex Media Server`](https://support.plex.tv/articles/202915258-where-is-the-plex-media-server-data-directory-located/) data directory
3. Restart Plex
4. Configure `Advanced ➔ Scanner` for each library and select `FileBot Xattr Scanner`
5. Configure `Settings ➔ Agents` and enable `FileBot Xattr Metadata` and move it to the top for each primary agent


## FileBot Xattr Metadata Scanner

The `FileBot Xattr Scanner` will read `name / year / season / episode / etc` from xattr metadata instead of guessing and parsing information from the file path. This scanner will greatly enhance primary agents such as `Plex Movie` or `TheTVDB`, regardless of whether files are named according to [`{plex}`](https://www.filebot.net/forums/viewtopic.php?f=5&t=4116) standards or not. Files without xattr metadata will be ignored.


## FileBot Xattr Metadata Agent

The `FileBot Xattr Metadata` secondary agent can contribute `title / airdate / etc` from xattr metadata instantly, to improve your browsing experience while the primary agent is still busy in the background retrieving complete movie and episode information and artwork.
