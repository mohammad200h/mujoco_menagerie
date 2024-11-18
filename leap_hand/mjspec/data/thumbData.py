from dataclasses import dataclass
from .defaultData import DefaultsData
import mujoco as mj


@dataclass
class ThumbData(DefaultsData):
  asset_path:str
  material = {
    "name":"black",
    "rgba":[.2, .2, .2, 1]
  }
  meshes = ["pip","thumb_pip","thumb_dip","thumb_fingertip"]
  mesh_format = ".stl"
  bodies = [
    {
      "body": {
          "name":"pip_4",
          "mass": 0.032,
          "iquat": [0.709913, 0.704273, -0.000363156, 0.00475427],
          "inertia": [4.7981e-06, 4.23406e-06, 2.86184e-06]
      },
      "joint": {
        "name": "j0",
        "range": [-2.094, 0.349],
        "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [-0.00535664, 0.0003, 0.000784034],
          "quat": [1, -1, -1, -1],
          "meshname": "pip"
        },
        {
          "pos": [-0.00535664, 0.0003, 0.000784034],
          "quat": [1, -1, -1, -1],
          "meshname": "pip"
        }
      ]
    },
    {
      "body": {
        "name":"thumb_pip",
        "pos": [0, -0.0141, -0.013],
        "quat": [1, -1, -1, -1],
        "mass": 0.003,
        "inertia": [5.93e-07, 5.49e-07, 2.24e-07]
      },
      "joint": {
        "name": "j1",
        "range": [-2.443, 0.47],
        "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [0.0119619, 0, -0.0158526],
          "quat": [1, 1, 0, 0],
          "meshname": "thumb_pip"
        },
        {
          "pos": [0.0119619, 0, -0.0158526],
          "quat": [1, 1, 0, 0],
          "meshname": "thumb_pip"
        }
      ]
    },
    {
      "body": {
        "name":"thumb_dip",
        "pos": [0, 0.0145, -0.017],
        "quat": [1, -1, 0, 0],
        "mass": 0.038,
        "iquat": [0.708624, 0.704906, 0.00637342, 0.0303153],
        "inertia": [8.48742e-06, 7.67823e-06, 3.82835e-06]
      },
      "joint": {
        "name": "j2",
        "range": [-1.2, 1.9],
        "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [0.0439687, 0.057953, -0.00862868],
          "quat": [1, 0, 0, 0],
          "meshname": "thumb_dip"
        },
        {
          "pos": [0.0439687, 0.057953, -0.00862868],
          "quat": [1, 0, 0, 0],
          "meshname": "thumb_dip"
        }
      ]
    },
    {
      "body": {
        "name":"thumb_fingertip",
        "pos": [0, 0.0466, 0.0002],
        "quat": [0, 0, 0, -1],
        "mass": 0.049,
        "iquat": [0.704307, 0.709299, 0.006848, -0.0282727],
        "inertia": [2.03882e-05, 1.98443e-05, 4.32049e-06]
      },
      "joint": {
        "name": "j3",
        "range": [-1.34, 1.88],
        "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [0.0625595, 0.0784597, 0.0489929],
          "quat": [1, 0, 0, 0],
          "meshname": "thumb_fingertip"
        },
        {
          "pos": [0.0625595, 0.0784597, 0.0489929],
          "quat": [1, 0, 0, 0],
          "meshname": "thumb_fingertip"
        }
      ]
    }
  ]
  joints = [body["joint"]["name"] for body in bodies]
  # default
  joint_armature = 0.01

  # sensors
  joint_pos_sensor = {
    "suffix":"_jpos",
    "type":mj.mjtSensor.mjSENS_JOINTPOS,
    "objtype":mj.mjtObj.mjOBJ_JOINT
  }
  joint_vel_sensor = {
    "suffix":"_jvel",
    "joints": [body["joint"]["name"] for body in bodies],
    "type":mj.mjtSensor.mjSENS_JOINTVEL,
    "objtype":mj.mjtObj.mjOBJ_JOINT
  }
  touch_sensor = {
    "name":bodies[-1]["body"]["name"] + "_touch",
    "objname":bodies[-1]["body"]["name"],
    "type":mj.mjtSensor.mjSENS_TOUCH,
    "objtype":mj.mjtObj.mjOBJ_SITE
  }
  force_sensor = {
    "name":bodies[-1]["body"]["name"] + "_force",
    "objname":bodies[-1]["body"]["name"],
    "type":mj.mjtSensor.mjSENS_FORCE,
    "objtype":mj.mjtObj.mjOBJ_SITE
  }

  # actuators
  kp = 20
  dampratio = 1
  actuator_suffix = "act_"


