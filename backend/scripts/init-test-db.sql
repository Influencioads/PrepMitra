-- Separate database for the automated test suite (dropped/recreated schema per test run).
CREATE DATABASE prepmitra_test OWNER prepmitra;
\connect prepmitra
CREATE EXTENSION IF NOT EXISTS vector;
\connect prepmitra_test
CREATE EXTENSION IF NOT EXISTS vector;
