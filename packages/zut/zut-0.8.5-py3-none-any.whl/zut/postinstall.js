#!/usr/bin/node
import { copy, findNodeModules } from './scripts/index.js'

const target = 'django/static/zut/lib'
const options = {base: findNodeModules()}

copy('bootstrap/LICENSE', target, options)
copy('bootstrap/dist/css/bootstrap.min.css', target, options)
copy('bootstrap/dist/css/bootstrap.min.css.map', target, options)
copy('bootstrap/dist/js/bootstrap.bundle.min.js', target, options)
copy('bootstrap/dist/js/bootstrap.bundle.min.js.map', target, options)

copy('bootstrap-icons/LICENSE', target, options)
copy('bootstrap-icons/font/bootstrap-icons.min.css', target, options)
copy('bootstrap-icons/font/fonts/bootstrap-icons.woff', target, options)
copy('bootstrap-icons/font/fonts/bootstrap-icons.woff2', target, options)

copy('jquery/LICENSE.txt', target, options)
copy('jquery/dist/jquery.min.js', target, options)

copy('bootstrap-table/LICENSE', target, options)
copy('bootstrap-table/dist/bootstrap-table.min.css', target, options)
copy('bootstrap-table/dist/bootstrap-table.min.js', target, options)
copy('bootstrap-table/dist/locale/*.min.js', target, options)

copy('select2/LICENSE.md', target, options)
copy('select2/dist/css/select2.min.css', target, options)
copy('select2/dist/js/select2.min.js', target, options)
copy('select2/dist/js/i18n/*.js', target, options)

copy('select2-bootstrap-5-theme/LICENSE', target, options)
copy('select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css', target, options)
