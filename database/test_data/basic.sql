insert into "user" (id, username, email, display_name, password_hash, user_type) values
(1, 'admin', 'admin@admin.com', 'ADMIN', 'abc', 'admin'),
(2, 'mod', 'mod@mod.com', 'MOD', 'abc', 'moderator'),
(3, 'foo', 'foo@foo.com', 'FOO', 'abc', 'normal'),
(4, 'bar', 'bar@bar.com', 'BAR', 'abc', 'normal')
;

insert into "position" (id, creator_user_id, position_category_id, location_id, statement, status) values
(1, 3, 2, 0, 'vote sideshow bob for mayor', 'active'),
(2, 3, 2, 0, 'mayor quimby is bad', 'active'),
(3, 3, 2, 0, 'homers should pay the homers tax', 'inactive'),
(4, 3, 2, 0, 'i love mayor grimby', 'active'),
(5, 4, 2, 0, 'the bear tax is outrageous', 'active'),
(6, 4, 2, 0, 'taxes are high because of immigants', 'active'),
(7, 4, 2, 0, 'the simpsons is a bad show', 'removed')
;

insert into "user_position" (id, user_id, position_id, result) values
(1, 4, 1, 'chat'),
(2, 4, 2, 'dislike'),
(3, 3, 4, 'chat')
;

insert into "chat_log" (id, position_id, creator_user_id, responder_user_id, status) values
(1, 1, 3, 4, 'active'),
(2, 2, 3, 4, 'pending'),
(3, 4, 4, 3, 'active')
;

insert into "chat_log_message" (id, chat_log_id, user_id, message) values
(1, 1, 4, 'sideshow bob is bad, what are you thinking'),
(2, 1, 3, 'calm down and lets talk about this'),
(3, 1, 4, 'fine'),
(4, 3, 3, 'the bear tax is good!')
;