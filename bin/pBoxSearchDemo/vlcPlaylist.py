import xml.etree.ElementTree as xml

# Create an xml playlist file for VLC (xspf)
class Playlist:

    # Define the basic tree structure
    def __init__(self):
        self.playlist = xml.Element('playlist')
        self.tree = xml.ElementTree(self.playlist)
        self.playlist.set('xmlns', 'http://xspf.org/ns/0/')
        self.playlist.set('xmlns:vlc', 'http://www.videolan.org/vlc/playlist/ns/0/')
        self.playlist.set('version', '1')

        self.title = xml.Element('title')
        self.playlist.append(self.title)
        self.title.text = 'Playlist'

        self.trackList = xml.Element('trackList')
        self.playlist.append(self.trackList)

    # Add tracks to xml tree (within trackList)
    def add_track(self, url, dur, ttl):
        track = xml.Element('track')
        location = xml.Element('location')
        location.text = url
        duration = xml.Element('duration')
        duration.text = dur
        title = xml.Element('title')
        title.text = ttl
        track.append(location)
        track.append(duration)
        track.append(title)
        self.trackList.append(track)

    # Write the complete playlist with tracks to file.
    def save_playlist(self, file):
        with open(file, 'w') as pl:
            pl.write(xml.tostring(self.playlist).decode('utf-8'))
