#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 05:26:25 2019

@author: kaniska
"""

import os

import aiohttp
from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

router = routing.Router()
routes = web.RouteTableDef()

@router.register('issues', action='opened')
async def issue_opened_event(event, gh, *args, **kwargs):
    url = event.data['issue']['comments_url']
    author = event.data['issue']['user']['login']
    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)"
    print(message)
    await gh.post(url, data={"body": message})

@routes.post("/")
async def main(request):
    # read the GitHub webhook payload
    body = await request.read()
    
    # our authentication token and secret
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")
    
    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)
    
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, 'mohantyk', oauth_token=oauth_token)
        await router.dispatch(event, gh)
        
    return web.Response(status=200)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
        
    web.run_app(app, port=port)