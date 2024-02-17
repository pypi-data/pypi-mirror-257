# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

"""
Application to patch a NXtomo entry. invalidating some frame or adding some.

.. code-block:: bash

    usage: nxtomomill patch-nx [-h] [--darks-at-start DARKS_AT_START] [--darks-at-end DARKS_AT_END] [--flats-at-start FLATS_AT_START] [--flats-at-end FLATS_AT_END] [--invalid-frames INVALID_FRAMES]
                               [--update-to-projection UPDATE_TO_PROJECTION] [--update-to-dark UPDATE_TO_DARK] [--update-to-flat UPDATE_TO_FLAT] [--update-to-alignment UPDATE_TO_ALIGNMENT] [--embed-data]
                               file_path entry

    Insert dark and / or flat frames and metadata into anexisting NXTomo file from url(s).

    positional arguments:
      file_path             NXTomo file to patch
      entry                 entry in the provided file

    optional arguments:
      -h, --help            show this help message and exit
      --darks-at-start DARKS_AT_START, --darks-start DARKS_AT_START
                            url to the dataset containing darks to be store atthe beginning. url should be providing the "default?silx way": silx:///data/image.edf?path=/scan_0/detector/data (see
                            www.silx.org/doc/silx/latest/modules/io/url.html?highlight=dataurl#silx.io.url.DataUrl)of just by giving dataset_path@file_path
      --darks-at-end DARKS_AT_END, --darks-end DARKS_AT_END
                            url to the dataset containing darks to be store atthe end.url should be providing the "default?silx way": silx:///data/image.edf?path=/scan_0/detector/data (see
                            www.silx.org/doc/silx/latest/modules/io/url.html?highlight=dataurl#silx.io.url.DataUrl)of just by giving dataset_path@file_path
      --flats-at-start FLATS_AT_START, --flats-start FLATS_AT_START
                            url to the dataset containing flats to be store atthe beginning of the acquisition sequence (made before projections acquisition). url should be providing the "default?silx way":
                            silx:///data/image.edf?path=/scan_0/detector/data (see www.silx.org/doc/silx/latest/modules/io/url.html?highlight=dataurl#silx.io.url.DataUrl)of just by giving dataset_path@file_path
      --flats-at-end FLATS_AT_END, --flats-end FLATS_AT_END
                            url to the dataset containing flats to be store atthe beginning of end of the sequence (made before projections acquisition). url should be providing the "default?silx way":
                            silx:///data/image.edf?path=/scan_0/detector/data (see www.silx.org/doc/silx/latest/modules/io/url.html?highlight=dataurl#silx.io.url.DataUrl)of just by giving dataset_path@file_path
      --invalid-frames INVALID_FRAMES
                            Define the set of frames to be mark as invalid. Frames can be provided two ways: - has a list: frame_index_1,frame_index_2 - has a python slice: from:to:steps
      --update-to-projection UPDATE_TO_PROJECTION, --update-to-proj UPDATE_TO_PROJECTION
                            Define the set of frames to be mark as projection. Frames can be provided two ways: - has a list: frame_index_1,frame_index_2 - has a python slice: from:to:steps
      --update-to-dark UPDATE_TO_DARK
                            Define the set of frames to be mark as dark. Frames can be provided two ways: - has a list: frame_index_1,frame_index_2 - has a python slice: from:to:steps
      --update-to-flat UPDATE_TO_FLAT
                            Define the set of frames to be mark as flat. Frames can be provided two ways: - has a list: frame_index_1,frame_index_2 - has a python slice: from:to:steps
      --update-to-alignment UPDATE_TO_ALIGNMENT
                            Define the set of frames to be mark as alignment. Frames can be provided two ways: - has a list: frame_index_1,frame_index_2 - has a python slice: from:to:steps
      --embed-data          Embed data from url in the file if not already inside

"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "12/10/2020"

import argparse
import logging
import os

from silx.io.url import DataUrl
from silx.utils.enum import Enum as _Enum
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan

from nxtomomill import utils
from nxtomo.nxobject.nxdetector import ImageKey

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


_SILX_DATA_URL = "www.silx.org/doc/silx/latest/modules/io/url.html?highlight=dataurl#silx.io.url.DataUrl"


_INFO_URL = (
    'url should be providing the "default?silx way": '
    "silx:///data/image.edf?path=/scan_0/detector/data "
    f"(see {_SILX_DATA_URL})"
    "of just by giving dataset_path@file_path"
)


class _ImageKeyName(_Enum):
    ALIGNMENT = "alignment"
    PROJECTION = "projection"
    FLAT_FIELD = "flat"
    DARK_FIELD = "dark"
    INVALID = "invalid"

    @staticmethod
    def to_image_key(image_key) -> ImageKey:
        image_key = _ImageKeyName.from_value(image_key.lower())
        if image_key is _ImageKeyName.ALIGNMENT:
            return ImageKey.ALIGNMENT
        elif image_key is _ImageKeyName.PROJECTION:
            return ImageKey.PROJECTION
        elif image_key is _ImageKeyName.DARK_FIELD:
            return ImageKey.DARK_FIELD
        elif image_key is _ImageKeyName.FLAT_FIELD:
            return ImageKey.FLAT_FIELD
        elif image_key is _ImageKeyName.INVALID:
            return ImageKey.INVALID
        else:
            raise ValueError(f"{image_key} not handled")


_INFO_FRAME_INPUT = (
    "Frames can be provided three ways: \n"
    "- has a list: frame_index_1,frame_index_2\n"
    "- has a python slice: from:to:steps\n"
    f"- has an image key value. Valid values are {_ImageKeyName.values()}\n"
)


def _extract_data_url(url_as_a_str):
    """
    Extract url from a string
    """
    if url_as_a_str is None:
        return None
    elif "@" in url_as_a_str:
        try:
            entry, file_path = url_as_a_str.split("@")
        except Exception:
            _logger.error(f"Fail to create an url from {url_as_a_str}. {_INFO_URL}")
            return None
        else:
            url = DataUrl(file_path=file_path, data_path=entry, scheme="silx")
            return url
    else:
        try:
            url = DataUrl(path=url_as_a_str)
        except Exception as e:
            _logger.error(
                f"Fail to create an url from {url_as_a_str}."
                f"Reason is {e}. For more information see {_SILX_DATA_URL}"
            )
            return None
        else:
            return url


def _get_slice_to_modify(slice_as_str, master_file, entry):
    """
    Return a list of int or a `slice` from  slice_as_str
    :param slice_as_str:
    :return: slice to be modify on the image_key and image_key_control dataset
    :rtype: Union[None, slice, list]
    """
    if slice_as_str is None:
        return None
    elif slice_as_str.lower() in _ImageKeyName.values():
        image_key = _ImageKeyName.to_image_key(slice_as_str)
        scan = NXtomoScan(master_file, entry)
        frames = scan.frames
        slices = []
        for frame in frames:
            if frame.image_key is image_key:
                slices.append(frame.index)
        return slices
    elif ":" in slice_as_str:
        elmts = slice_as_str.split(":")

        def get_value(index):
            if index >= len(elmts):
                return None
            elif elmts[index] == "":
                return None
            else:
                return int(elmts[index])

        from_ = get_value(0)
        to_ = get_value(1)
        step = get_value(2)
        return slice(from_, to_, step)
    else:
        return [int(index) for index in slice_as_str.split(",")]


def main(argv):
    """ """
    parser = argparse.ArgumentParser(
        description="Insert dark and / or flat frames and metadata into an"
        "existing NXTomo file from url(s)."
    )
    parser.add_argument("file_path", help="NXTomo file to patch")
    parser.add_argument("entry", help="entry in the provided file")

    # dark and flat options
    parser.add_argument(
        "--darks-at-start",
        "--darks-start",
        default=None,
        help="url to the dataset containing darks to be store at"
        "the beginning. " + _INFO_URL,
    )
    parser.add_argument(
        "--darks-at-end",
        "--darks-end",
        default=None,
        help="url to the dataset containing darks to be store at"
        "the end." + _INFO_URL,
    )
    parser.add_argument(
        "--flats-at-start",
        "--flats-start",
        default=None,
        help="url to the dataset containing flats to be store at"
        "the beginning of the acquisition sequence (made before "
        "projections acquisition). " + _INFO_URL,
    )
    parser.add_argument(
        "--flats-at-end",
        "--flats-end",
        default=None,
        help="url to the dataset containing flats to be store at"
        "the beginning of end of the sequence (made before "
        "projections acquisition). " + _INFO_URL,
    )

    # modify frame type option
    parser.add_argument(
        "--invalid-frames",
        default=None,
        help="Define the set of frames to be mark as invalid. " + _INFO_FRAME_INPUT,
    )
    parser.add_argument(
        "--update-to-projection",
        "--update-to-proj",
        default=None,
        help="Define the set of frames to be mark as projection. "
        "" + _INFO_FRAME_INPUT,
    )
    parser.add_argument(
        "--update-to-dark",
        default=None,
        help="Define the set of frames to be mark as dark. " + _INFO_FRAME_INPUT,
    )
    parser.add_argument(
        "--update-to-flat",
        default=None,
        help="Define the set of frames to be mark as flat. " + _INFO_FRAME_INPUT,
    )
    parser.add_argument(
        "--update-to-alignment",
        default=None,
        help="Define the set of frames to be mark as alignment. "
        "" + _INFO_FRAME_INPUT,
    )
    parser.add_argument(
        "--embed-data",
        default=False,
        action="store_true",
        help="Embed data from url in the file if not already inside",
    )

    options = parser.parse_args(argv[1:])

    # get information for adding dark / flat
    darks_start_url = _extract_data_url(options.darks_at_start)
    darks_end_url = _extract_data_url(options.darks_at_end)
    flat_start_url = _extract_data_url(options.flats_at_start)
    flat_end_url = _extract_data_url(options.flats_at_end)

    patch_det_data = darks_start_url or flat_start_url or flat_end_url or darks_end_url

    # get information for modifying image_key
    slice_to_update_to_dark = _get_slice_to_modify(
        options.update_to_dark, master_file=options.file_path, entry=options.entry
    )
    slice_to_update_to_flat = _get_slice_to_modify(
        options.update_to_flat, master_file=options.file_path, entry=options.entry
    )
    slice_to_update_to_projection = _get_slice_to_modify(
        options.update_to_projection, master_file=options.file_path, entry=options.entry
    )
    slice_to_update_to_alignment = _get_slice_to_modify(
        options.update_to_alignment, master_file=options.file_path, entry=options.entry
    )
    slice_to_invalid = _get_slice_to_modify(
        options.invalid_frames, master_file=options.file_path, entry=options.entry
    )
    patch_image_key = (
        slice_to_update_to_dark
        or slice_to_update_to_flat
        or slice_to_update_to_projection
        or slice_to_update_to_alignment
        or slice_to_invalid
    )

    if patch_det_data and patch_image_key:
        _logger.info(
            "Both adding dark / flat and modifying `image_key` / "
            "`image_key_control` are requested. Will first add "
            "dark / flat then modify `image_key` / "
            "`image_key_control`."
        )

    elif not (patch_det_data or patch_image_key):
        _logger.warning(
            "No url provided for dark or flats or frame type to "
            "modify. Nothing to be done."
        )
    elif not utils.is_nx_tomo_entry(file_path=options.file_path, entry=options.entry):
        _logger.error(
            f"{options.entry}@{options.file_path} is not recognized as a valid NXTomo entry."
        )
    elif not os.access(options.file_path, os.W_OK):
        _logger.error(f"You don't have rights to write on {options.file_path}.")
    else:
        slices_patch = {
            ImageKey.ALIGNMENT: slice_to_update_to_alignment,
            ImageKey.PROJECTION: slice_to_update_to_projection,
            ImageKey.FLAT_FIELD: slice_to_update_to_flat,
            ImageKey.DARK_FIELD: slice_to_update_to_dark,
            ImageKey.INVALID: slice_to_invalid,
        }
        if patch_image_key:
            _logger.info("start updating frames")

        for image_key_type, frames_to_update in slices_patch.items():
            if frames_to_update is None:
                continue
            utils.change_image_key_control(
                file_path=options.file_path,
                entry=options.entry,
                frames_indexes=frames_to_update,
                image_key_control_value=image_key_type,
                logger=_logger,
            )

        if patch_det_data:
            _logger.info("start adding dark and flat field")
            utils.add_dark_flat_nx_file(
                file_path=options.file_path,
                entry=options.entry,
                darks_start=darks_start_url,
                flats_start=flat_start_url,
                darks_end=darks_end_url,
                flats_end=flat_end_url,
                embed_data=True,
                logger=_logger,
            )
