create table "user_position_category" (
	id bigserial primary key,
	user_id bigint not null,
	position_category_id bigint not null,
	priority integer not null
);