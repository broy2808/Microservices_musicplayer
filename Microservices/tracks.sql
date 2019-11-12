
DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks
(
    id GUID primary key,
    track_title VARCHAR,
    album_title VARCHAR,
    artist VARCHAR,
    track_length VARCHAR,
    URL_media VARCHAR,
    URL_artwork VARCHAR
);
