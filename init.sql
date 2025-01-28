/*
The vigil user for the bot and web dashboard.
You must set the same password as in `docker-compose.yml`.
*/
CREATE USER vigil WITH PASSWORD '...';
CREATE DATABASE bot;
ALTER DATABASE bot OWNER TO vigil;

/*
The nginx user for the proxy server.
You must set the same password as in `docker-compose.yml`.
*/
CREATE USER nginx WITH PASSWORD '...';
CREATE DATABASE npm;
ALTER DATABASE npm OWNER TO nginx;
