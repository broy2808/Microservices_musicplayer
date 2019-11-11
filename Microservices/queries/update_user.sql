-- :name update_user :insert
UPDATE users set password=:password where username=:username
