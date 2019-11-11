-- :name create_user :insert
INSERT INTO users(username,full_name,password,email,homeurl)
VALUES(:username, :full_name, :password, :email,:homeurl)
