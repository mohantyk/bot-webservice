#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 05:26:25 2019

@author: kaniska
"""

import os

from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def main(request):
    return web.Response(status=200, text="Hello World!")

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
        
    web.run_app(app, port=port)