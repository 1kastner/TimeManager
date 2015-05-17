from PyQt4.QtGui import QColor
from qgis._core import QgsMapLayerRegistry, QgsFields
from qgis.core import QgsRasterLayer
from logging import warn

__author__ = 'carolinux'


def getLayerAttributes(layerId):
    try:
        layer=QgsMapLayerRegistry.instance().mapLayers()[layerId]
        fieldmap = layer.pendingFields() 
        #TODO v1.7 figure out what to do for fields with fieldmap.fieldOrigin(idx) = QgsFields.OriginEdit/OriginExpression
        return fieldmap
    except:
        # OpenLayers, Raster layers don't work with this
        warn("Could not get attributes of layer {}".format(layerId))
        return None

def getAllLayerIds(filter_func):
    # FIXME Make this nicer
    res = []
    for (id, layer) in QgsMapLayerRegistry.instance().mapLayers().iteritems():
        if filter_func(layer):
            res.append(id)
    return res

def getLayerFromId(layerId):
    try:
        layer=QgsMapLayerRegistry.instance().mapLayers()[layerId]
        return layer
    except:
        warn("Could not get layer for id {}".format(layerId))
        return None

def isRaster(layer):
    return type(layer) == QgsRasterLayer

def doesLayerNameExist(name):
    return getIdFromLayerName(name) is not None

def getIdFromLayerName(layerName):
    # Important: If multiple layers with same name exist, it will return the first one it finds
    for (id, layer) in QgsMapLayerRegistry.instance().mapLayers().iteritems():
        if unicode(layer.name())==layerName:
            return id
    return None

def getLayerFromLayerName(layerName):
    # Important: If multiple layers with same name exist, it will return the first one it finds
    for (id, layer) in QgsMapLayerRegistry.instance().mapLayers().iteritems():
        if unicode(layer.name())==layerName:
            return layer
    return None

def getNameFromLayerId(layerId):
    layer =  QgsMapLayerRegistry.instance().mapLayers()[layerId]
    return unicode(layer.name())

def getLayerColor(layer):
    renderer = layer.rendererV2()
    symbol = renderer.symbol()
    return symbol.color().name()

def getLayerSize(layer):
    renderer = layer.rendererV2()
    symbol = renderer.symbol()
    return symbol.size()

def setLayerColor(layer, color_name):
    renderer = layer.rendererV2()
    symbol = renderer.symbol()
    symbol.setColor(QColor(color_name))


def setLayerSize(layer, size):
    renderer = layer.rendererV2()
    symbol = renderer.symbol()
    symbol.setSize(size)

def setLayerTransparency(layer, alpha):
    renderer = layer.rendererV2()
    symbol = renderer.symbol()
    symbol.setAlpha(alpha)

def refreshSymbols(iface, layer):
    iface.legendInterface().refreshLayerSymbology(layer)
    iface.mapCanvas().refresh()
