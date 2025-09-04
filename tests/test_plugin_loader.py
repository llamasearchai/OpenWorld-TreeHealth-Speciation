from openworld_tshm.plugin_loader import load_plugins, get_plugin_by_name


def test_plugin_loader_fallback_and_lookup():
    plugins = load_plugins()
    names = {p.name for p in plugins}
    assert {"lidar_laspy", "multispectral_rasterio", "field_csv"}.issubset(names)
    p = get_plugin_by_name("lidar_laspy")
    assert p is not None


