create database blog character set 'utf8';

use blog;

create table blog_role (
  id int(11) not null auto_increment,
  role varchar(16) not null,
  permission varchar(16) not null,
  primary key (id)
) ;


create table blog_user (
  id int(11) not null auto_increment,
  username varchar(32) not null,
  password varchar(32) not null,
  roles_id int(11) not null,
  primary key (id),
  foreign key (roles_id) references blog_role (id)
) ;

create table blog_article (
  id int(11) not null auto_increment,
  article longtext not null,
  belong_id int(11) not null,
  primary key (id),
  foreign key (belong_id) references blog_user (id)
);