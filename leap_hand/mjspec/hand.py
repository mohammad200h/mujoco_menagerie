from finger import Finger
from data.fingerData import FingerData
from data.thumbData import ThumbData
from data.handData import HandData

import mujoco as mj
import numpy as np

class Hand:
  def __init__(self,
               fingerData:FingerData,
               thumbData:ThumbData,
               handData:HandData
  ):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False
    self.model = self.spec.worldbody

    # add mesh
    self.spec.add_mesh(
      name = handData.mesh,
      file = handData.asset_path + handData.mesh + handData.mesh_format
    )
    # add material
    self.spec.add_material(**handData.material)

    # add palm
    body = self.model.add_body(**handData.body)
    # geoms
    for g in handData.geoms:
      body.add_geom(**g)

    # adding first middle and ring finger
    for idx,pos in enumerate(handData.fingers_frames_pos):
      frame = body.add_frame(
        name = handData.fingers_prefix[idx],
        quat = handData.fingers_frame_quat,
        pos = pos
      )
      frame.attach_body(Finger(fingerData).model,
        "",handData.fingers_prefix[idx]
      )

    # adding thumb
    frame = body.add_frame(
      name = "TH",
      quat = handData.thumb_frame_quat,
      pos = handData.thumb_frame_pos
    )
    frame.attach_body(Finger(thumbData).model,
      "", "TH"
    )



