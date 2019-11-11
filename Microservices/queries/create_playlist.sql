-- :name create_playlist :insert
INSERT INTO playlists(playlist_title, URL_list, username, description)
VALUES(:playlist_title, :URL_list, :username, :description)
