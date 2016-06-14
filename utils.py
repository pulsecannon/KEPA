"""Utility functions for KEPA."""

import constants
import httplib
import json
import logging
import urllib


def ReadKOIS():
  """Reads kepler objects of intrest.

  Returns:
    list<dict>, the kepler objects of intrest.
  """
  # construct request to kepler uri.
  logging.info('Connecting to host.')
  connection = httplib.HTTPConnection(constants.HOST)
  connection.request('GET', constants.KOI_SEARCH_URI)
  data = None
  try:
    response = connection.getresponse()
    if response.status == httplib.OK and response.reason == constants.OK:
      logging.info('Got response.')
      data = json.load(response)
    else:
      logging.error(constants.REQUEST_FAILED % (
          response.reason, response.status))
  except:
    logging.exception(constants.CONN_EXCEPTION)
  finally:
    logging.info('Closing connection.')
    connection.close()
  return data
