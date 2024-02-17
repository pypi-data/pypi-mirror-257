/**
 * Put formatters in the global scope so that bootstrapTables can use them in HTML
 * @file
 */
import { formatters } from "./commons.js"

window.intFormatter = formatters.int
window.dateFormatter = formatters.date
window.linkFormatter = formatters.link
window.followingFormatter = formatters.following
