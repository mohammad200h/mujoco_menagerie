from hand import Hand

from data.fingerData import FingerData
from data.thumbData import ThumbData
from data.handData import HandData

import json
import mujoco as mj


if __name__ == "__main__":

  asset_path = "../assets/"
  fingerData = FingerData( asset_path=asset_path)
  thumbData = ThumbData( asset_path=asset_path)
  handData = HandData( asset_path=asset_path)

  robot = Hand(
    fingerData,
    thumbData,
    handData
  )
  model = robot.spec.compile()

  data = mj.MjData(model)

  print(robot.spec.to_xml())

  # visualization
  with mj.viewer.launch_passive(
        model=model, data=data, show_left_ui=False, show_right_ui=False
    ) as viewer:
        mj.mjv_defaultFreeCamera(model, viewer.cam)

        mj.mj_forward(model, data)

        while viewer.is_running():
            mj.mj_step(model, data)
            viewer.sync()
