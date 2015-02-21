__author__ = 'carolinux'

DEFAULT_FRAME_UNIT = "seconds"
DEFAULT_FRAME_SIZE = 1
MIN_TIMESLIDER_DEFAULT = 0
MAX_TIMESLIDER_DEFAULT = 1
DEFAULT_FRAME_LENGTH = 500
FRAME_FILENAME_PREFIX = "frame"

NO_INTERPOLATION = "No interpolation (faster)"
LINEAR_INTERPOLATION = "Linear interpolation (point geometries only)"
INTERPOLATION_MODES = {LINEAR_INTERPOLATION:True, # add other
                        # interpolation modes where interpolation=True at the beginning
                       NO_INTERPOLATION:False,}
NO_ID_TEXT = "None - every geometry is a position of the same moving object in time"

SAVE_DELIMITER=';'
