# BrainGenix-NES
# AGPLv3


class Configuration():

    def __init__(self):
        
        # Create Attributes
        self.VoxelResolution_nm:float = None
        self.ImageWidth_px:int = None
        self.ImageHeight_px:int = None
        self.NumVoxelsPerSlice:float = None
        self.ScanRegionOverlap_percent:float = None 
        self.NumPixelsPerVoxel_px:int = None
        self.FlourescingNeuronIDs:list = None
        self.CalciumIndicator:str = None
        self.IndicatorRiseTime_ms:float = None
        self.IndicatorDecayTime_ms:float = None
        self.IndicatorInterval_ms:float = None
