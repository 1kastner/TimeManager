__author__ = 'carolinux'

## UI settings
DEFAULT_FRAME_UNIT = "minutes"
DEFAULT_FRAME_SIZE = 1
DEFAULT_SHOW_LABEL = True
DEFAULT_EXPORT_EMPTY = True
MIN_TIMESLIDER_DEFAULT = 0
MAX_TIMESLIDER_DEFAULT = 1
DEFAULT_FRAME_LENGTH = 500
FRAME_FILENAME_PREFIX = "frame"
DEFAULT_GRANULARITY_IN_SECONDS = 1

## interpolation settings
NO_INTERPOLATION = "No interpolation (faster)"
LINEAR_POINT_INTERPOLATION = "Linear interpolation (point geometries only)"
INTERPOLATION_MODES = {LINEAR_POINT_INTERPOLATION:True, # add other
                        # interpolation modes where interpolation=True at the beginning
                       NO_INTERPOLATION:False,}

INTERPOLATION_MODE_TO_CLASS = {LINEAR_POINT_INTERPOLATION:"LinearPointInterpolator",
                            }
DEFAULT_ID = 0
NO_ID_TEXT = "None - every geometry is a position of the same moving object in time"

## load/save settings
SAVE_DELIMITER=';'

## logging settings 

LOG_TAG="TimeManager"

