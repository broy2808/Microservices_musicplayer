-- :name user_by_id :one
SELECT username,full_name,email,homeurl FROM users
WHERE username = :id;
