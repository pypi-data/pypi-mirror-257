import os
from math import ceil
from multiprocessing.pool import ThreadPool
import numpy as np
from silx.io.dictdump import h5todict
from tomoscan.io import HDF5File
from .utils import get_compacted_dataslices, convert_dict_values
from ..misc.binning import binning as image_binning
from ..utils import subsample_dict, get_3D_subregion, get_num_threads

try:
    from fabio.edfimage import EdfImage
except ImportError:
    EdfImage = None


class Reader:
    """
    Abstract class for various file readers.
    """

    def __init__(self, sub_region=None):
        """
        Parameters
        ----------
        sub_region: tuple, optional
            Coordinates in the form (start_x, end_x, start_y, end_y), to read
            a subset of each frame. It can be used for Regions of Interest (ROI).
            Indices start at zero !
        """
        self._set_default_parameters(sub_region)

    def _set_default_parameters(self, sub_region):
        self._set_subregion(sub_region)

    def _set_subregion(self, sub_region):
        self.sub_region = sub_region
        if sub_region is not None:
            start_x, end_x, start_y, end_y = sub_region
            self.start_x = start_x
            self.end_x = end_x
            self.start_y = start_y
            self.end_y = end_y
        else:
            self.start_x = 0
            self.end_x = None
            self.start_y = 0
            self.end_y = None

    def get_data(self, data_url):
        """
        Get data from a silx.io.url.DataUrl
        """
        raise ValueError("Base class")

    def release(self):
        """
        Release the file if needed.
        """
        pass


class NPReader(Reader):
    multi_load = True

    def __init__(self, sub_region=None, mmap=True):
        """
        Reader for NPY/NPZ files. Mostly used for internal development.
        Please refer to the documentation of nabu.io.reader.Reader
        """
        super().__init__(sub_region=sub_region)
        self._file_desc = {}
        self._set_mmap(mmap)

    def _set_mmap(self, mmap):
        self.mmap_mode = "r" if mmap else None

    def _open(self, data_url):
        file_path = data_url.file_path()
        file_ext = self._get_file_type(file_path)
        if file_ext == "npz":
            if file_path not in self._file_desc:
                self._file_desc[file_path] = np.load(file_path, mmap_mode=self.mmap_mode)
            data_ref = self._file_desc[file_path][data_url.data_path()]
        else:
            data_ref = np.load(file_path, mmap_mode=self.mmap_mode)
        return data_ref

    @staticmethod
    def _get_file_type(fname):
        if fname.endswith(".npy"):
            return "npy"
        elif fname.endswith(".npz"):
            return "npz"
        else:
            raise ValueError("Not a numpy file: %s" % fname)

    def get_data(self, data_url):
        data_ref = self._open(data_url)
        data_slice = data_url.data_slice()
        if data_slice is None:
            res = data_ref[self.start_y : self.end_y, self.start_x : self.end_x]
        else:
            res = data_ref[data_slice, self.start_y : self.end_y, self.start_x : self.end_x]
        return res

    def release(self):
        for fname, fdesc in self._file_desc.items():
            if fdesc is not None:
                fdesc.close()
                self._file_desc[fname] = None

    def __del__(self):
        self.release()


class EDFReader(Reader):
    multi_load = False  # not implemented

    def __init__(self, sub_region=None):
        """
        A class for reading series of EDF Files.
        Multi-frames EDF are not supported.
        """
        if EdfImage is None:
            raise ImportError("Need fabio to use this reader")
        super().__init__(sub_region=sub_region)
        self._reader = EdfImage()
        self._first_fname = None

    def read(self, fname):
        if self._first_fname is None:
            self._first_fname = fname
            self._reader.read(fname)
        if self.sub_region is None:
            data = self._reader.data
        else:
            data = self._reader.fast_read_roi(fname, (slice(self.start_y, self.end_y), slice(self.start_x, self.end_x)))
        self._reader.close()
        return data

    def get_data(self, data_url):
        return self.read(data_url.file_path())


class HDF5Reader(Reader):
    multi_load = True

    def __init__(self, sub_region=None):
        """
        A class for reading a HDF5 File.
        """
        super().__init__(sub_region=sub_region)
        self._file_desc = {}

    def _open(self, file_path):
        if file_path not in self._file_desc:
            self._file_desc[file_path] = HDF5File(file_path, "r", swmr=True)

    def get_data(self, data_url):
        file_path = data_url.file_path()
        self._open(file_path)
        h5dataset = self._file_desc[file_path][data_url.data_path()]
        data_slice = data_url.data_slice()
        if data_slice is None:
            res = h5dataset[self.start_y : self.end_y, self.start_x : self.end_x]
        else:
            res = h5dataset[data_slice, self.start_y : self.end_y, self.start_x : self.end_x]

        return res

    def release(self):
        for fname, fdesc in self._file_desc.items():
            if fdesc is not None:
                try:
                    fdesc.close()
                    self._file_desc[fname] = None
                except Exception as exc:
                    print("Error while closing %s: %s" % (fname, str(exc)))

    def __del__(self):
        self.release()


class HDF5Loader:
    """
    An alternative class to HDF5Reader where information is first passed at class instantiation
    """

    def __init__(self, fname, data_path, sub_region=None, data_buffer=None, pre_allocate=True, dtype="f"):
        self.fname = fname
        self.data_path = data_path
        self._set_subregion(sub_region)
        if not ((data_buffer is not None) ^ (pre_allocate is True)):
            raise ValueError("Please provide either 'data_buffer' or 'pre_allocate'")
        self.data = data_buffer
        self._loaded = False
        if pre_allocate:
            expected_shape = get_hdf5_dataset_shape(fname, data_path, sub_region=sub_region)
            self.data = np.zeros(expected_shape, dtype=dtype)

    def _set_subregion(self, sub_region):
        self.sub_region = sub_region
        if sub_region is not None:
            start_z, end_z, start_y, end_y, start_x, end_x = sub_region
            self.start_x, self.end_x = start_x, end_x
            self.start_y, self.end_y = start_y, end_y
            self.start_z, self.end_z = start_z, end_z
        else:
            self.start_x, self.end_x = None, None
            self.start_y, self.end_y = None, None
            self.start_z, self.end_z = None, None

    def load_data(self, force_load=False):
        if self._loaded and not force_load:
            return self.data
        with HDF5File(self.fname, "r") as fdesc:
            if self.data is None:
                self.data = fdesc[self.data_path][
                    self.start_z : self.end_z, self.start_y : self.end_y, self.start_x : self.end_x
                ]
            else:
                self.data[:] = fdesc[self.data_path][
                    self.start_z : self.end_z, self.start_y : self.end_y, self.start_x : self.end_x
                ]
        self._loaded = True
        return self.data


class ChunkReader:
    """
    A reader of chunk of images.
    """

    def __init__(
        self,
        files,
        sub_region=None,
        detector_corrector=None,
        pre_allocate=True,
        data_buffer=None,
        convert_float=False,
        shape=None,
        dtype=None,
        binning=None,
        dataset_subsampling=None,
        num_threads=None,
    ):
        """
        Initialize a "ChunkReader". A chunk is a stack of images.

        Parameters
        ----------
        files: dict
            Dictionary where the key is the file/data index, and the value is a
            silx.io.url.DataUrl pointing to the data.
            The dict must contain only the files which shall be used !
            Note: the shape and data type is infered from the first data file.
        sub_region: tuple, optional
            If provided, this must be a tuple in the form
            (start_x, end_x, start_y, end_y). Each image will be cropped to this
            region. This is used to specify a chunk of files.
            Each of the parameters can be None, in this case the default start
            and end are taken in each dimension.
        pre_allocate: bool
            Whether to pre-allocate data before reading.
        data_buffer: array-like, optional
            If `pre_allocate` is set to False, this parameter has to be provided.
            It is an array-like object which will hold the data.
        convert_float: bool
            Whether to convert data to float32, regardless of the input data type.
        shape: tuple, optional
            Shape of each image. If not provided, it is inferred from the first image
            in the collection.
        dtype: `numpy.dtype`, optional
            Data type of each image. If not provided, it is inferred from the first image
            in the collection.
        binning: int or tuple of int, optional
            Whether to bin the data. If multi-dimensional binning is done,
            the parameter must be in the form (binning_x, binning_y).
            Each image will be binned by these factors.
        dataset_subsampling: int or tuple, optional
            Subsampling factor when reading the images.
            If an integer `n` is provided, then one image out of `n` will be read.
            If a tuple of integers (step, begin) is given, the data is read as data[begin::step]
        num_threads: int, optional
            Number of threads to use for binning the data.
            Default is to use all available threads.
            This parameter has no effect when binning is disabled.

        Notes
        ------
        The files are provided as a collection of `silx.io.DataURL`. The file type
        is inferred from the extension.

        Binning is different from subsampling. Using binning will not speed up
        the data retrieval (quite the opposite), since the whole (subregion of) data
        is read and then binning is performed.
        """
        self.detector_corrector = detector_corrector
        self._get_reader_class(files)
        self.dataset_subsampling = dataset_subsampling
        self.num_threads = get_num_threads(num_threads)
        self._set_files(files)
        self._get_shape_and_dtype(shape, dtype, binning)
        self._set_subregion(sub_region)
        self._init_reader()
        self._loaded = False
        self.convert_float = convert_float
        if convert_float:
            self.out_dtype = np.float32
        else:
            self.out_dtype = self.dtype
        if not ((data_buffer is not None) ^ (pre_allocate is True)):
            raise ValueError("Please provide either 'data_buffer' or 'pre_allocate'")
        self.files_data = data_buffer
        if data_buffer is not None:
            # overwrite out_dtype
            self.out_dtype = data_buffer.dtype
            if data_buffer.shape != self.chunk_shape:
                raise ValueError("Expected shape %s but got %s" % (self.shape, data_buffer.shape))
        if pre_allocate:
            self.files_data = np.zeros(self.chunk_shape, dtype=self.out_dtype)
        if (self.binning is not None) and (np.dtype(self.out_dtype).kind in ["u", "i"]):
            raise ValueError(
                "Output datatype cannot be integer when using binning. Please set the 'convert_float' parameter to True or specify a 'data_buffer'."
            )

    def _set_files(self, files):
        if len(files) == 0:
            raise ValueError("Expected at least one data file")
        self._files_begin_idx = 0
        if isinstance(self.dataset_subsampling, (tuple, list)):
            self._files_begin_idx = self.dataset_subsampling[1]
            self.dataset_subsampling = self.dataset_subsampling[0]
        self.n_files = len(files)
        self.files = files
        self._sorted_files_indices = sorted(files.keys())
        self._fileindex_to_idx = dict.fromkeys(self._sorted_files_indices)
        self._configure_subsampling()

    def _infer_file_type(self, files):
        fname = files[sorted(files.keys())[0]].file_path()
        ext = os.path.splitext(fname)[-1].replace(".", "")
        if ext not in Readers:
            raise ValueError("Unknown file format %s. Supported formats are: %s" % (ext, str(Readers.keys())))
        return ext

    def _get_reader_class(self, files):
        ext = self._infer_file_type(files)
        reader_class = Readers[ext]
        self._reader_class = reader_class

    def _get_shape_and_dtype(self, shape, dtype, binning):
        if shape is None or dtype is None:
            shape, dtype = self._infer_shape_and_dtype()
        assert len(shape) == 2, "Expected the shape of an image (2-tuple)"
        self.shape_total = shape
        self.dtype = dtype
        self._set_binning(binning)

    def _configure_subsampling(self):
        dataset_subsampling = self.dataset_subsampling
        self.files_subsampled = self.files
        if dataset_subsampling is not None and dataset_subsampling > 1:
            self.files_subsampled = subsample_dict(self.files, dataset_subsampling)
            self.n_files = len(self.files_subsampled)
            if not (self._reader_class.multi_load):
                # 3D loading not supported for this reader.
                # Data is loaded frames by frame, so subsample directly self.files
                self.files = self.files_subsampled
                self._sorted_files_indices = sorted(self.files.keys())
                self._fileindex_to_idx = dict.fromkeys(self._sorted_files_indices)

    def _infer_shape_and_dtype(self):
        self._reader_entire_image = self._reader_class()
        first_file_dataurl = self.files[self._sorted_files_indices[0]]
        first_file_data = self._reader_entire_image.get_data(first_file_dataurl)
        return first_file_data.shape, first_file_data.dtype

    def _set_subregion(self, sub_region):
        sub_region = sub_region or (None, None, None, None)
        start_x, end_x, start_y, end_y = sub_region
        if start_x is None:
            start_x = 0
        if start_y is None:
            start_y = 0
        if end_x is None:
            end_x = self.shape_total[1]
        if end_y is None:
            end_y = self.shape_total[0]
        self.sub_region = (start_x, end_x, start_y, end_y)
        self.shape = (end_y - start_y, end_x - start_x)
        if self.binning is not None:
            self.shape = (self.shape[0] // self.binning[1], self.shape[1] // self.binning[0])
        self.chunk_shape = (self.n_files,) + self.shape
        if self.detector_corrector is not None:
            self.detector_corrector.set_sub_region_transformation(target_sub_region=self.sub_region)

    def _init_reader(self):
        # instantiate reader with user params
        if self.detector_corrector is not None:
            adapted_subregion = self.detector_corrector.get_adapted_subregion(self.sub_region)
        else:
            adapted_subregion = self.sub_region

        self.file_reader = self._reader_class(sub_region=adapted_subregion)

    def _set_binning(self, binning):
        if binning is None:
            self.binning = None
            return
        if np.isscalar(binning):
            binning = (binning, binning)
        else:
            assert len(binning) == 2, "Expected binning in the form (binning_x, binning_y)"
        if binning[0] == 1 and binning[1] == 1:
            self.binning = None
            return
        for b in binning:
            if int(b) != b:
                raise ValueError("Expected an integer number for binning values, but got %s" % binning)
        self.binning = binning

    def get_data(self, file_url):
        """
        Get the data associated to a file url.
        """
        arr = self.file_reader.get_data(file_url)

        if arr.ndim == 2:
            if self.detector_corrector is not None:
                arr = self.detector_corrector.transform(arr)
            if self.binning is not None:
                arr = image_binning(arr, self.binning[::-1])

        else:
            if self.detector_corrector is not None:
                if self.detector_corrector is not None:
                    _, (
                        src_x_start,
                        src_x_end,
                        src_z_start,
                        src_z_end,
                    ) = self.detector_corrector.get_actual_shapes_source_target()

                    arr_target = np.empty([len(arr), src_z_end - src_z_start, src_x_end - src_x_start], "f")

                def apply_corrector(i_img_tuple):
                    i, img = i_img_tuple
                    arr_target[i] = self.detector_corrector.transform(img)

                with ThreadPool(self.num_threads) as tp:
                    tp.map(apply_corrector, enumerate(arr))
                arr = arr_target
            if self.binning is not None:
                nz = arr.shape[0]
                res = np.zeros((nz,) + image_binning(arr[0], self.binning[::-1]).shape, dtype="f")

                def apply_binning(img_res_tuple):
                    img, res = img_res_tuple
                    res[:] = image_binning(img, self.binning[::-1])

                with ThreadPool(self.num_threads) as tp:
                    tp.map(apply_binning, zip(arr, res))
                arr = res

        return arr

    def _load_single(self):
        for i, fileidx in enumerate(self._sorted_files_indices):
            file_url = self.files[fileidx]
            self.files_data[i] = self.get_data(file_url)
            self._fileindex_to_idx[fileidx] = i

    def _load_multi(self):
        urls_compacted = get_compacted_dataslices(
            self.files, subsampling=self.dataset_subsampling, begin=self._files_begin_idx
        )
        loaded = {}
        start_idx = 0
        sorted_files_indices = sorted(urls_compacted.keys())
        for idx in sorted_files_indices:
            url = urls_compacted[idx]
            url_str = str(url)
            is_loaded = loaded.get(url_str, False)
            if is_loaded:
                continue
            ds = url.data_slice()
            delta_z = ds.stop - ds.start
            if ds.step is not None and ds.step > 1:
                delta_z = ceil(delta_z / ds.step)
            end_idx = start_idx + delta_z
            self.files_data[start_idx:end_idx] = self.get_data(url)
            start_idx += delta_z
            loaded[url_str] = True

    def load_files(self, overwrite: bool = False):
        """
        Load the files whose links was provided at class instantiation.

        Parameters
        -----------
        overwrite: bool, optional
            Whether to force reloading the files if already loaded.
        """
        if self._loaded and not (overwrite):
            raise ValueError("Radios were already loaded. Call load_files(overwrite=True) to force reloading")
        if self.file_reader.multi_load:
            self._load_multi()
        else:
            self._load_single()
        self._loaded = True

    load_data = load_files

    @property
    def data(self):
        return self.files_data


Readers = {
    "edf": EDFReader,
    "hdf5": HDF5Reader,
    "h5": HDF5Reader,
    "nx": HDF5Reader,
    "npz": NPReader,
    "npy": NPReader,
}


def load_images_from_dataurl_dict(data_url_dict, **chunk_reader_kwargs):
    """
    Load a dictionary of dataurl into numpy arrays.

    Parameters
    ----------
    data_url_dict: dict
        A dictionary where the keys are integers (the index of each image in the dataset),
        and the values are numpy.ndarray (data_url_dict).

    Other parameters
    -----------------
    chunk_reader_kwargs: params
        Named parameters passed to `nabu.io.reader.ChunkReader`.

    Returns
    --------
    res: dict
        A dictionary where the keys are the same as `data_url_dict`, and the values are numpy arrays.
    """
    chunk_reader = ChunkReader(data_url_dict, **chunk_reader_kwargs)
    img_dict = {}
    for img_idx, img_url in data_url_dict.items():
        img_dict[img_idx] = chunk_reader.get_data(img_url)
    return img_dict


def load_images_stack_from_hdf5(fname, h5_data_path, sub_region=None):
    """
    Load a 3D dataset from a HDF5 file.

    Parameters
    -----------
    fname: str
        File path
    h5_data_path: str
        Data path within the HDF5 file
    sub_region: tuple, optional
        Tuple indicating which sub-volume to load, in the form (xmin, xmax, ymin, ymax, zmin, zmax)
        where the 3D dataset has the python shape (N_Z, N_Y, N_X).
        This means that the data will be loaded as `data[zmin:zmax, ymin:ymax, xmin:xmax]`.
    """
    xmin, xmax, ymin, ymax, zmin, zmax = get_3D_subregion(sub_region)
    with HDF5File(fname, "r") as f:
        d_ptr = f[h5_data_path]
        data = d_ptr[zmin:zmax, ymin:ymax, xmin:xmax]
    return data


def get_hdf5_dataset_shape(fname, h5_data_path, sub_region=None):
    zmin, zmax, ymin, ymax, xmin, xmax = get_3D_subregion(sub_region)
    with HDF5File(fname, "r") as f:
        d_ptr = f[h5_data_path]
        shape = d_ptr.shape
    n_z, n_y, n_x = shape
    # perhaps there is more elegant
    res_shape = []
    for n, bounds in zip([n_z, n_y, n_x], ((zmin, zmax), (ymin, ymax), (xmin, xmax))):
        res_shape.append(np.arange(n)[bounds[0] : bounds[1]].size)
    return tuple(res_shape)


def check_virtual_sources_exist(fname, data_path):
    with HDF5File(fname, "r") as f:
        if data_path not in f:
            print("No dataset %s in file %s" % (data_path, fname))
            return False
        dptr = f[data_path]
        if not dptr.is_virtual:
            return True
        for vsource in dptr.virtual_sources():
            vsource_fname = os.path.join(os.path.dirname(dptr.file.filename), vsource.file_name)
            if not os.path.isfile(vsource_fname):
                print("No such file: %s" % vsource_fname)
                return False
            elif not check_virtual_sources_exist(vsource_fname, vsource.dset_name):
                print("Error with virtual source %s" % vsource_fname)
                return False
    return True


def import_h5_to_dict(h5file, h5path, asarray=False):
    """
    Wrapper on top of silx.io.dictdump.dicttoh5 replacing "None" with None

    Parameters
    -----------
    h5file: str
        File name
    h5path: str
        Path in the HDF5 file
    asarray: bool, optional
        Whether to convert each numeric value to an 0D array. Default is False.
    """
    dic = h5todict(h5file, path=h5path, asarray=asarray)
    modified_dic = convert_dict_values(dic, {"None": None}, bytes_tostring=True)
    return modified_dic
