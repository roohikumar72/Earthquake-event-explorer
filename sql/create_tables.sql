DROP TABLE IF EXISTS earthquakes;

CREATE TABLE earthquakes (
    id TEXT PRIMARY KEY,
    time INTEGER,
    latitude REAL,
    longitude REAL,
    depth REAL,
    magnitude REAL,
    place TEXT
);
