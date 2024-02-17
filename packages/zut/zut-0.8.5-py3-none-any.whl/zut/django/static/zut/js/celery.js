import { formatters } from "./commons.js"
import { BASE_WEBSOCKET_URL, startWebsocket } from "./websockets.js"

export function calculateDuration(start, end) {
    if (! start || start == 'null') {
        return null
    }
    else if (typeof(start.getMonth) != 'function') {
        start = new Date(start)
    }

    if (! end || end == 'null') {
        end = new Date()
    }
    else if (typeof(end.getMonth) != 'function') {
        end = new Date(end)
    }
    
    const total_ms = end - start
    const sign = total_ms < 0 ? '-' : ''
    const total_sec = Math.round(Math.abs(total_ms / 1000))
    const total_min = Math.floor(total_sec / 60)
    const remaining_sec = total_sec - 60 * total_min
    const total_h = Math.floor(total_min / 60)
    const remaining_min = total_min - 60 * total_h
    const total_j = Math.floor(total_h / 24)
    const remaining_h = total_h - 24 * total_j
    return `${sign}${total_j > 0 ? `${total_j}j&nbsp;` : ''}${remaining_h < 10 ? '0' : ''}${remaining_h}:${remaining_min < 10 ? '0' : ''}${remaining_min}:${remaining_sec < 10 ? '0' : ''}${remaining_sec}`
}

export const taskFormatters = {
    shortId: function (value) {
        if (! value) {
            return value
        }
        let base = window.location.pathname.replace(/\/$/, '')
        return `<a href="${base}/${value}/" title="${value}">${value.substring(0,8)}…</a>`
    },

    state: function (value) {
        let color = 'secondary'
        switch (value) {
            case 'STARTED': color = 'primary'; break
            case 'PROGRESS': color = 'info'; break
            case 'FAILURE': color = 'danger'; break
            case 'SUCCESS': color = 'success'; break
            case 'RETRY': color = 'warning'; break
            case 'ISSUE': color = 'warning'; break
        }
        return `<span class="text-${color}">${value}</span>`
    },

    progress: function (value, row) {
        if (! value) {
            return null
        }
    
        value = parseInt(value)
        return `<div class="progress"><div class="progress-bar${row['state'] == 'PROGRESS' ? ' progress-bar-striped progress-bar-animated' : ''}" role="progressbar" aria-valuenow="${value}%" aria-valuemin="0" aria-valuemax="100" style="width: ${value}%">${value}%</div></div>`
    },

    duration: function (value, row) {
        return `<span class='task-duration' data-task-id="${row.id}">${calculateDuration(row.start, row.end) ?? '-'}</span>`
    },
}

/**
 * Create a websocket to monitor the status of a task.
 * @param {HTMLElement} container
 */
export function startTaskDetailWebsocket(container) {
    const task_id = container.dataset.taskId

    const id_elem = container.querySelector('[data-field="id"]')
    const name_elem = container.querySelector('[data-field="name"]')
    const params_elem = container.querySelector('[data-field="params"]')
    const worker_elem = container.querySelector('[data-field="worker"]')
    const state_elem = container.querySelector('[data-field="state"]')
    const progress_elem = container.querySelector('[data-field="progress"]')
    const details_elem = container.querySelector('[data-field="details"]')
    const start_elem = container.querySelector('[data-field="start"]')
    const end_elem = container.querySelector('[data-field="end"]')
    const duration_elem = container.querySelector('[data-field="duration"]')

    function onMessage(data) {
        if (id_elem) {
            id_elem.innerHTML = data.task.id ?? '-'
        }
        if (name_elem) {
            name_elem.innerHTML = data.task.name ?? '-'
        }
        if (params_elem) {
            params_elem.innerHTML = data.task.params ?? '-'
        }
        if (worker_elem) {
            worker_elem.innerHTML = data.task.worker ?? '-'
        }
        if (state_elem) {
            state_elem.innerHTML = taskFormatters.state(data.task.state) ?? '-'
        }
        if (progress_elem) {
            progress_elem.innerHTML = taskFormatters.progress(data.task.progress, {state: data.task.state}) ?? '-'
        }
        if (details_elem) {
            details_elem.innerHTML = data.task.details ?? '-'
        }
        if (start_elem) {
            start_elem.dataset.value = data.task.start
            start_elem.innerHTML = formatters.date(data.task.start) ?? '-'
        }
        if (end_elem) {
            end_elem.dataset.value = data.task.end
            end_elem.innerHTML = formatters.date(data.task.end) ?? '-'
        }
        if (duration_elem) {
            duration_elem.innerHTML = taskFormatters.duration(null, {start: data.task.start, end: data.task.end}) ?? '-'
        }
    }
    
    function updateTaskDuration() {
        setTimeout(() => {
            duration_elem.innerHTML = calculateDuration(start_elem.dataset.value, end_elem.dataset.value) ?? '-'
            updateTaskDuration()
        }, 900)
    }
    
    const prefix = window.location.pathname.startsWith('/task/') ? '/task' : '/zut/task'
    const url = `${BASE_WEBSOCKET_URL}${prefix}/${task_id}/`
    startWebsocket(url, {onMessage, name: `task-${task_id}`})
    if (duration_elem) {
        updateTaskDuration()
    }
}
