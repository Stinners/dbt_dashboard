CREATE TABLE IF NOT EXISTS "schema_migrations" (version varchar(128) primary key);
CREATE TABLE project (
    project_id integer primary key,
    dbt_id integer not null,
    name varchar not null,

    unique(dbt_id)
);
CREATE TABLE environment (
    environment_id integer primary key,
    dbt_id integer not null,
    name varchar not null,
    type varchar not null,
    repo_name varchar not null,
    project_id integer not null,

    foreign key (project_id) references project(project_id),
    unique(dbt_id)
);
CREATE TABLE job (
    job_id integer primary key,
    dbt_id integer not null,
    name varchar,
    project_id integer not null,
    environment_id integer not null,

    foreign key(project_id) references project(project_id),
    foreign key(environment_id) references environment(environment_id),
    unique(dbt_id)
);
CREATE TABLE run (
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
);
-- Dbmate schema migrations
INSERT INTO "schema_migrations" (version) VALUES
  ('20241218020200'),
  ('20241218020455'),
  ('20241218021053'),
  ('20241218021428');
