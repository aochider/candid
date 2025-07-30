create table "chat_log" (
	id bigserial primary key,
	position_id bigint not null,
	responder_user_id bigint not null,
	chat_log_time timestamp without time zone default current_timestamp,
	status varchar(16) not null
);