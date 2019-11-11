-- :name get_playlist_by_user :many
SELECT * FROM playlists
WHERE username = :username
