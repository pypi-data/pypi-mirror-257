# BrainGenix-NES
# AGPLv3

import json
import base64
import tqdm
import yaspin
import os
import time
import math

from . import Configuration

from BrainGenix.NES.Client import RequestHandler

import BrainGenix.LibUtils.ConfigCheck
import BrainGenix.LibUtils.GetID




class Calcium:

    def __init__(self, _Configuration:Configuration, _RequestHandler:RequestHandler, _SimulationID:int):
        # Create Attributes
        self.RequestHandler = _RequestHandler
        self.SimulationID = _SimulationID

        # Run Configuration Check
        BrainGenix.LibUtils.ConfigCheck.ConfigCheck(_Configuration)

        # Create On Server
        QueryList:list = []
        QueryList.append({
            "VSDA/Ca/Initialize": {
                "SimulationID": _SimulationID
            }
        })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")[0]
        assert(Response != None)

        QueryList:list = []
        QueryList.append({
            "VSDA/Ca/SetupMicroscope": {
                "VoxelResolution_nm": _Configuration.VoxelResolution_nm,
                "ImageWidth_px": _Configuration.ImageWidth_px,
                "ImageHeight_px": _Configuration.ImageHeight_px,
                "NumVoxelsPerSlice": _Configuration.NumVoxelsPerSlice,
                "ScanRegionOverlap_percent": _Configuration.ScanRegionOverlap_percent,
                "NumPixelsPerVoxel_px": _Configuration.NumPixelsPerVoxel_px,
                "FlourescingNeuronIDs": _Configuration.FlourescingNeuronIDs,
                "CalciumIndicator": _Configuration.CalciumIndicator,
                "IndicatorRiseTime_ms": _Configuration.IndicatorRiseTime_ms,
                "IndicatorDecayTime_ms": _Configuration.IndicatorDecayTime_ms,
                "IndicatorInterval_ms": _Configuration.IndicatorInterval_ms,
                "BrightnessAmplification": _Configuration.BrightnessAmplification,
                "SimulationID": _SimulationID
            }
        })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")[0]
        assert(Response != None)



    ## Access Methods
    def DefineScanRegion(self, _Point1_um:list, _Point2_um:list):
        QueryList:list = []
        QueryList.append({
            "VSDA/Ca/DefineScanRegion": {
                "Point1_um": _Point1_um,
                "Point2_um": _Point2_um,
                "SimulationID": self.SimulationID
            }
        })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")[0]
        assert(Response != None)
        self.ScanRegionID = Response["ScanRegionID"]


    def QueueRenderOperation(self):
        QueryList:list = []
        QueryList.append({
            "VSDA/Ca/QueueRenderOperation": {
                "ScanRegionID": self.ScanRegionID,
                "SimulationID": self.SimulationID
            }
        })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")[0]
        assert(Response != None)
        return Response["StatusCode"]


    def GetRenderStatus(self):
        QueryList:list = []
        QueryList.append({
            "VSDA/Ca/GetRenderStatus": {
                "SimulationID": self.SimulationID
            }
        })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")[0]
        assert(Response != None)
        return Response
    

    def GetImageStack(self):
        QueryList:list = []
        QueryList.append({
            "VSDA/Ca/GetImageStack": {
                "ScanRegionID": self.ScanRegionID,
                "SimulationID": self.SimulationID
            }
        })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")[0]
        assert(Response != None)
        return Response["RenderedImages"]


    def GetImage(self, _ImageHandle:str):
        QueryList:list = []
        QueryList.append({
            "VSDA/GetImage": {
                "ImageHandle": _ImageHandle,
                "SimulationID": self.SimulationID
            }
        })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")[0]
        assert(Response != None)
        return bytes(Response["ImageData"], 'utf-8')


    def GetImages(self, _ImageHandles:list):
    
        QueryList:list = []

        for ImageHandle in _ImageHandles:
            QueryList.append({
                "VSDA/GetImage": {
                    "SimulationID": self.SimulationID,
                    "ImageHandle": ImageHandle
                }
            })
        Response = self.RequestHandler.BuildPostQuery(QueryList, "/NES")
        assert(Response != None)
        
        ImageBytes:list = []
        for ImageResponse in Response:
            ImageBytes.append(bytes(ImageResponse["ImageData"], 'utf-8'))
        return ImageBytes




    def WaitForRender(self):

        # Setup Status Information
        StatusInfo:dict = self.GetRenderStatus()


        # Perform Sanity Check On Render
        if (StatusInfo["RenderStatus"] < 3):
            print("Error during rendering, API reports:\n")
            print(StatusInfo)


        # Block With Queued Spinner
        QueueSpinner = yaspin.yaspin(text="Calcium Render Operation In Queue, Elapsed Time", color="green", timer=True)
        QueueSpinner.start()
        while (StatusInfo["RenderStatus"] == 3):

            # Get Status Info, Wait To Avoid API Spam
            StatusInfo:dict = self.GetRenderStatus()
            time.sleep(0.25)

        QueueSpinner.ok()


        
        # Setup Slice, Image Status Bar
        RegionStatusBar = tqdm.tqdm("Rendering Region", total=1)
        RegionStatusBar.leave = True
        RegionStatusBar.bar_format = "{desc}{percentage:3.0f}%|{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        RegionStatusBar.colour = "blue"
        LastRegionNumber:int = 0

        SliceStatusBar = tqdm.tqdm("Rendering Slice", total=1)
        SliceStatusBar.leave = True
        SliceStatusBar.colour = "green"
        SliceStatusBar.bar_format = "{desc}{percentage:3.0f}%|{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        LastSliceNumber:int = 0

        ImageStatusBar = tqdm.tqdm("Rendering Image", total=1)
        ImageStatusBar.leave = True
        ImageStatusBar.bar_format = "{desc}{percentage:3.0f}%|{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        ImageStatusBar.colour = "magenta"


        # Block Execution Until Render Finishes, Update Bar As We Wait
        while (StatusInfo["RenderStatus"] != 5):

            # Update Region Bar
            RegionStatusBar.total = int(StatusInfo["TotalRegions"])
            RegionStatusBar.n = max(int(StatusInfo["CurrentRegion"]), 0)
            RegionStatusBar.refresh()
            RegionStatusBar.set_description(f"Rendering Calcium Region {str(StatusInfo['CurrentRegion']).rjust(5, '0')} / {str(StatusInfo['TotalRegions']).rjust(5, '0')}")


            # Update Slice Bar
            if (RegionStatusBar.n > LastRegionNumber):
                LastRegionNumber = RegionStatusBar.n
                SliceStatusBar.reset()
            SliceStatusBar.total = int(StatusInfo["TotalSlices"])
            SliceStatusBar.n = max(int(StatusInfo["CurrentSlice"]), 0)
            SliceStatusBar.refresh()
            SliceStatusBar.set_description(f"Rendering Calcium Slice {str(StatusInfo['CurrentSlice']).rjust(5, '0')} / {str(StatusInfo['TotalSlices']).rjust(5, '0')}")


            # Update Image Bar
            if (SliceStatusBar.n > LastSliceNumber):
                LastSliceNumber = SliceStatusBar.n
                ImageStatusBar.reset()
            ImageStatusBar.total = int(StatusInfo["TotalSliceImages"])
            ImageStatusBar.n = max(int(StatusInfo["CurrentSliceImage"]), 0)
            ImageStatusBar.refresh()
            ImageStatusBar.set_description(f"Rendering Calcium Image {str(StatusInfo['CurrentSliceImage']).rjust(5, '0')} / {str(StatusInfo['TotalSliceImages']).rjust(5, '0')}")



            # Get Status Info, Wait To Avoid API Spam
            StatusInfo:dict = self.GetRenderStatus()
            time.sleep(0.1)
        
    
        # When we're done, rendering is finished - make it look like it truly is, then close the bar
        RegionStatusBar.total = int(StatusInfo["TotalRegions"])
        RegionStatusBar.n = int(StatusInfo["TotalRegions"])
        RegionStatusBar.set_description(f"Rendering Calcium Region {str(StatusInfo['TotalRegions']).rjust(5, '0')} / {str(StatusInfo['TotalRegions']).rjust(5, '0')}")
        RegionStatusBar.refresh()
        RegionStatusBar.close()
        SliceStatusBar.total = int(StatusInfo["TotalSlices"])
        SliceStatusBar.n = int(StatusInfo["TotalSlices"])
        SliceStatusBar.set_description(f"Rendering Calcium Slice {str(StatusInfo['TotalSlices']).rjust(5, '0')} / {str(StatusInfo['TotalSlices']).rjust(5, '0')}")
        SliceStatusBar.refresh()
        SliceStatusBar.close()
        ImageStatusBar.total = int(StatusInfo["TotalSliceImages"])
        ImageStatusBar.n = int(StatusInfo["TotalSliceImages"])
        ImageStatusBar.set_description(f"Rendering Calcium Image {str(StatusInfo['TotalSliceImages']).rjust(5, '0')} / {str(StatusInfo['TotalSliceImages']).rjust(5, '0')}")
        ImageStatusBar.refresh()
        ImageStatusBar.close()




    def SaveImageStack(self, _ImageStackDirectoryPrefix:str = "", _NumImagesPerCall:int = 4):

        # Check That The DirectoryPath Exists
        if not _ImageStackDirectoryPrefix.endswith("/"):
            _ImageStackDirectoryPrefix += "/"
        
        if not os.path.exists(_ImageStackDirectoryPrefix):
            os.makedirs(_ImageStackDirectoryPrefix)
            

        # Get Image Stack Manifest
        ImageHandles = self.GetImageStack()

        # Setup Progress Bar
        Bar = tqdm.tqdm("Downloading Image Stack", total=len(ImageHandles))
        Bar.leave = True
        Bar.bar_format = "{desc}{percentage:3.0f}%|{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        Bar.colour = "green"

        Total:int = 0
        for x in range(math.ceil(len(ImageHandles) / _NumImagesPerCall)):

            BatchHandles:list = []
            for i in range(_NumImagesPerCall):
                if (Total < len(ImageHandles)):
                    BatchHandles.append(ImageHandles[Total])
                    Total += 1

            # Save These Images
            ImagesData:list = self.GetImages(BatchHandles)

            for i in range(_NumImagesPerCall):
                with open(_ImageStackDirectoryPrefix + BatchHandles[i].replace("/", "_").strip("Renders")[1:], "wb") as FileHandler:
                    FileHandler.write(base64.decodebytes(ImagesData[i]))
        
            # Count Up Bar
            CurrentImageIndex = x * _NumImagesPerCall
            Bar.set_description(f"Downloading Image {str(CurrentImageIndex + 1).rjust(5, '0')} / {str(len(ImageHandles)).rjust(5, '0')}")
            Bar.n = CurrentImageIndex + 1
            Bar.refresh()

        Bar.close()
