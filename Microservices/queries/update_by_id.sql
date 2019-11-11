-- :name update_by_id :affected
UPDATE tracks set track_title= :track_title
WHERE id = :id
