-- :name fetch_track :one
SELECT description FROM tracksdesc WHERE username = :username and trackurl=:trackurl;
