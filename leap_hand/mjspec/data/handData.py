from dataclasses import dataclass
from .defaultData import DefaultsData
import mujoco as mj

@dataclass
class HandData(DefaultsData):
  asset_path:str
  material = {
    "name":"black",
    "rgba":[.2, .2, .2, 1]
  }
  mesh = "palm_lower_left"
  mesh_format = ".stl"

  body = {
    "name":"palm_lower",
    "pos": [0, 0, 0.1],
    "quat": [0, 1, 0, 0],
    "mass": 0.235,
    "iquat": [0.704257, -0.0014136, 0.00678547, 0.709911],
    "inertia": [0.000523252, 0.000351001, 0.000256955]
  }
  geoms = [
    {
      "pos": [-0.0955742, -0.11704, 0.0207796],
      "quat": [0, 0, 1, 1],
      "meshname": "palm_lower_left"
    },
    {
      "pos": [-0.0955742, -0.11704, 0.0207796],
      "quat": [0, 0, 1, 1],
      "meshname": "palm_lower_left"
    }
  ]

  fingers_frame_quat = [1, 1, 1, -1]
  thumb_frame_quat =  [1, 0, 1, 0]
  fingers_frames_pos = [
    [-0.0825742, -0.08574, 0.00780089],
    [-0.0825742, -0.04029, 0.00780089],
    [-0.0825742, 0.00515999, 0.00780089]
  ]
  fingers_prefix = ["FF","MF","RF"]
  thumb_frame_pos = [-0.144874, -0.09004, 0.00490089]

  contacts = [
    {
      "bodyname1":"palm_lower",
      "bodyname2":["ff_mcp_joint","mf_mcp_joint",
                   "rf_mcp_joint","th_pip_4",
                   "th_thumb_dip","th_thumb_pip"
      ]
    },
    { "prefix":["ff_","mf_","rf_"],
        "bodyname1":"dip",
        "bodyname2":"mcp_joint"
    }
  ]
