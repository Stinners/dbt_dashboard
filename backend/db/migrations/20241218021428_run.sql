-- migrate:up
create table if not exists run (
    run_id integer primary key,
    dbt_id integer not null,
    environment_id integer not null, 
    project_id integer not null, 
    job_id integer not null,
    git_branch varchar, 
    git_hash varchar,
    started_at timestamp not null,
    finished_at timestamp,
    is_error boolean not null,
    duration varchar,

    foreign key(job_id) references job(job_id),
    foreign key(project_id) references project(project_id),
    foreign key(environment_id) references environment(environment_id),
    unique(dbt_id)
)

-- migrate:down
drop table if exists run;
