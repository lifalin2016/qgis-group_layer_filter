# -*- coding: utf-8 -*-
"""Group Layer Filter

Adds a right-click context menu entry to layer tree groups that lets you
apply one identical attribute filter (subset string) to every vector layer
inside that group, including nested subgroups.
"""

import os

from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import QgsLayerTreeGroup, QgsVectorLayer

from .filter_dialog import FilterDialog


class GroupLayerFilterPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.menu_action = None
        self._view = None

    # ------------------------------------------------------------------
    # QGIS plugin lifecycle
    # ------------------------------------------------------------------
    def initGui(self):
        self._view = self.iface.layerTreeView()
        self._view.contextMenuAboutToShow.connect(self.on_context_menu)

    def unload(self):
        if self._view is not None:
            try:
                self._view.contextMenuAboutToShow.disconnect(
                    self.on_context_menu
                )
            except (TypeError, RuntimeError):
                # already disconnected / view already destroyed
                pass
        self._view = None

    # ------------------------------------------------------------------
    # Context menu handling
    # ------------------------------------------------------------------
    def on_context_menu(self, menu):
        group = self._view.currentGroupNode()

        # Skip the invisible project root (it has no parent node); only
        # offer the action for a real, named group.
        if group is None or not isinstance(group, QgsLayerTreeGroup):
            return
        if group.parent() is None:
            return

        action = QAction("Set Filter on Group Layers...", menu)
        action.triggered.connect(lambda: self.run_filter_dialog(group))
        menu.addAction(action)

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------
    def collect_vector_layers(self, group):
        """Recursively collect vector layers under a QgsLayerTreeGroup."""
        layers = []
        for child in group.children():
            if isinstance(child, QgsLayerTreeGroup):
                layers.extend(self.collect_vector_layers(child))
            else:
                layer = child.layer()
                if isinstance(layer, QgsVectorLayer):
                    layers.append(layer)
        return layers

    def run_filter_dialog(self, group):
        layers = self.collect_vector_layers(group)
        layer_names = [layer.name() for layer in layers]

        # Pre-fill with the existing filter if every layer already shares
        # the same one; otherwise start blank.
        initial_text = ""
        if layers:
            subset_strings = {layer.subsetString() for layer in layers}
            if len(subset_strings) == 1:
                initial_text = next(iter(subset_strings))

        dialog = FilterDialog(
            group.name(), layer_names, initial_text, self.iface.mainWindow()
        )
        if not dialog.exec_():
            return

        expression = dialog.filter_text()

        if not layers:
            QMessageBox.information(
                self.iface.mainWindow(),
                "Group Layer Filter",
                "No vector layers were found in group '{0}'.".format(
                    group.name()
                ),
            )
            return

        failed = []
        for layer in layers:
            if not layer.setSubsetString(expression):
                failed.append(layer.name())

        if failed:
            QMessageBox.warning(
                self.iface.mainWindow(),
                "Group Layer Filter",
                "The filter was rejected by these layers (check field "
                "names / SQL syntax for their provider):\n\n"
                + "\n".join(failed),
            )
