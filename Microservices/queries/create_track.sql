-- :name create_track :insert
INSERT INTO tracks(track_title, album_title, artist, track_length, URL_media, URL_artwork)
VALUES(:track_title, :album_title, :artist, :track_length, :URL_media, :URL_artwork)
