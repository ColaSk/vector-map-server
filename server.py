#!/usr/bin/env python3
import os
import aiosqlite

import ujson

import sanic
from sanic import response

import config

vector_server = sanic.Sanic("vector_server")
vector_server.static("/static", "./static")

vector_server.update_config(config)

EMPTY_TILE = bytes.fromhex("1F8B0800FA78185E000393E2E3628F8F4FCD2D28A9D46850A86002006471443610000000")
EMPTY_FONT = bytes.fromhex("0A1F0A124D6574726F706F6C697320526567756C61721209313533362D31373931")


@vector_server.get("/")
async def index(request):
    return await response.file_stream("static/index.html")


@vector_server.before_server_start
async def initialize_sqlite(app: sanic.Sanic, loop):
    mbtiles_path = app.config['MBTILES_PATH']
    if not os.path.exists(mbtiles_path):
        raise FileExistsError(f"file {mbtiles_path} does not exists")

    app.ctx.connection = await aiosqlite.connect(mbtiles_path)
    

@vector_server.before_server_stop
async def deinitialize_sqlite(app: sanic.Sanic, loop):
    await app.ctx.connection.close()


@vector_server.get("/maps/metadata")
async def metadata(request: sanic.Request):
    """get metadata"""
    max_age = request.app.config['MAX_AGE_TIME']
    metadata = dict()
    async with request.app.ctx.connection.cursor() as cr:
        await cr.execute("SELECT name,value FROM metadata")
        res = await cr.fetchall()

    for k, v in res:
        if k == 'json':
            v = ujson.loads(v)

        metadata[k] = v

    return response.json(metadata,
                         headers={
                             'Cache-Control': f"max-age={max_age}",
                             'Access-Control-Allow-Origin': '*',
                         })


@vector_server.get("/maps/<z:int>/<x:int>/<y=int:ext=pbf>")
async def vector_titles(request: sanic.Request, z: int, x: int, y: int, ext: str):
    """get mbtiles"""
    max_age = request.app.config['MAX_AGE_TIME']
    tms_y = 2**z - y - 1

    async with request.app.ctx.connection.cursor() as cr:
        await cr.execute("SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
                         (z, x, tms_y))
        res = await cr.fetchone()

        blob = res and res[0] or EMPTY_TILE

    return response.HTTPResponse(
        blob, 200, {
            'Content-Type': 'application/x-protobuf',
            'Content-Encoding': 'gzip',
            'Content-Length': str(len(blob)),
            'Cache-Control': f"max-age={max_age}",
            'Access-Control-Allow-Origin': '*'
        })


if __name__ == "__main__":
    vector_server.run(host="0.0.0.0")
