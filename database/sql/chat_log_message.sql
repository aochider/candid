create table "chat_log_message" (
	id bigserial primary key,
	chat_log_id bigint not null,
	user_id bigint null,
	message varchar(256) not null,
	message_time timestamp without time zone default current_timestamp
);