from bar_linkage import (create_driver,
                         create_spring_link)
from robotiq_2f85 import create_robotiq_2f85
import mujoco as mj
import json


if __name__ =="__main__":
    asset_path = "../assets/"
    data_file = "./2f85.json"

    with open(data_file, 'r') as file:
      data = json.load(file)

    model = create_robotiq_2f85(data,asset_path)

    data = mj.MjData(model)

    # visualization
    with mj.viewer.launch_passive(
          model=model, data=data, show_left_ui=False, show_right_ui=False
      ) as viewer:
          mj.mjv_defaultFreeCamera(model, viewer.cam)

          mj.mj_forward(model, data)

          while viewer.is_running():
              mj.mj_step(model, data)
              viewer.sync()