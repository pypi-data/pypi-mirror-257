from datetime import date, datetime
from typing import List, Optional, Tuple

from fao56_model.data_models.crop import Crop
from fao56_model.planted_crop import PlantedCrop
from fao56_model.utils import is_overlapping


class CropCalendar:
    def __init__(self, crop_plus_sowing: List[Tuple[Crop, date]]) -> None:
        self.set_crops(crop_plus_sowing)

    def set_crops(self, crop_plus_sowing: List[Tuple[Crop, date]]) -> None:
        self.planted_crops: List[PlantedCrop] = []
        for c, d in crop_plus_sowing:
            self.planted_crops.append(PlantedCrop(c, d))
        if is_overlapping([pc.growing_period for pc in self.planted_crops]):
            raise ValueError("Overlapping crop growing periods")
        sorted(self.planted_crops, key=lambda pc: pc.sowing_date)

    @property
    def time_range(self):
        period = None
        for planted_crop in self.planted_crops:
            period = (
                planted_crop.growing_period
                if period is None
                else period.encompass(planted_crop.growing_period)
            )
        return period

    def get_crop(self, timestamp: datetime) -> Optional[PlantedCrop]:
        for planted_crop in self.planted_crops:
            if timestamp in planted_crop.growing_period:
                return planted_crop
        return None
