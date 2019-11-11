-- :name update_by_id_playlist :affected
UPDATE playlists set playlist_title= :playlist_title
WHERE id = :id
