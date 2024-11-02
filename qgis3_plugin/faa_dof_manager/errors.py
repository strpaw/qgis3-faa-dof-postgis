"""Custom errors"""


class FAADOFManagerError(Exception):
    """Base FAADOFManager exception"""


class NoLayersError(FAADOFManagerError):
    """Risen when layers added to the QGIS project"""


class LayerError(FAADOFManagerError):
    """Risen when required layer is incorrect (e.g.: provider)"""
