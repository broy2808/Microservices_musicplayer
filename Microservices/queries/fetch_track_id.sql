-- :name fetch_track_id :one
SELECT trackid FROM tracksdesc WHERE username = :username and trackurl=:trackurl;
