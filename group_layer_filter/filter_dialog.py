# -*- coding: utf-8 -*-
"""Small dialog for entering the filter expression to apply to a group."""

from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
)


class FilterDialog(QDialog):
    """Simple dialog with a single text field for the filter expression."""

    def __init__(self, group_name, layer_names, initial_text="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Filter on Group Layers")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        intro = QLabel(
            "Group: <b>{0}</b><br>"
            "Layers that will receive this filter ({1}):<br>{2}".format(
                group_name,
                len(layer_names),
                ", ".join(layer_names) if layer_names else "<i>none found</i>",
            )
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        layout.addWidget(
            QLabel(
                "Filter expression (provider subset string, e.g. "
                '"status" = \'active\'). Leave empty to clear the filter:'
            )
        )

        self.line_edit = QLineEdit(self)
        self.line_edit.setText(initial_text)
        layout.addWidget(self.line_edit)

        note = QLabel(
            "Note: this is passed as-is to each layer's data provider "
            "(setSubsetString). Field names and SQL dialect must exist on "
            "and be understood by every layer in the group, since providers "
            "can differ (PostGIS, OGR/Shapefile/GeoPackage, etc.)."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(note)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def filter_text(self):
        return self.line_edit.text().strip()
