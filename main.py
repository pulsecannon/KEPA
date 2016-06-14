#!/usr/bin/env python
"""Router for KEPA."""


import controller
import webapp2


routes = [
  webapp2.Route('/', handler='controller.Main',
                name='main'),
  webapp2.Route('/agg-reports/', handler='controller.AggReportsRequestHandler',
                name='aggrigate_reports'),
  webapp2.Route('/sync-data/', handler='controller.DataSyncPipelineRequestHandler',
                name='sync_handler')
]

app = webapp2.WSGIApplication(routes, debug=True)
