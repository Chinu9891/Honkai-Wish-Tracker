from dataclasses import dataclass, asdict
from typing import Optional
from config.config import PATHS_MAPPING

@dataclass
class WishSchema:
    name: str
    rarity: int
    item_type: str
    path: str
    element: Optional[str] = None

    @classmethod
    def from_json(cls, data: dict) -> dict:
        
        res = []
        
        # filter only the keys defined in dataclass
        fields = {f.name for f in cls.__dataclass_fields__.values()}
        
        # filters all the data and returns list of cleaned items
        for value in data.values():  
            filtered_data = {k: v for k, v in value.items() if k in fields}
            
            filtered_data['item_type'] = 'character' if filtered_data.get('element') else 'lightcone'
            
            path_to_map = filtered_data['path']
            
            filtered_data['path'] = PATHS_MAPPING[path_to_map]
            
            res.append(asdict(cls(**filtered_data)))
        
        return res