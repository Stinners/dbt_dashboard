import dayjs from "dayjs"
import duration from "dayjs/plugin/duration";
import relativeTime from "dayjs/plugin/relativeTime";
import { Component, For, Show } from 'solid-js';

dayjs.extend(duration);
dayjs.extend(relativeTime);

export type JobCardData = {
    // Job data 
    job_name: string,
    project_name: string,
    environment_name: string,
    has_run: boolean,

    // Run data - may be missing 
    git_branch?: string,
    git_hash?: string,
    started_at?: string,
    finished_at?: string,
    is_error?: boolean,
    duration?: string
}

const durationParts: [string, (duration.Duration) => number][]  = [
    ["years", dur => dur.years()],
    ["months", dur => dur.months()],
    ["days", dur => dur.months()],
    ["hours", dur => dur.months()],
    ["minutes", dur => dur.months()],
    ["seconds", dur => dur.months()],
]

// TODO Display just he two longest components of the duration
const formatDayJsDuration = (dur: duration.Duration, includeAgo = false) => {
    if (includeAgo) {
        return dur.format("H [hours] m [minutes] [ago]");
    } else {
        return dur.format("H [hours] m [minutes]");
    }

}

const formatStartTime = (timeStr?: string): string => {
    if (timeStr) {
       let datetime = dayjs(timeStr);
       let diffInMilliseconds = dayjs().diff(datetime);
       let duration = dayjs.duration(diffInMilliseconds);
       return formatDayJsDuration(duration);
    } else {
        return "---";
    }
}

const durationRE = /([0-9]+):([0-9]+):([0-9]+)/
const formatDuration = (durationStr?: string): string => {
    if (durationStr) {
        let match = durationStr.match(durationRE);

        if (!match) {
            return "---"
        }

        let hours  = parseInt(match[1]);
        let minutes = parseInt(match[2]);
        let seconds = parseInt(match[3]);

        let duration = dayjs.duration({hours, minutes, seconds});

        return formatDayJsDuration(duration);
    } else {
        return "---";
    }
    
}


const JobCard: Component<JobCardData> = (card: JobCardData) => {

    let color = 'bg-success';
    if (!card.has_run) {
        color = 'bg-grey';
    } else if (card.is_error) {
        color = 'bg-error';
    }

   const card_classes = `card ${color} job-card`;
   const card_wrapper_classes = `job-card__wrapper ${color} job-card card-shape`

    return (
        <div class={card_wrapper_classes}>
        <div class={card_classes}>
            <div class='card-header'>
                <h3 class='card-title job-card__job_name'>{card.job_name}</h3>
            </div>
            <div class='card-body'>
                <Show when={card.has_run} fallback={<p>No Runs on Record</p>}>
                    <p>Last ran: {formatStartTime(card.started_at)}</p>
                    <p>Ran for: {formatDuration(card.duration)}</p>
                </Show>
            </div>
        </div>
        </div>
    )
};

const renderCardArray = (title: string, cards: JobCardData[]) => {
    // Find the number of extra cards needed for 4 columns
    let nCards = cards.length;
    let extraNeeded = 4 - (nCards % 4);

    if (cards.length === 0) {
        return (<></>)
    }

    return (
        <>
        <div class="card-group">
        <h2>{title}</h2>
          <div class='columns card-group'>
              <For each={cards}>
              {(card => { 
                  return (
                      <div class='column col-3' title={card.job_name}>
                        <JobCard {...card} />
                      </div>
                  )
              })}
              </For>

              <For each={new Array(extraNeeded)}>
              {(_ => {
                  return (
                      <div class='column col-3'>
                        <div class="empty card-shape"></div>
                      </div>
                  )
              })}
              </For>
          </div>
          </div>
      </>
    )
}
export const renderCards: Component<JobCardData[]> = (cards: JobCardData[]) => {

    let noRuns = cards.filter(card => !card.has_run);
    let hasError = cards.filter(card => card.is_error);
    let success = cards.filter(card => card.has_run && !card.is_error);

    return (
        <>
        {renderCardArray("Errors", hasError)}
        {renderCardArray("Successful", success)}
        {renderCardArray("No Runs", noRuns)}
        </>
    )
}


