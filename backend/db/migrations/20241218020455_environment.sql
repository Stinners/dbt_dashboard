-- migrate:up
CREATE TABLE IF NOT EXISTS environment (
    environment_id integer primary key,
    dbt_id integer not null,
    name varchar not null,
    type varchar not null, 
    repo_name varchar not null,
    project_id integer not null,

    foreign key (project_id) references project(project_id),
    unique(dbt_id)
);


-- migrate:down
drop table if exists environment;

