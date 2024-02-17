import logging
import typing

import npc_lims
import npc_sessions
import numpy as np
import zarr

from . import exceptions, models

logger = logging.getLogger(__name__)


def _get_timing_data(
    ephys_device_info: npc_sessions.EphysDeviceInfo,
) -> models.TimingData:
    """Gets timing data and path (isilon or s3)."""
    if ephys_device_info.compressed:
        path = ephys_device_info.compressed
        logger.debug("Opening zarr: %s" % path.path)
        return models.TimingData(
            data=zarr.open(path, mode="r")["traces_seg0"],
            path=path.path,
        )
    else:
        path = ephys_device_info.continuous / "continuous.dat"
        logger.debug("Opening memmap: %s" % path)
        return models.TimingData(
            data=np.memmap(
                path,
                dtype=np.int16,
                mode="r",
            ).reshape(-1, 384),
            path=path.path,
        )


def generate_timing_data(
    session_id: str,
) -> typing.Generator[tuple[models.TimingData, models.TimingData], None, None]:
    """Generates associated isilon and s3 data."""
    info = npc_lims.get_session_info(
        session=session_id,
    )
    if not info.is_uploaded:
        raise exceptions.ValidationException("Data not yet uploaded.")

    s3 = npc_sessions.Session(info)
    logger.debug("s3 session id: %s" % s3.id)
    isilon = npc_sessions.Session(info.allen_path)
    logger.debug("isilon session id: %s" % isilon.id)
    # if s3.id == isilon.id:
    #     raise exceptions.ValidationException(
    #         "Fetched s3 and isilon sessions are the same.")

    for timing_data in isilon.ephys_timing_data:
        try:
            logger.debug("isilon device name: %s" % timing_data.device.name)
            isilon_timing_data = _get_timing_data(timing_data.device)
            s3_device = next(
                d.device
                for d in s3.ephys_timing_data
                if d.device.name.lower() == timing_data.device.name.lower()
            )
            logger.debug("s3 device name: %s" % s3_device.name)
            s3_timing_data = _get_timing_data(s3_device)
            yield (
                isilon_timing_data,
                s3_timing_data,
            )
        except Exception:
            logger.error("Failed to get timing data.", exc_info=True)
            continue
