from typing import Generic, List, Optional, Type, TypeVar, Union

import pandas as pd
import pkg_resources

from fao56_model.data_models.crop import Crop, CropType
from fao56_model.data_models.soil import Soil, SoilType

T = TypeVar("T", Soil, Crop)
K = TypeVar("K", bound=Union[SoilType, CropType])


class NotFoundException(Exception):
    def __init__(self, item_type: K):
        self.item_type: K = item_type
        self.message = f"{item_type} not found in database"
        super().__init__(self.message)


class Database(Generic[T, K]):
    def __init__(self, data_type: Type[T], file_name: str):
        self.data_type: Type[T] = data_type
        self.data: List[T] = self._load_data_from_csv(file_name)

    def _load_data_from_csv(self, file_name: str) -> List[T]:
        file_path = pkg_resources.resource_filename(
            "fao56_model", f"data/{file_name}"
        )
        df = pd.read_csv(file_path)
        return [
            self.data_type(**datum)  # type: ignore
            for datum in df.to_dict(orient="records")
        ]

    def get_by_type(self, item_type: K) -> T:
        item: Optional[T] = next(
            (item for item in self.data if item.kind == item_type), None
        )
        if item is None:
            raise NotFoundException(item_type)
        return item

    def get_all(self) -> List[T]:
        return self.data


class SoilDatabase(Database[Soil, SoilType]):
    def __init__(self):
        super().__init__(Soil, "soils.csv")


class CropDatabase(Database[Crop, CropType]):
    def __init__(self):
        super().__init__(Crop, "crops.csv")
