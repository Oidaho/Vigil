CREATE USER vigil WITH PASSWORD '...';
CREATE DATABASE bot;
ALTER DATABASE bot OWNER TO vigil;

CREATE USER nginx WITH PASSWORD '...';
CREATE DATABASE npm;
ALTER DATABASE npm OWNER TO nginx;
