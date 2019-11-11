-- :name delete_by_id_playlist
-- :result :n
DELETE FROM playlists
WHERE id = :id
