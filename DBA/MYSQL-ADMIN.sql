use information_schema;

select table_name, table_schema, table_catalog, table_type from TABLES -- list tables
   where TABLE_SCHEMA = 'mysql'
   order by table_schema,table_name;

-- LIST TABLES IN A SCHEMA
SHOW TABLES in mysql;
select table_name as tables_in_mysql from TABLES where TABLE_SCHEMA = 'mysql' order by table_name;

select table_schema, table_name,table_rows from tables order by table_schema, table_name;
select table_schema, table_name,table_rows from tables where table_schema = '' order  by table_schema, table_name;

select * from user_privileges order by grantee,privilege_type;
-- LIST FILES
select file_name,TOTAL_EXTENTS,EXTENT_SIZE,(TOTAL_EXTENTS * EXTENT_SIZE) from files order by file_name;

-- DESCRIBE COLUMNS
select column_name, table_name, data_type, ordinal_position  from COLUMNS where table_name = 'COLUMNS';
select table_name, column_name,column_type,data_type,privileges from COLUMNS where table_name = 'COLUMNS' order by column_name;
-- DESCRIBE TABLES
select column_name, table_name, data_type, ordinal_position  from COLUMNS where table_name = 'TABLES';
-- DESCRIBE USER
select column_name, table_name, data_type, ordinal_position  from COLUMNS where table_name = 'user';
select user,host,account_locked as LOCKED,password_lifetime as PASSLIFE,super_priv as SUPER,shutdown_priv as SDOWN,show_db_priv as SHOWDB from mysql.user order by host,user;
select * from mysql.user;


-- DATABASES
create database example_db;
create user 'dbmgr'@'%' identified by 'password';
grant all on example_db.* to 'dbmgr'@'%';

INSERT INTO `example_db`.`breads` (`bread_name`, `bread_description`) VALUES ('PUMPERNICKEL', 'PUMPERNICKEL / a flavorful rye bread');
select bread_id as ID, bread_name as NAME, bread_description as DESCR from breads;

create database db_example;
create user 'springuser'@'%' identified by 'springuser';
grant all on db_example.* to 'springuser'@'%';

-- WORDLE
create trigger check_word_length
    before insert on wordle
    for each row
    call check_word_length();

delimiter //
CREATE PROCEDURE `check_word_length` (in the_word varchar(5))
BEGIN
   if (character_length(the_word) != 5) then signal sqlstate '81020'
      set message_text = 'Wordle word length must be exactly 5 characters.';
end if;
END //
delimiter ;
DROP PROCEDURE `check_word_length`;
create trigger `verify_word`
    before insert on wordle for each row call check_word_length(NEW.word_value);
drop trigger verify_word;

