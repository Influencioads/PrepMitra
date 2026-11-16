-- Runs once when the Docker database is first created, connected to POSTGRES_DB as POSTGRES_USER.
-- pgvector in the main database, plus a separate database for the automated test suite.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE DATABASE prepmitra_test OWNER CURRENT_USER;
\connect prepmitra_test
CREATE EXTENSION IF NOT EXISTS vector;
