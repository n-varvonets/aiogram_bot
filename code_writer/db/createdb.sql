create table users(
    id integer NOT NULL primary key  autoincrement,
    user_id integer NOT NULL,
    nickname varchar(60),
    time_sub datetime,
    sign_up varchar(255) DEFAULT  setnickname
);
-- time_sub - время когда юзер подписался
--sign_up - этап регистрации пользователя
--uid - айди самого юзера, которое будет браться из данных нашего ползьователя


