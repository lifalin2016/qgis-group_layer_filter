# Group Layer Filter

A small QGIS plugin that lets you apply one identical attribute filter to
every vector layer inside a layer group, in one step.

## Install

1. Zip the `group_layer_filter` folder (or use the `.zip` you were given).
2. In QGIS: **Plugins > Manage and Install Plugins > Install from ZIP**,
   then select the zip file. QGIS will unpack it into your profile's
   `plugins` folder for you.
   - Alternatively, unzip it manually into your QGIS profile's plugin
     folder, e.g. on Windows:
     `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
     or on Linux/macOS:
     `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
3. Enable it in **Plugins > Manage and Install Plugins > Installed** if it
   isn't already active.

## Use

1. In the **Layers** panel, right-click a **group** (not an individual
   layer).
2. Choose **Set Filter on Group Layers...**.
3. Enter a filter expression as your data provider's subset string, e.g.:
   - `"status" = 'active'`
   - `"year" >= 2020 AND "region" = 'North'`
4. Click **OK**. The filter is applied to every vector layer directly in
   that group and in any nested subgroups.
5. To remove the filter again, reopen the dialog on the same group and
   clear the text box, then click OK.

## Notes / limitations

- The filter text is passed straight to each layer's
  `setSubsetString()`. That means the expression must be valid in that
  layer's data provider dialect (PostgreSQL/PostGIS SQL, OGR SQL for
  Shapefiles/GeoPackages, etc.), and referenced field names must exist on
  every layer in the group. If a layer rejects the filter (e.g. a missing
  field), the plugin applies the filter to the layers that accept it and
  then lists the ones that failed.
- Only vector layers are affected; raster layers in the group are
  skipped.
- If every layer in the group currently shares the same filter, the
  dialog pre-fills it so you can tweak and reapply it.
