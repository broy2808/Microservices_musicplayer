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
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Aleckie');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Jowalton');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl2','My Favourite Track2','Aleckie');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl2','My Favourite Track2','Jowalton');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Conniewillis');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Davidbrin');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Katewilhelm');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Williamgibson');
INSERT INTO tracksdesc(trackurl,description,username) VALUES('trackurl1','My Favourite Track1','Nealwalton');

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username VARCHAR(255) primary key NOT NULL,
    full_name VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    homeurl TEXT,
    UNIQUE(full_name,password,email)
);

INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Aleckie', 'Ann Leckie', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Aleckie@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Jowalton', 'Jo Walton', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'JoWalton@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Conniewillis', 'Connie Willis', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Conniewillis@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Davidbrin', 'David Brin', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Davidbrin@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Katewilhelm', 'Kate Wilhelm', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Katewilhelm@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Williamgibson', 'William Gibsone', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Williamgibson@gmail.com','www.abc.com');
INSERT INTO users(username,full_name,password,email,homeurl) VALUES('Nealwalton', 'Neal Walton', '$2b$12$DbmIZ/a5LByoJHgFItyZCeIEHz9koaXCGjwc/fLJAPp5G6jmQvg4u', 'Neal@gmail.com','www.abc.com');



DROP TABLE IF EXISTS playlists;
CREATE TABLE playlists
(
    id INTEGER primary key,
    playlist_title VARCHAR,
    URL_list VARCHAR,
    username VARCHAR,
    description VARCHAR
);

INSERT INTO playlists(playlist_title,URL_list,username,description) VALUES("MyPlaylist", '["Track1","Track2","Track3","Track4"]', "Brandon","This Track is good");
