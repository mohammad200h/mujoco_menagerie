from dataclasses import dataclass

@dataclass
class DefaultsData:
  
  geom_col_default = {
    "group": 3
  }
  geom_vis_default = {
    "group": 2,
    "contype": 0,
    "conaffinity": 0,
    "density": 0,
    "material": "black"
  }
