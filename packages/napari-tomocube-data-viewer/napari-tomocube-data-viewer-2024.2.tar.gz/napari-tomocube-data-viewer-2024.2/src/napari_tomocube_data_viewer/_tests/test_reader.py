import numpy as np
import h5py
from napari_tomocube_data_viewer import napari_get_reader


# tmp_path is a pytest fixture
def test_reader(tmp_path):
    """An example of how you might test your plugin."""

    # write some fake data using your supported file format
    my_test_file = str(tmp_path / "myfile.TCF")
    original_data = np.random.rand(20, 20, 20)
    with h5py.File(my_test_file,'w') as f:
        f.attrs['FormatVersion'] = np.array([b'1.2'], dtype='|S7')
        f.create_group("Data/3D")
        grp = f["Data/3D"]
        grp.attrs["DataCount"] = np.array([1],np.int64)
        grp.attrs["TimeInterval"] = np.array([1],np.int64)
        for axis in ("X","Y","Z"):
            grp.attrs[f"Size{axis}"] = np.array([20.])
            grp.attrs[f"Resolution{axis}"] = np.array([1.])
        grp["000000"] = original_data

    # try to read it back in
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure it's the same as it started
    np.testing.assert_allclose(original_data, layer_data_tuple[0])


def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None
