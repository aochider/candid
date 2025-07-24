create table "user_position" (
	id bigserial primary key,
	user_id bigint not null,
	position_id bigint not null,
	result varchar(16) not null
);