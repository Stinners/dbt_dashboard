-- migrate:up
create table if not exists job (
    job_id integer primary key,
    dbt_id integer not null, 
    name varchar,
    project_id integer not null,
    environment_id integer not null,

    foreign key(project_id) references project(project_id),
    foreign key(environment_id) references environment(environment_id),
    unique(dbt_id)
);


-- migrate:down
drop table if exists job;

