use SciamIndexDB;
use SciamTestDB;

select * from articles order by article_year desc, article_month desc, article_id asc;
select * from articles where article_category like '%Technology%' order by article_year desc, article_month desc, article_id;
select * from articles where article_author like '%Pogue%' order by article_year desc, article_month desc, article_id;
select * from articles where article_title like '%Lemur%' order by article_year desc, article_month desc, article_id;
select * from articles where article_synopsis like '%bees%' order by article_year desc, article_month desc, article_id;
select * from articles order by article_year desc, article_month desc, article_id;

select * from articles where article_month = 11 and article_year = 2022	 order by article_year, article_month, article_id;
select * from articles where article_year = 2020;
select * from articles where article_month = 6 and article_year = 2016 order by article_title;
select * from articles where article_id = 18;
select count(*) from articles;

alter table articles add constraint article_titleuk unique (article_title, article_month, article_year);
alter table articles drop constraint article_titleuk;
alter table articles rename column article_category to article_topic;

update articles set article_author = 'Scientific American\'s Board of Editors' where article_author = 'The Editors of Scientific American';
update articles set article_category = 'The Science of Health' where article_category = 'Science of Health';
commit;

create index article_category_index on articles(article_category);

-- WORDLE
insert into wordle (word_value) values ('short');
select * from wordle where (select substring(word_value,5,1)= 'E') order by word_value;
select * from wordle order by word_value;


SHOW VARIABLES LIKE "sql_safe_updates";
show variables like '%limit%';
