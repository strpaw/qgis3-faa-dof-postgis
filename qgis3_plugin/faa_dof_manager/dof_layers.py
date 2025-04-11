"""FAA DOF layers handling"""
from __future__ import annotations
import logging

from qgis.core import (
    QgsDataProvider,
    QgsMapLayer,
    QgsProject,
    QgsDataSourceUri
)

from qgis.PyQt.QtWidgets import (
    QWidget,
    QMessageBox
)

from .errors import (
    LayerError,
    NoLayersError
)
from .types import DBConnectionSettings


class DOFLayers:

    """Handle DOF layers"""

    REQUIRED_LAYERS: list[str] = [
        "country",
        "obstacle",
        "us_state"
    ]
    EXPECTED_PROVIDER: str = "PostgreSQL database with PostGIS extension"

    def __init__(self) -> None:
        self.layers: dict[str, QgsMapLayer] = {}

    def find_layer(self, name: str) -> bool | Exception:
        """Find required layer from the QGIS Project layers.

        :param name: layer to be found
        :return: True if layer is added, False if layer is not added or more than one
        layers added with name 'name'
        """
        layers: list[QgsMapLayer] = QgsProject.instance().mapLayersByName(name)

        if not layers:
            raise NoLayersError(f"Layer {name} not added to the QGIS project.")

        if len(layers) > 1:
            raise LayerError(f"{len(layers)} layers  '{name}' found in layers.\n"
                             f"Only one layer '{name}' is allowed.\n"
                             f"Remove unnecessary/duplicated layers.")

        self.layers[name] = layers[0]
        return True

    def check_provider(self, name: str) -> bool | Exception:
        """Check if provider for required layer is PostgreSQL with PostGIS extension.

        :param name: layer name to check
        :return: True if provider is PostgreSQL+PostGIS, False otherwise
        """
        provider: QgsDataProvider = self.layers[name].dataProvider()
        actual_storage: str = provider.storageType()
        if actual_storage == DOFLayers.EXPECTED_PROVIDER:
            return True

        raise LayerError(f"Layer {name} is not a PostgreSQL database with PostGIS extension.")

    def check_layers(self) -> bool:
        """Check if required layers
        - are added to the QGIS project
        - are 'PostGIS' layers

        :return: True if check successful, False otherwise
        """
        logging.info("Checking layers...")
        check_result = True
        for layer in DOFLayers.REQUIRED_LAYERS:
            logging.info("Checking layer %s...", layer)
            try:
                self.find_layer(layer)
                self.check_provider(layer)
                logging.info("Layer %s check result successful.", layer)
            except NoLayersError as e:
                check_result = False
                logging.error(e)
                break
            except LayerError as e:
                check_result = False
                logging.error(e)

        if check_result:
            logging.info("Layers check successful.")
            return True

        msg = "Layers check failed. Load correct layers and run plugin again."
        logging.error(msg)
        QMessageBox.critical(QWidget(), "Message", msg)
        return False

    def get_db_settings(self) -> DBConnectionSettings:
        """Return database connection settings based on the obstacle layer.

        :return: database connection settings (host, database, credentials)
        """
        layer = self.layers["obstacle"]
        provider = layer.dataProvider()
        uri = QgsDataSourceUri(provider.dataSourceUri())
        return DBConnectionSettings(
            host=uri.host(),
            database=uri.database(),
            user=uri.username(),
            password=uri.password()
        )
