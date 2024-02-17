import { formatters, submitLoading, initBootstrapTable } from "../js/commons.js"
import { BASE_WEBSOCKET_URL, startWebsocket } from "../js/websockets.js"
import { calculateDuration, taskFormatters } from "../js/celery.js"

const tableId = 'task-list'
const tableElem = document.getElementById(tableId)
const actionElem = document.getElementById('task-list-action')

function onMessage(data) {
    if (data.tasks) {
        for (let task of data.tasks) {
            appendOrUpdate(task)
        }
    }

    if (data.task) {
        appendOrUpdate(data.task)
    }
}

function appendOrUpdate(task) {
    const row = table.bootstrapTable('getRowByUniqueId', task['id'])
    if (row) {
        table.bootstrapTable('updateByUniqueId', {id: task['id'], row: task})
    }
    else {
        table.bootstrapTable('append', task)
    }

}

function prepareTable() {
    return initBootstrapTable(tableId, {
        uniqueId: 'id',
        clickToSelect: true,
        fields: {
            _checkbox: { checkbox: true, sortable: false },
            id: { formatter: taskFormatters.shortId },
            state: { formatter: taskFormatters.state },
            progress: { formatter: taskFormatters.progress },
            start: { formatter: formatters.date },
            end: { formatter: formatters.date },
            duration: { formatter: taskFormatters.duration },
        }
    })
}

function updateTaskDurations() {
    setTimeout(() => {
        tableElem.querySelectorAll('.task-duration').forEach(elem => elem.innerHTML = '-')
        const tasks = table.bootstrapTable('getData', {useCurrentPage: true, includeHiddenRows: false})
        for (let task of tasks) {
            const duration_elem = tableElem.querySelector(`.task-duration[data-task-id="${task.id}"]`)
            if (duration_elem) {
                duration_elem.innerHTML = calculateDuration(task.start, task.end) ?? '-'
            }
        }

        updateTaskDurations()
    }, 900)
}

function bindActions() {
    actionElem.form.addEventListener('submit', (ev) => {
        ev.preventDefault()

        const data = {}
        
        data.action = actionElem.options[actionElem.selectedIndex].value
        if (! data.action) {
            return
        }

        const task_ids = table.bootstrapTable('getSelections').map(row => row['id'])
        data.task_ids = task_ids.join(';')
        if (! data.task_ids.length) {
            return
        }

        submitLoading(actionElem.form, {
            data,
            onSuccess: () => {
                if (data.action == 'forget') {
                    for (const task_id of task_ids) {
                        table.bootstrapTable('removeByUniqueId', task_id)
                    }
                }    
            }            
        })
    })
}

function bindLaunchTask() {
    const form = document.getElementById('taskLaunch')
    form.addEventListener('submit', ev => {
        ev.preventDefault()
        submitLoading(form)
    })

    const taskNameElem = document.getElementById('taskLaunch-name')
    $(taskNameElem).select2({
        theme: 'bootstrap-5',
        placeholder: taskNameElem.dataset.placeholder,
        allowClear: true,
        tags: true,
    })
}

let table = prepareTable()
updateTaskDurations()
bindActions()
bindLaunchTask()
startWebsocket(`${BASE_WEBSOCKET_URL}${window.location.pathname}`, {onMessage, name: 'tasks', reconnectButton: true})
