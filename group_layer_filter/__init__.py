def classFactory(iface):
    """Load GroupLayerFilterPlugin class from file group_filter_plugin.py.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .group_filter_plugin import GroupLayerFilterPlugin
    return GroupLayerFilterPlugin(iface)
