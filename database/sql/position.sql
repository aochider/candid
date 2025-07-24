create table "position" (
	id bigserial primary key,
	creator_user_id bigint not null,
	position_category_id bigint not null,
	location_id bigint not null,
	statement varchar(512) not null,
	created_time timestamp without time zone default current_timestamp,
	status varchar(16) not null
);