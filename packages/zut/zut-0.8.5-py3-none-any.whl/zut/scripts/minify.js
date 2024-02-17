import fs from 'fs'
import path from 'path'
import readline from 'readline'
import * as messages from './messages.js'

// Non-NodeJS requirements
import { globSync } from 'glob'
import { transform as transformCss } from 'lightningcss'
import UglifyJS from 'uglify-js'

function replaceJsImports(code) {
    let result = ''
    for (let line of code.replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n')) {
        line = line.replace(/^(\s*import[^a-z0-9\-_].+)\.js(['"]\s*;?)\s*$/i, '$1.min.js$2') // replace '.js' by '.min.js' in import statements
        result += `${line}\n`
    }
    return result
}

export function minifyCss(pattern) {
    if (! pattern.endsWith('.css')) {
        messages.error(`[minifyCss] ${pattern}: does not end with ".css"`)
        return
    }

    const srcFiles = globSync(pattern, {ignore: '**/*.min.*'})
    
    if (srcFiles.length == 0) {
        messages.error(`[minifyCss] ${pattern}: no file`)
        return
    }
    
    console.log(`[minifyCss] ${pattern}: ${srcFiles.length} file${srcFiles.length > 1 ? 's' : ''} ...`)

    for (const srcFile of srcFiles) {
        const dstFile = srcFile.replace(/\.css$/, '.min.css')
        const code = fs.readFileSync(srcFile, {encoding: 'utf-8'})

        const result = transformCss({
            filename: path.basename(srcFile),
            code: Buffer.from(code),
            minify: true,
            sourceMap: true,
        })

        if (!result.code || !result.map) {            
            messages.error(`[minifyCss] ${srcFile}: ${result}`)
            continue
        }
        
        const codeWithSourceMappingUrl = `${result.code}\n//# sourceMappingURL=${path.basename(dstFile)}.map`

        fs.writeFileSync(dstFile, codeWithSourceMappingUrl, {encoding: 'utf-8'})
        fs.writeFileSync(`${dstFile}.map`, result.map, {encoding: 'utf-8'})
    }
}

export function minifyJs(pattern) {
    if (! pattern.endsWith('.js')) {
        messages.error(`[minifyJs] ${pattern}: does not end with ".js"`)
        return
    }

    const srcFiles = globSync(pattern, {ignore: '**/*.min.*'})
    
    if (srcFiles.length == 0) {
        messages.error(`[minifyJs] ${pattern}: no file`)
        return
    }
    
    console.log(`[minifyJs] ${pattern}: ${srcFiles.length} file${srcFiles.length > 1 ? 's' : ''} ...`)

    for (const srcFile of srcFiles) {
        const dstFile = srcFile.replace(/\.js$/, '.min.js')
        const code = replaceJsImports(fs.readFileSync(srcFile, {encoding: 'utf-8'}))

        const result = UglifyJS.minify(code, {
            sourceMap: {
                filename: path.basename(srcFile),
                url: `${path.basename(dstFile)}.map`,
            }
        })

        if (!result.code || !result.map) {               
            messages.error(`[minifyJs] ${srcFile}: ${result}`)
            continue
        }

        fs.writeFileSync(dstFile, result.code, {encoding: 'utf-8'})
        fs.writeFileSync(`${dstFile}.map`, result.map, {encoding: 'utf-8'})
    }
}

export function minify(pattern) {
    const srcFiles = globSync(pattern, {ignore: '**/*.min.*'})
    
    if (srcFiles.length == 0) {
        messages.error(`[minify] ${pattern}: no file`)
        return
    }

    for (const srcFile of srcFiles) {
        if (srcFile.endsWith('.css')) {
            minifyCss(srcFile)
        }
        else if (srcFile.endsWith('.js')) {
            minifyJs(srcFile)
        }    
        else {
            messages.error(`[minify] ${srcFile}: does not end with ".css" or ".js"`)
        }
    }
}
