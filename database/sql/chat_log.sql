create table "chat_log" (
	id bigserial primary key,
	position_id bigint not null,
	creator_user_id bigint not null,
	responder_user_id bigint not null,
	message varchar(256) not null,
	message_time timestamp without time zone default current_timestamp
);