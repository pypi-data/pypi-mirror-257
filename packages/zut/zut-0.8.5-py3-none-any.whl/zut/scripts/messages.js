export function error(msg) {
    console.error('\x1b[31m%s\x1b[0m', msg)
}

export function warning(msg) {
    console.error('\x1b[33m%s\x1b[0m', msg)
}

export function success(msg) {
    console.log('\x1b[32m%s\x1b[0m', msg)
}

export function debug(msg) {
    console.log('\x1b[90m%s\x1b[0m', msg)
}
