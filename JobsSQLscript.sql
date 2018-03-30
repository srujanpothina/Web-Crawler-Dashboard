select * from skills
drop table skills
create table skills(
id int identity(1,1) primary key,
skill_name varchar(100) unique
)

select * from skills
insert into skills(skill_name) values('java')
insert into skills(skill_name) values('ruby')
insert into skills(skill_name) values('nodejs')
insert into skills(skill_name) values('c#')
insert into skills(skill_name) values('c++')
insert into skills(skill_name) values('tsql')
insert into skills(skill_name) values('.net')
insert into skills(skill_name) values('python')
insert into skills(skill_name) values('algorithm')
insert into skills(skill_name) values('jsp')
insert into skills(skill_name) values('j2ee')
insert into skills(skill_name) values('t-sql')
insert into skills(skill_name) values('ios')
insert into skills(skill_name) values('android')
insert into skills(skill_name) values('javascript')
insert into skills(skill_name) values('rest')
insert into skills(skill_name) values('soap')
insert into skills(skill_name) values('servicenow')
insert into skills(skill_name) values('hybris')
insert into skills(skill_name) values('websphere')
insert into skills(skill_name) values('angularjs')
insert into skills(skill_name) values('aws')

select max(id) from skills
select * from jobs

create table skill_mapping(
skill_id int not null,
job_id int not null,
constraint fk_Id_skill foreign key(skill_id) references skills(id) on update cascade on delete cascade,
constraint fk_bId_job foreign key(job_id) references Jobs(id) on update cascade on delete cascade
)
drop table skill_mapping

-- 'Job_Title','URL','Job Type','Company','City','State','Minimum Salary','Maximum Salary','Skills'
select * from jobs
truncate table jobs

create table Jobs(
id int identity(1,1) primary key,
job_title varchar(200) not null,
job_type varchar(200) not null,
company varchar(100) not null,
city varchar(100) not null,
state varchar(100) not null,
minimum_salary int not null,
maximum_salary int not null ,
url varchar(350) not null,
skills varchar(350) not null
)
drop table jobs
-- To populate a job
insert into jobs([job_title],[job_type],[company],[city],[state],[minimun_salary],[maximum_salary],[url]) values