/**
 * Utils for postinstall/prebuild scripts.
 */
import fs from 'fs'
import path from 'path'
import zlib from 'zlib'
import { execSync } from 'child_process'
import { Readable } from 'stream'
import { finished } from 'stream/promises'
import * as messages from './messages.js'

// Non-NodeJS requirements
import { globSync } from 'glob'


export { messages }

export function findNodeModules({startDir} = {}) {
    if (startDir == undefined) {
        startDir = process.cwd()
    }

    let dir = startDir
    while (dir) {
        let nodeModules = path.join(dir, 'node_modules')
        if (fs.existsSync(nodeModules)) {
            return nodeModules
        }
        const parentDir = path.dirname(dir)
        if (parentDir == dir) {
            throw new Error(`node_modules not found`)
        }
        dir = parentDir
    }

    throw new Error(`node_modules not found`)
}

export function findPythonSitePackages() {
    return execSync(`python -c 'from site import getsitepackages; print(getsitepackages()[0])'`, {encoding: 'utf-8'}).trimEnd()
}

export function getCgroupAnchorPoint() {
    for (const line of fs.readFileSync('/proc/1/cgroup', {encoding:'utf-8'}).split('\n')) {
        const m = line.match(/^\d+:cpuset:(.+)/)
        if (m) {
            return m[1]
        }
    }

    throw new Error(`cpuset cgroup not found`)
}

export function inDocker() {
    const anchorPoint = getCgroupAnchorPoint()
    if (anchorPoint.startsWith('/docker/')) {
        const ref = anchorPoint.substring('/docker/'.length)
        const inContainer = fs.existsSync('/.dockerenv')
        if (inContainer) {
            return `container:${ref}`
        }
        else {
            return `${ref}`
        }
    }

    return null
}

export function copy(pattern, target, {base} = {}) {
    if (base === undefined) {
        base = process.cwd()
    }

    const files = globSync(pattern, {cwd: base})
    
    if (files.length == 0) {
        messages.error(`[copy] ${pattern}: no file`)
        return
    }
    
    console.log(`[copy] ${pattern}: ${files.length} file${files.length > 1 ? 's' : ''} ...`)
    
    for (const file of files) {
        const src = path.join(base, file)
        const dst = path.join(target, file)
        fs.mkdirSync(path.dirname(dst), {recursive: true})
        fs.copyFileSync(src, dst)
    }
}

const _cleanDirs = []

function inCleanDirs(file) {
    for (let cleanDir of _cleanDirs) {
        if (file.startsWith(`${cleanDir}${path.sep}`)) {
            return true
        }
    }
}

export function clean(pattern, {dryRun, ignore, noDefaultIgnore, ...options} = {}) {
    if (ignore === undefined) {
        ignore = []
    }

    if (!noDefaultIgnore) {
        for (const value of ['.venv/**', '.venv.*/**', 'node_modules/**', 'local/**']) {
            if (!pattern.includes(value) && !ignore.includes(value)) {
                ignore.push(value)
            }
        }
    }
    
    const files = globSync(pattern, {ignore, ...options})
    console.log(`[clean${dryRun ? ' dryrun' : ''}] ${pattern}: ${files.length} file${files.length > 1 ? 's' : ''} ...`)

    if (dryRun) {
        for (const file of files) {
            if (! inCleanDirs(file)) {
                messages.debug(`    ${file}`)
                if (fs.lstatSync(file).isDirectory()) {
                    _cleanDirs.push(file)
                }
            }
        }
    }
    else {
        for (const file of files) {
            messages.debug(`    ${file}`)
            fs.rmSync(file, {recursive: true, force: true})
        }
    }
}

export function run(cmd, {noException, ...options} = {}) {
    if (options.stdio === undefined) {
        options.stdio = 'inherit'
    }

    try {
        messages.debug(cmd) 
        execSync(cmd, options)
        return 0
    }
    catch (err) {
        const msg = `command exited with code ${err.status}`
        if (noException) {
            messages.error(msg)
            return err.status
        }
        else {
            throw new Error(msg)
        }
    }
}

export async function download(url, dst, {gunzip} = {}) {
    console.log(`[download] ${url}`)
    fs.mkdirSync(path.dirname(dst), {recursive: true})
    
    const res = await fetch(url)  
    
    let stream = Readable.fromWeb(res.body)
    if (gunzip) {
        stream = stream.pipe(zlib.createGunzip())    
    }
    await finished(stream
        .pipe(fs.createWriteStream(dst, { flags: 'w' }))
    )
}

export function getLastModifiedFile(dir) {
    const data_list = []

    for (const name of fs.readdirSync(dir)) {
        const file = path.join(dir, name)
        const stat = fs.statSync(file)
        if (stat.isDirectory()) {
            continue
        }
        data_list.push({file, mtime: stat.mtime.getTime()})
    }

    data_list.sort((fileA, fileB) => fileB.mtime - fileA.mtime)
    const data = data_list[0]
    return data !== undefined ? data.file : null
}
