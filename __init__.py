# -*- coding: UTF-8 -*-
from timemanager import timemanager

def name():
    return "TimeManager"

def description():
    return "The aim of TimeManager plugin for QGIS is to provide comfortable browsing through temporal geodata. A dock widget provides a time slider and a configuration dialog for your layers to manage."

def version():
    return "Version 0.6"

def qgisMinimumVersion():
    return '1.6.0' 

def authorName():
    return "Anita Graser"

def classFactory(iface):
    return timemanager(iface)

def icon():
    return "icon.png"

def experimental():
    return True

def homepage():
    return "https://github.com/anitagraser/TimeManager"
    
def tracker():
    return "https://github.com/anitagraser/TimeManager"
    
def repository():
    return 'http://plugins.qgis.org/plugins/'
    
