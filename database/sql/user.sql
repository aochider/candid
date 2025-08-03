create table "user" (
	id bigserial primary key,
	username varchar(32) unique not null,
	email varchar(120) unique not null,
	display_name varchar(32) unique not null,
	password_hash varchar(64) not null,
	role varchar(16) not null,
	created_time timestamp without time zone default current_timestamp,
	-- TODO probably want to verify the email
	verified_time timestamp without time zone default current_timestamp
);