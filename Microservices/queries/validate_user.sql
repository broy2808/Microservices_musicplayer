-- :name validate_user :one
SELECT username FROM users WHERE username = :username and password=:password;
