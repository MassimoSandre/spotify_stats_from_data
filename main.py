from spotifystats import SpotifyStats

s = SpotifyStats()

s.load_data()
print(s.no_tracks_by_interval())