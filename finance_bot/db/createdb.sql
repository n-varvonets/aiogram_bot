create table budget(
    id integer primary key autoincrement,
    total_income integer,
    month_planing_base_expenses integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "продукти", true, "іжа, еда, атб, таврія, таврия, ева, eva, котикам, звірі, півко"),
    ("regular_bills", "щомісяна виплата", true, "квартира, дом, інет, інтернет, inet, tenet, tennet, прибиральниця, виплата, поповнення"),
    ("transport", "транспорт", true, "таксі, такси, маршрутка, метро, автобус"),
    ("phone", "телефон та інтернет", true, "телефон, лайф, связь, моб, тел, ітернет, tenet, tennet, інет, тенет"),
    ("my_treats", "власне задоволення", false, "кава, coffee, кофе, паб, бар, мак, піцца, піца, пицца, суши, кіно, футбол, спортзал, теніс, пк"),
    ("books", "книги", false, "книга, book, литература, литра, лит-ра"),
    ("lent_debt", "займи", false, "дав у борг, взяв у борг, борг, взяв борг, дав борг, борг, заняв"),
    ("subscriptions", "підписки", false, "підписка, підписка на канал, донат, зсу, амазон, aws, Слава Україні, ігра"),
    ("other", "інше", false, "_");

insert into budget(total_income, month_planing_base_expenses) values (0, 0);
