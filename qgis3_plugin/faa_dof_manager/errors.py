"""Custom errors"""


class FAADOFManagerError(Exception):
    """Base FAADOFManager exception"""


class NoLayersError(FAADOFManagerError):
    """Risen when layers added to the QGIS project"""


class LayerError(FAADOFManagerError):
    """Risen when required layer is incorrect (e.g.: provider)"""


class DBConnectionError(FAADOFManagerError):
    """Risen when connection to the database cannot be established"""


class ObstacleNotFoundError(FAADOFManagerError):
    """Risen when obstacle not found in database"""


class CoordinateError(FAADOFManagerError):
    """Risen when coordinate has error os is in not supported format"""


class MissingRequiredValueError(FAADOFManagerError):
    """Risen when required value is not entered by user"""


class NumberExpectedError(FAADOFManagerError):
    """Risen when value is not a number"""
