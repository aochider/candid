create table "kudos" (
	id bigserial primary key,
	sender_user_id bigint not null,
	receiver_user_id bigint not null,
	chat_log_id bigint not null
);