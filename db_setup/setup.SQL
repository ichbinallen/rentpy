CREATE SCHEMA IF NOT EXISTS rentpy AUTHORIZATION rentpy;

CREATE TABLE IF NOT EXISTS forsale (
	scrape_id SERIAL,
	url TEXT,
	street_address VARCHAR,
	city VARCHAR,
	state VARCHAR,
	zipcode VARCHAR(5),
	num_beds INTEGER,
	num_baths NUMERIC,
	sq_ft NUMERIC,
	listprice NUMERIC,
	listing_text TEXT
);
