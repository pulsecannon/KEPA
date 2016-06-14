"""Pipelines for KEPA."""

import constants
import collections
import datetime
import logging
import pipeline
import models
import utils

from google.appengine.ext import ndb


_MODEL = models.ExoPlanet


@ndb.tasklet
def _SyncKoiExoPlanets(kois):
  """Sync kois with exo planets by creating new ones or updating existing.

  Args:
    list<dict>, the exo-planets to sync.
  """
  results = collections.defaultdict(list)
  koi_ids = [ep.get('kepid') for ep in kois]
  results['received'] += koi_ids
  to_sync = []
  existing_exo_planets = yield _MODEL.query(
      _MODEL.planet_id.IN(koi_ids)).fetch_async()
  exo_planet_map = {ep.planet_id: ep for ep in existing_exo_planets}
  for koi in kois:
    new_exo_planet_id = koi.get('kopid')
    existing_exo_planet = exo_planet_map.get(new_exo_planet_id)
    if existing_exo_planet and (
        existing_exo_planet.last_updated < datetime.datetime(
            planet.get('last_update', 0))):
      models.UpdateExoPlanetProperties(existing_exo_planet, koi)
      results['synced'].append(existing_exo_planet.planet_id)
      to_sync.append(existing_exo_planet)
    else:
      new_exo_planet = models.ExoPlanet.CreateExoPlanetEntity(koi)
      to_sync.append(new_exo_planet)
      results['added'].append(new_exo_planet.planet_id)
  yield ndb.put_multi_async(to_sync)
  raise ndb.Return(results)


class ExoPlanetSyncPipeline(pipeline.Pipeline):
  """ExoPlanet sync pipeline for kepler confirmed planets."""

  def run(self, *args, **kwargs):
    """The body of the pipeline."""
    logging.info(constants.SYNC_PIPELINE_START)
    kois = utils.ReadKOIS()
    results = _SyncKoiExoPlanets(kois).get_result()
    logging.info(constants.SYNC_PIPELINE_RES % (
        'Synced', len(results['synced'])))
    logging.info(constants.SYNC_PIPELINE_RES % (
        'Added', len(results['added'])))
    logging.info(constants.SYNC_PIPELINE_FIN)
