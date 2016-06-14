"""Models for KEPA."""

import datetime

from google.appengine.ext import ndb


class Earth(object):
  """Earth enum used for relativity."""
  RADIUS = 1
  DAYS = 365
  TEMP_MAX = 331.15
  TEMP_MIN = 185.15


class Sun(object):
  """Sun enum used for relativity."""
  MASS = 1
  RADIUS = 1
  TEMP = 5778


class ExoPlanet(ndb.Model):
  """The exo-planet model."""
  planet_id = ndb.IntegerProperty()
  name = ndb.StringProperty()
  koi_name = ndb.StringProperty()
  koi_number = ndb.FloatProperty()
  temprature = ndb.IntegerProperty()
  radius = ndb.FloatProperty()
  transit_duration = ndb.FloatProperty()
  period = ndb.FloatProperty()
  star_mass = ndb.FloatProperty()
  star_temp = ndb.IntegerProperty()
  star_radius = ndb.FloatProperty()
  star_gravity = ndb.FloatProperty()
  last_update = ndb.DateTimeProperty()

  @classmethod
  def CreateExoPlanetEntity(cls, koi):
    """Creates a exo_planet instance from the dict format.

    Args:
      exo_planet: dict, the exo-planet dict.
    Returns:
      models.ExoPlanet, the exo-planet instance.
    """
    entity = cls()
    UpdateExoPlanetProperties(entity, koi)
    return entity


def UpdateExoPlanetProperties(entity, koi):
  """Updates an exo planets properties from the koi.

  Args:
    entity: models.ExoPlanet, the exo-planet entity.
    koi: dict, the koi dict.
  """
  entity.planet_id = int(koi.get('Kepler ID'))
  entity.name = koi.get('KOI Name')
  entity.koi_name = koi.get('Kepler Name')
  entity.koi_number = float(
      koi.get('KOI Number') if koi.get('KOI Number') else 0.0)
  entity.temprature = int(
      koi.get('Teq') if koi.get('Teq') else 0)
  entity.radius = float(
      koi.get('Planet Radius') if koi.get('Planet Radius') else 0.0)
  entity.transit_duration = float(
      koi.get('Duration') if koi.get('Duration') else 0.0)
  entity.period = float(
      koi.get('Period') if koi.get('Period') else 0.0)
  entity.star_mass = float(
      koi.get('Stellar Mass') if koi.get('Stellar Mass') else 0.0)
  entity.star_temp = int(
      koi.get('Teff') if koi.get('Teff') else 0)
  entity.star_radius = float(
      koi.get('Stellar Radius') if koi.get('Stellar Radius') else 0.0)
  entity.star_gravity = float(
      koi.get('log(g)') if koi.get('log(g)') else 0.0)
  entity.last_update = datetime.datetime.strptime(
      koi.get('Last vet Update'), '%Y-%m-%d %H:%M:%S')
