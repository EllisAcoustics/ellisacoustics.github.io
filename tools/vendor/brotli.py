"""Minimal stand-in for the `brotli` module, used only when the real one is missing.
fontTools needs brotli to write WOFF2; Node.js ships Brotli in its standard library, so this
pipes the bytes through `node` instead."""
import subprocess

_JS = ("const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d)).on('end',()=>{"
       "const b=Buffer.concat(c);process.stdout.write(process.argv[1]==='c'?"
       "z.brotliCompressSync(b,{params:{[z.constants.BROTLI_PARAM_QUALITY]:+process.argv[2],"
       "[z.constants.BROTLI_PARAM_MODE]:+process.argv[3],[z.constants.BROTLI_PARAM_LGWIN]:+process.argv[4],"
       "[z.constants.BROTLI_PARAM_SIZE_HINT]:b.length}}):z.brotliDecompressSync(b))})")
MODE_GENERIC, MODE_TEXT, MODE_FONT = 0, 1, 2


def compress(data, mode=0, quality=11, lgwin=22, lgblock=0):
    return subprocess.run(['node', '-e', _JS, 'c', str(quality), str(mode), str(lgwin)], input=data, capture_output=True, check=True).stdout


def decompress(data):
    return subprocess.run(['node', '-e', _JS, 'd'], input=data, capture_output=True, check=True).stdout
