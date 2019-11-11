-- :name search_by_id_playlists :one
SELECT * FROM playlists
WHERE id = :id
