-- :name delete_user
-- :result :n
DELETE FROM users WHERE username = :username;
