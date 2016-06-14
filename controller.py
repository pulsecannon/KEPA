"""Controllers for KEPA"""

import constants
import collections
import json
import logging
import models
import os
import pipelines
import webapp2


from google.appengine.ext import ndb
from google.appengine.ext.webapp import template


class Main(webapp2.RequestHandler):
  """Main request handler."""

  def get(self):
    """Servers index.html"""
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))


class DataSyncPipelineRequestHandler(webapp2.RequestHandler):
  """Sync's data with the kepler open api's"""

  def get(self):
    """Starts the sync pipeline."""
    logging.info('Starting sync pipeline.')
    sync_pipeline = pipelines.ExoPlanetSyncPipeline()
    sync_pipeline.start()


class AggReportsRequestHandler(webapp2.RequestHandler):
  """The report view for KEPA."""

  def get(self):
    """Gets a aggrigate reports."""
    reports = GetAggChartsAsync().get_result()
    self.response.content_type = 'application/json'
    self.response.write(json.dumps(reports))


@ndb.tasklet
def GetAggChartsAsync():
  """Gets exo planet aggrigate charts.

  Yields:
    list<list<dict>>, the aggrigate reports
  """
  planets = yield models.ExoPlanet.query().fetch_async()
  agg_charts = yield (
      GetPlanetsSizeChartAsync(planets),
      GetPlanetsDaysAsync(planets),
  )
  raise ndb.Return(agg_charts)


@ndb.tasklet
def GetPlanetsSizeChartAsync(planets):
  """Gets planets by size chart data.

  Args:
    planets: models.ExoPlanet, the exo planets.
  """
  planets_by_size = collections.defaultdict(int)
  for planet in planets:
    if planet.radius < models.Earth.RADIUS:
      planets_by_size['Smaller Than Earth Size'] += 1
    if planet.radius > models.Earth.RADIUS:
      planets_by_size['Bigger Than Earth Size'] += 1
    if planet.radius == models.Earth.RADIUS:
      planets_by_size['Exactly Earth Size'] += 1

  planets_by_percent = [{'key': key, 'y': (value/float(len(planets))) * 100}
                        for key, value in planets_by_size.items()]
  raise ndb.Return(planets_by_percent)


@ndb.tasklet
def GetPlanetsDaysAsync(planets):
  """Gets planets by days chart data.

  Args:
    planets: models.ExoPlanet, the exo planets.
  """
  planets_by_size = collections.defaultdict(int)
  for planet in planets:
    if planet.radius < models.Earth.DAYS - constants.EARTH_DAYS_ERROR :
      planets_by_size['Years Shorter Than Earth'] += 1
    if planet.radius > models.Earth.DAYS + constants.EARTH_DAYS_ERROR:
      planets_by_size['Years Longer Than Earth'] += 1
    if planet.radius in (
          models.Earth.DAYS - constants.EARTH_DAYS_ERROR,
          models.Earth.DAYS + constants.EARTH_DAYS_ERROR):
      planets_by_size['Year Like Earth Year'] += 1

  planets_by_percent = [{'key': key, 'y': (value/float(len(planets))) * 100}
                        for key, value in planets_by_size.items()]
  raise ndb.Return(planets_by_percent)
