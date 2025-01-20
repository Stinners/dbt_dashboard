import { Component, For, Show } from 'solid-js';
import moment from 'moment';

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

//  2025-01-02T12:43:06.732752
const DateFormat = 'YYYY-MM-DDTHH:mm:ss.SSSSSS';
const formatStartTime = (timeStr?: string): string => {
    if (timeStr) {
        let date = moment.utc(timeStr, DateFormat).local();
        return date.format("MMM Do LT");
    } else {
        return "---";
    }
}

const displayDuration = (duration: moment.Duration): string => {
    if (duration.hours() != 0) {
        return `${duration.hours()}hours ${duration.minutes()} minutes`
    } else if (duration.minutes() != 0) {
        return `${duration.minutes()} minutes ${duration.seconds()} seconds`
    } else {
        return `${duration.seconds()} seconds`
    }
}

const formatDuration = (durationStr?: string): string => {
    if (durationStr) {
        let duration = moment.duration(durationStr);
        return displayDuration(duration);
    }
    else {
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


