-- migrate:up
create table if not exists project (
    project_id integer primary key,
    dbt_id integer not null, 
    name varchar not null,
    
    unique(dbt_id)
);

-- migrate:down
drop table if exists project;

