-- $ sqlite3 users.db < sqlite.sql
--PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracksdesc;
CREATE TABLE tracksdesc(
    trackid INTEGER primary key NOT NULL,
    trackurl VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY(username) REFERENCES users(username),
    UNIQUE(trackurl,description,username)
);
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co','My Favourite Track1','Suramya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co1','My Favourite Track1','Suramya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co2','My Favourite Track1','Suramya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co3','My Favourite Track1','Suramya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Jowalton');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co','My Favourite Track2','Bony');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co1','My Favourite Track2','Bony');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co2','My Favourite Track2','Bony');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co3','My Favourite Track2','Bony');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co','My Favourite Track3','Brandon');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co1','My Favourite Track3','Brandon');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co2','My Favourite Track3','Brandon');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co3','My Favourite Track3','Brandon');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co','My Favourite Track4','Shreya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co1','My Favourite Track4','Shreya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co2','My Favourite Track4','Shreya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co3','My Favourite Track4','Shreya');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co','My Favourite Track5','Sudhir');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co1','My Favourite Track5','Sudhir');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co2','My Favourite Track5','Sudhir');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('night.co3','My Favourite Track5','Sudhir');


DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username VARCHAR(255) primary key NOT NULL,
    full_name VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    homeurl TEXT,
    UNIQUE(full_name,password,email)
);

INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Suramya', 'Suramya Singh', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'ssingh@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Bony', 'Bony Roy', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'broy@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Conniewillis', 'Connie Willis', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Conniewillis@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Brandon', 'Brandon Tomich', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'btomich@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Katewilhelm', 'Kate Wilhelm', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Katewilhelm@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Shreya', 'Shreya Singh', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'shreyasingh@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Sudhir', 'Sudhir Singh', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'sudhirsingh@gmail.com','www.abc.com');



DROP TABLE IF EXISTS playlists;
CREATE TABLE playlists
(
    id INTEGER primary key,
    playlist_title VARCHAR,
    URL_list VARCHAR,
    username VARCHAR,
    description VARCHAR
);



INSERT INTO playlists(playlist_title,URL_list,username,description) VALUES("MyPlaylist", '["Track1","Track2","Track3","Track4"]', "Brandon","My Favourite Track1");
INSERT INTO playlists(playlist_title,URL_list,username,description) VALUES("MyPlaylist", '["Track1","Track2","Track3","Track4"]', "Suramya","My Favourite Track2");
INSERT INTO playlists(playlist_title,URL_list,username,description) VALUES("MyPlaylist", '["Track1","Track2","Track3","Track4"]', "Bony","My Favourite Track3");
INSERT INTO playlists(playlist_title,URL_list,username,description) VALUES("MyPlaylist", '["Track1","Track2","Track3","Track4"]', "Shreya","My Favourite Track4");
INSERT INTO playlists(playlist_title,URL_list,username,description) VALUES("MyPlaylist", '["Track1","Track2","Track3","Track4"]', "Sudhir","My Favourite Track5");




DROP TABLE IF EXISTS playlist_tracks;
CREATE table playlist_tracks
(
  playlist_id INT,
  trackurl VARCHAR
);

INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(1, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbadf");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(1, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbabc");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(1, "http://127.0.0.1:9002/recources/tracks/9944dd14-499a-4d64-8a78-62cc35205449");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(1, "http://127.0.0.1:9002/recources/tracks/1000dd14-499a-4d64-8a78-62cc35205455");

INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(2, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbadf");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(2, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbabc");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(2, "http://127.0.0.1:9002/recources/tracks/9944dd14-499a-4d64-8a78-62cc35205449");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(2, "http://127.0.0.1:9002/recources/tracks/1000dd14-499a-4d64-8a78-62cc35205455");

INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(3, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbadf");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(3, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbabc");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(3, "http://127.0.0.1:9002/recources/tracks/9944dd14-499a-4d64-8a78-62cc35205449");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(3, "http://127.0.0.1:9002/recources/tracks/1000dd14-499a-4d64-8a78-62cc35205455");

INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(4, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbadf");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(4, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbabc");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(4, "http://127.0.0.1:9002/recources/tracks/9944dd14-499a-4d64-8a78-62cc35205449");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(4, "http://127.0.0.1:9002/recources/tracks/1000dd14-499a-4d64-8a78-62cc35205455");

INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(5, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbadf");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(5, "http://127.0.0.1:9002/recources/tracks/805944b7-b211-4e26-b74e-6c75d92cbabc");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(5, "http://127.0.0.1:9002/recources/tracks/9944dd14-499a-4d64-8a78-62cc35205449");
INSERT INTO playlist_tracks(playlist_id, trackurl) VALUES(5, "http://127.0.0.1:9002/recources/tracks/1000dd14-499a-4d64-8a78-62cc35205455");
