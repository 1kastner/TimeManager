from qgis._core import QgsMapLayerRegistry, QgsMessageLog

__author__ = 'carolinux'


def getLayerAttributes(layerId):
    try:
        layer=QgsMapLayerRegistry.instance().mapLayers()[layerId]
        #QgsMessageLog.logMessage(str(QgsMapLayerRegistry.instance().mapLayers()))
        #QgsMessageLog.logMessage("layer"+str(layer))
        provider=layer.dataProvider() # this will crash on OpenLayers layers
        fieldmap=provider.fields() # this function will crash on raster layers
        return fieldmap
    except:
        QgsMessageLog.logMessage("Could not get attributes of layer {}".format(layerId))
        return None