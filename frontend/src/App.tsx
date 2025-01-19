import { Component, createResource, Show } from 'solid-js';
import { JobCardData, renderCards } from './JobCard';
import NavBar from './NavBar';

type Job = {
    job_id: number,
    dbt_id: number,
    project_name: string,
    enviornment_name: string,
    name: string,
}

type Run = {
    dbt_id: number,
    environment_name: string,
    project_name: string,
    job_name: string,
    git_branch?: string,
    git_hash?: string,
    started_at: string,
    finished_at?: string,
    is_error: boolean,
    duration: string,
}

// TODO This should probably be returned from a database query
// rather than assembled on the frontent
const initJobCardData = (job: Job) => {
    return {
        "job_name": job.name,
        "project_name": job.project_name,
        "environment_name": job.enviornment_name,
        "has_run": false,
    };
}

const addRunData = (data: JobCardData, run: Run) => {
    data.has_run = true;
    data.git_branch = run.git_branch;
    data.git_hash = run.git_hash;
    data.started_at = run.started_at;
    data.finished_at = run.finished_at;
    data.is_error = run.is_error;
    data.duration = run.duration;
}

const fetchJobs = async (): Promise<Job[]> => {
    const response = await fetch("api/jobs")
    return await response.json();
}

const fetchRuns = async (): Promise<Run[]> => {
    const response = await fetch("api/runs")
    return await response.json();
}

const matchJobsWithRuns = (jobs: Job[], runs: Run[]) => {
    let enrichedJobs = [];
    // For now just do a nested loop left-join
    for (let job of jobs) {
        let jobData = initJobCardData(job);
        for (let run of runs) {
            if (run.job_name === job.name) {
                addRunData(jobData, run);
                break;
            }
        }
        enrichedJobs.push(jobData)
    }
    return enrichedJobs
}


const App: Component = () => {
    const [ jobs ] = createResource(fetchJobs);
    const [ runs ] = createResource(fetchRuns);

    return (
      <div class='container'>
          <NavBar/>

          <main class='card-holder'>
              <Show when={jobs() && runs()}>
                  {renderCards(matchJobsWithRuns(jobs()!, runs()!))}
              </Show>
          </main>
      </div>
    );
};

export default App;
