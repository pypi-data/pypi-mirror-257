"""Script to stitch fragments of rendered slices together according to user-specified options."""

from __future__ import annotations
import re
import os
import logging
from functools import partial
from typing import Optional
from dataclasses import dataclass

from pathlib import Path

import PIL
import imageio
import pandas as pd

from joblib import Parallel, delayed
from tqdm import tqdm
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s-%(levelname)s: %(message)s")


@dataclass
class SliceInfo:
    """Class representing information parsed from a single tile image filename."""

    simID: int
    regionID: int
    sliceNo: int
    xVal: float
    yVal: float

    @classmethod
    def fromParsed(
        cls,
        simID: int | str,
        regionID: int | str,
        sliceNo: int | str,
        xVal: float | str,
        yVal: float | str,
    ) -> SliceInfo:
        """Convert data from parsing information from a string into SliceInfo."""
        return SliceInfo(
            int(simID), int(regionID), int(sliceNo), float(xVal), float(yVal)
        )


def BuildSliceData(SourceDir: Path | str) -> pd.DataFrame:
    """
    Build a dataframe with parsed information about slices from the filenames in the source directory.

    :param SourceDir: Directory containing fragments of slice image to stitch.
    :type SourceDir: Path | str
    :rtype: pd.DataFrame
    """
    SourceDir = Path(SourceDir)

    sliceData: list[SliceInfo] = []

    fileNameRegex = re.compile(
        r"Simulation(\d+)_Region(\d+)_Slice(\d+)_X(-?\d+\.\d+)_Y(-?\d+\.\d+).png"
    )

    for filePath in SourceDir.glob("*.png"):
        matches = (fileNameRegex.findall(filePath.name))[0]
        if len(matches) != 5:
            logging.debug(
                f"Could not find all matches for {str(filePath)}, skipping..."
            )
            continue

        sliceData.append(SliceInfo.fromParsed(*matches))
    return pd.DataFrame(sliceData)


def MakeSliceGIF(baseDir: Path | str, simID: int, regionID: int):
    """
    Create a GIF out of slice images for specified simulation and region IDs.

    :param baseDir: Path to directory with stitched slice images.
    :type baseDir: Path | str
    :param simID: integer ID of the simulation.
    :type simID: int
    :param regionID: integer ID of the region.
    :type regionID: int
    """
    baseDir = Path(baseDir)

    GifFilepath = baseDir / f"Simulation{simID}_Region{regionID}.gif"

    sliceNoRegex = re.compile(r"Slice(\d+).png")

    with imageio.get_writer(GifFilepath, mode="I", loop=0) as Writer:
        sliceNos = sorted(
            [
                int(sliceNoRegex.findall(filepath.name)[0])
                for filepath in baseDir.glob(
                    f"Simulation{simID}_Region{regionID}_Slice*.png"
                )
            ]
        )
        for sliceNo in sliceNos:
            Filename = (
                baseDir / f"Simulation{simID}_Region{regionID}_Slice{sliceNo}.png"
            )
            Image = imageio.v3.imread(Filename)
            ImageNoAlpha = Image[:, :, :3]
            Writer.append_data(ImageNoAlpha)
    logging.info(f"Wrote GIF to {str(GifFilepath)}.")


def MakeSliceMP4(baseDir: Path | str, simID: int, regionID: int):
    """
    Create a MP4 out of slice images for specified simulation and region IDs.

    :param baseDir: Path to directory with stitched slice images.
    :type baseDir: Path | str
    :param simID: integer ID of the simulation.
    :type simID: int
    :param regionID: integer ID of the region.
    :type regionID: int
    """
    baseDir = Path(baseDir)

    VideoFilepath = baseDir / f"Simulation{simID}_Region{regionID}.mp4"

    sliceNoRegex = re.compile(r"Slice(\d+).png")

    with imageio.get_writer(VideoFilepath, fps=30) as Writer:
        sliceNos = sorted(
            [
                int(sliceNoRegex.findall(filepath.name)[0])
                for filepath in baseDir.glob(
                    f"Simulation{simID}_Region{regionID}_Slice*.png"
                )
            ]
        )
        for sliceNo in sliceNos:
            Filename = (
                baseDir / f"Simulation{simID}_Region{regionID}_Slice{sliceNo}.png"
            )
            Image = imageio.v3.imread(Filename)
            ImageNoAlpha = Image[:, :, :3]
            Writer.append_data(ImageNoAlpha)
    logging.info(f"Wrote MP4 to {str(VideoFilepath)}.")


def partsToTileImgName(
    simID: int, regionID: int, sliceNo: int, coords: tuple[float, float]
) -> str:
    """Return the name of a tile image from its parts.

    :param simID:
    :type simID: int
    :param regionID:
    :type regionID: int
    :param sliceNo:
    :type sliceNo: int
    :param coords:
    :type coords: tuple[float, float]
    :rtype: str
    """
    return f"Simulation{simID}_Region{regionID}_Slice{sliceNo}_X{coords[0]:.6f}_Y{coords[1]:.6f}.png"


def getUnborderedOutputImageSize(
    sourceDir: Path,
    simID: int,
    regionID: int,
    sliceNo: int,
    coords: list[pd.Series, pd.Series],
) -> tuple[int, int]:
    """Return the size of the unbordered stitched slice image."""
    numX, numY = len(coords[0].unique()), len(coords[1].unique())
    tileDims = Image.open(
        sourceDir
        / partsToTileImgName(
            simID, regionID, sliceNo, (coords[0].iloc[0], coords[1].iloc[0])
        )
    ).size

    return (
        tileDims[0] * numX,
        tileDims[1] * numY,
    )


def coordsToPixels(
    coord: tuple[float, float],
    topLeft: tuple[float, float],
    bottomRight: tuple[float, float],
    targetDims: tuple[int, int],
    borderSizePx: int,
    numX: int,
    numY: int,
) -> tuple[int, int]:
    """Convert coordinates of top left corners of slice tiles to pixel positions in the stitched slice."""
    if numX == 1:
        xCoordPx = borderSizePx
    else:
        xCoordPx = (coord[0] - topLeft[0]) / (bottomRight[0] - topLeft[0]) * targetDims[
            0
        ] + (
            int((coord[0] - topLeft[0]) / (bottomRight[0] - topLeft[0]) * numX) + 1
        ) * borderSizePx
    if numY == 1:
        yCoordPx = borderSizePx
    else:
        yCoordPx = (
            (coord[1] - bottomRight[1]) / (topLeft[1] - bottomRight[1]) * targetDims[1]
        ) + (
            int((coord[1] - bottomRight[1]) / (topLeft[1] - bottomRight[1]) * numY) + 1
        ) * borderSizePx

    return int(xCoordPx), int(yCoordPx)


def getSliceCoords(
    data: pd.DataFrame, simID: int, regionID: int, sliceNo: int
) -> list[pd.Series, pd.Series]:
    filt = (
        (data["simID"] == simID)
        & (data["regionID"] == regionID)
        & (data["sliceNo"] == sliceNo)
    )
    return [data[filt]["xVal"], data[filt]["yVal"]]


def getUnborderedImageCorners(
    coords: list[pd.Series],
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return the coordinates for the top left and bottom right corners of the slice."""
    numX, numY = len(coords[0].unique()), len(coords[1].unique())
    xMin, yMin, xMax, yMax = (
        coords[0].min(),
        coords[1].min(),
        coords[0].max(),
        coords[1].max(),
    )
    if numX > 1:
        xMax += (xMax - xMin) / (numX - 1)
    if numY > 1:
        yMax += (yMax - yMin) / (numY - 1)
    return (xMin, yMax), (xMax, yMin)


def StitchOneSlice(
    sourceDir: Path,
    destinationDir: Path,
    simID: int,
    regionID: int,
    sliceNo: int,
    coords: list[pd.Series, pd.Series],
    label: Optional[bool] = False,
    borderSizePx: Optional[int] = 0,
):
    """Stitch together parts (tiles) of a single slice together.

    :param sourceDir: source directory of all tile images.
    :type sourceDir: Path
    :param destinationDir: destination directory to store stitched slices.
    :type destinationDir: Path
    :param simID: ID of the simulation to which the slice belongs.
    :type simID: int
    :param regionID: ID of the region to which the slice belongs.
    :type regionID: int
    :param sliceNo: Integer identifier of the slice.
    :type sliceNo: int
    :param coords: List of two pd.Series containing x and y coordinates of the tiles.
    :type coords: list[pd.Series, pd.Series]
    :param label: whether to label the tiles with X and Y coordinates. default=False
    :type label: Optional[bool]
    :param borderSizePx: size of the border around each tile of the slice in pixels, default = 0.
    :type borderSizePx: Optional[int]
    """
    OutputImageSize = getUnborderedOutputImageSize(
        sourceDir, simID, regionID, sliceNo, coords
    )
    numX, numY = len(coords[0].unique()), len(coords[1].unique())
    OutputSliceImage = Image.new(
        "RGBA",
        (
            OutputImageSize[0] + (numX + 1) * borderSizePx,
            OutputImageSize[1] + (numY + 1) * borderSizePx,
        ),
        (0, 255, 0, 255),
    )

    topLeft, bottomRight = getUnborderedImageCorners(coords)

    for xCoord, yCoord in zip(*coords):
        sliceTilePath = sourceDir / partsToTileImgName(
            simID, regionID, sliceNo, (xCoord, yCoord)
        )

        # Get position of top-left corner of tile in new image
        # in pixels from coordinates
        xCoordPx, yCoordPx = coordsToPixels(
            (xCoord, yCoord),
            topLeft,
            bottomRight,
            OutputImageSize,
            borderSizePx,
            numX,
            numY,
        )

        TileImage = Image.open(sliceTilePath)

        # Label with X and Y coordinates, if needed
        if label:
            Overlay = PIL.ImageDraw.Draw(TileImage)
            Overlay.text(
                (16, 16),
                f"X {xCoord} um, Y {yCoord} um",
                fill=(255, 0, 0),
            )
        OutputSliceImage.paste(TileImage, (xCoordPx, yCoordPx))

    # Save stitched slice image to destination directory
    OutputImageFilepath = (
        destinationDir / f"Simulation{simID}_Region{regionID}_Slice{sliceNo}.png"
    )
    OutputSliceImage.save(OutputImageFilepath)
    logging.debug(
        f"Stitched {len(coords[0])} tiles for slice {sliceNo} for simulation {simID} and region {regionID}."
    )


def StitchManySlices(
    srcDir: Path | str,
    destDir: path | str,
    label: Optional[boot] = False,
    borderSizePx: Optional[int] = 0,
    nWorkers: Optional[int] = os.cpu_count(),
    makeGIF: Optional[bool] = False,
):
    """
    Stitch many slices in parallel. Optionally, make a GIF out of the stitched slices.

    :param srcDir: Source directory for all rendered slice parts.
    :type srcDir: Path | str
    :param destDir: Destination directory for all stitched slice images.
    :type destDir: path | str
    :param label: Whether to label each tile within each slice with x and y coordinates.
    :type label: Optional[boot]
    :param borderSizePx: Size in pixels of a border drawn around each tile within each slice.
    :type borderSizePx: Optional[int]
    :param nWorkers: Number of processors (CPUs) to use for parallelly stitching slices together.
    :type nWorkers: Optional[int]
    :param makeGIF: Whether to make a GIF out of stitched slices.
    :type makeGIF: Optional[bool]
    """

    def _doStitch(data: pd.DataFrame, simID: int, regionID: int, sliceNo: int):
        coords = getSliceCoords(data, simID, regionID, sliceNo)
        StitchOneSlice(
            srcDir,
            destDir,
            simID,
            regionID,
            sliceNo,
            coords,
            label,
            borderSizePx,
        )

    srcDir, destDir = Path(srcDir), Path(destDir)

    # Create destination directory if it does not exist
    destDir.mkdir(exist_ok=True)

    # Build data from filenames
    data = BuildSliceData(srcDir)
    sliceData = (
        data[["sliceNo", "simID", "regionID"]].drop_duplicates().reset_index(drop=True)
    )

    # Stitch slices
    _doStitchFunc = partial(_doStitch, data=data)

    Parallel(n_jobs=min(nWorkers, os.cpu_count()))(
        delayed(_doStitchFunc)(
            simID=sliceData["simID"].loc[i],
            regionID=sliceData["regionID"].loc[i],
            sliceNo=sliceData["sliceNo"].loc[i],
        )
        for i in tqdm(
            range(sliceData.shape[0]),
            desc="Stitching slice ",
            bar_format="{desc} {n_fmt}/{total_fmt} : {percentage:3.0f}%|{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
        )
    )

    # Create GIF animations out of slices
    for simID in data["simID"].unique():
        for regionID in data["regionID"].unique():
            MakeSliceGIF(destDir, simID, regionID)
