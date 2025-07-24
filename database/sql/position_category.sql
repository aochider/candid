create table "position_category" (
	id bigserial primary key,
	label varchar(32) unique not null
);

insert into "position_category" (id, label) values
(1, 'foo'),
(2, 'bar'),
(3, 'baz')
;