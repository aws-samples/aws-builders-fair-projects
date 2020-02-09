CREATE TABLE IF NOT EXISTS media_files (
	id integer PRIMARY KEY,
	file_name text NOT NULL,
	md5_hash text,
	file_type text,
	current_state text,
	last_updated integer,
	last_updated_dt text
);

INSERT INTO media_files(file_name,md5_hash,file_type,current_state,last_updated,last_updated_dt)
	VALUES(?,?,?,?,?,?)

CREATE TABLE IF NOT EXISTS local_settings (
	id integer PRIMARY KEY,
	setting_name text NOT NULL,
	setting_value text NOT NULL,
	last_updated integer,
	last_updated_dt text
);
