insert into "user" (username, email, display_name, password_hash, user_type) values
('admin', 'admin@admin.com', 'ADMIN', 'abc', 'admin'),
('mod', 'mod@mod.com', 'MOD', 'abc', 'moderator'),
('foo', 'foo@foo.com', 'FOO', 'abc', 'normal'),
('bar', 'bar@bar.com', 'BAR', 'abc', 'normal')
;

insert into "position" (creator_user_id, position_category_id, location_id, statement, status) values
(3, 2, 0, 'vote sideshow bob for mayor', 'active'),
(3, 2, 0, 'mayor quimby is bad', 'active'),
(3, 2, 0, 'homers should pay the homers tax', 'inactive'),
(3, 2, 0, 'i love mayor grimby', 'active'),
(4, 2, 0, 'the bear tax is outrageous', 'active'),
(4, 2, 0, 'taxes are high because of immigants', 'active'),
(4, 2, 0, 'the simpsons is a bad show', 'removed')
;

insert into "user_position" (user_id, position_id, result) values
(4, 1, 'chat'),
(4, 2, 'dislike'),
(3, 4, 'chat')
;

insert into "chat_log" (position_id, responder_user_id, status) values
(1, 4, 'active'),
(2, 4, 'pending'),
(4, 3, 'active')
;

insert into "chat_log_message" (chat_log_id, user_id, message) values
(1, 4, 'sideshow bob is bad, what are you thinking'),
(1, 3, 'calm down and lets talk about this'),
(1, 4, 'fine'),
(3, 3, 'the bear tax is good!')
;