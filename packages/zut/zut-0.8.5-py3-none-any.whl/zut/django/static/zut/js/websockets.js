import { DEBUG, messages } from "./commons.js"
import { gettext } from "./i18n.js"

/**
 * Base URL for the websockets (without trailing slash).
 */
export const BASE_WEBSOCKET_URL = `${window.location.protocol == 'https:' ? 'wss:' : 'ws:'}//${window.location.hostname}${(window.location.protocol == 'http:' && window.location.port == 80) || (window.location.protocol == 'https:' && window.location.port == 443) ? '' : `:${window.location.port}`}/ws`

/**
 * Start a websocket.
 * @param {string} url URL of the websocket.
 * @param {object} options
 * @param {function} options.onMessage A function to call when a message is received from the websocket.
 * @param {boolean} options.reconnectButton If true, add a "Try to reconnect" button when connection to server is closed.
 * @param {string} options.name Optional name to display in debug messages.
 */
export function startWebsocket(url, {onMessage, reconnectButton, name} = {}) {
    let websocket = new WebSocket(url)
    const prefix = name ? `${name} ` : ''

    websocket.onopen = (ev) => {
        if (DEBUG) {
            console.log(`${prefix}websocket: open`)
        }
    }

    websocket.onclose = (ev) => {
        if (DEBUG) {
            console.log(`${prefix}websocket: close`, ev.code)
        }

        websocket = null
        let msg = gettext("Connection to web server closed")
        if (ev.code == 3000) { // unauthorized
            msg += gettext(":") + " " + gettext("Unauthorized") + "."
            messages.error(msg)
        }
        else if (ev.code == 4181) { // celery_not_working
            msg += gettext(":") + " " + gettext("Celery is not working") + "."
            messages.error(msg)
        }
        else {
            if (reconnectButton) {
                let bsAlert = null
                const messageElement = messages.error(`${msg}. <a href="#" class="reconnect">${gettext("Try to reconnect")}</a>.`)
                messageElement.querySelector('.reconnect').addEventListener('click', (ev) => {
                    ev.preventDefault()
                    startWebsocket(url, {onMessage, reconnectButton, name})
                    if (bsAlert && bsAlert._element) {
                        bsAlert.close()
                    }
                })
                bsAlert = new bootstrap.Alert(messageElement)
            }
            else {
                messages.error(`${msg}.`)
            }
        }
    }
    
    if (DEBUG || onMessage) {
        websocket.onmessage = (ev) => {
            const data = JSON.parse(ev.data)
            if (DEBUG) {
                console.log(`${prefix}websocket: message`, data)
            }
    
            onMessage(data)
        }
    }

    websocket.onerror = (ev) => {
        if (DEBUG) {
            console.error(`${prefix}websocket: error`, ev)
        }
        // No need to display error: onclosed is also automatically called
    }
}
