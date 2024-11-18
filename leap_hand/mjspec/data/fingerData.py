from dataclasses import dataclass
from .defaultData import DefaultsData
import mujoco as mj

@dataclass
class FingerData(DefaultsData):
  asset_path:str
  material = {
    "name":"black",
    "rgba":[.2, .2, .2, 1]
  }
  meshes = ["mcp_joint","pip","dip","fingertip"]
  mesh_format = ".stl"

  bodies=[
    {
      "body":{
        "name":"mcp_joint",
        "mass": 0.044,
        "iquat": [0.388585, 0.626468, -0.324549, 0.592628],
        "inertia": [1.47756e-05, 1.31982e-05, 6.0802e-06]
      },
      "joint": {
      "name": "j0",
      "range": [-0.314, 2.23],
      "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [0.0084069, 0.00776624, 0.0146574],
          "quat": [1, 0, 0, 0],
          "meshname": "mcp_joint"
        },
        {
          "pos": [0.0084069, 0.00776624, 0.0146574],
          "quat": [1, 0, 0, 0],
          "meshname": "mcp_joint"
        }
      ]
    },
    {
      "body": {
        "name":"pip",
        "pos": [-0.0122, 0.0381, 0.0145],
        "quat": [1, -1, -1, 1],
        "mass": 0.032,
        "iquat": [0.709913, 0.704273, -0.000363156, 0.00475427],
        "inertia": [4.7981e-06, 4.23406e-06, 2.86184e-06]
      },
      "joint": {
        "name": "j1",
        "range": [-1.047, 1.047],
        "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [0.00964336, 0.0003, 0.000784034],
          "quat": [1, -1, -1, -1],
          "meshname": "pip"
        },
        {
          "pos": [0.00964336, 0.0003, 0.000784034],
          "quat": [1, -1, -1, -1],
          "meshname": "pip"
        }
      ]
    },
    {
      "body": {
        "name":"dip",
        "pos": [0.015, 0.0143, -0.013],
        "quat": [1, 1, -1, 1],
        "mass": 0.037,
        "iquat": [-0.252689, 0.659216, 0.238844, 0.666735],
        "inertia": [6.68256e-06, 6.24841e-06, 5.02002e-06]
      },
      "joint": {
        "name": "j2",
        "range": [-0.506, 1.885],
        "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [0.0211334, -0.00843212, 0.00978509],
          "quat": [0, -1, 0, 0],
          "meshname": "dip"
        },
        {
          "pos": [0.0211334, -0.00843212, 0.00978509],
          "quat": [0, -1, 0, 0],
          "meshname": "dip"
        }
      ]
    },
    {
      "body": {
        "name":"fingertip",
        "pos": [-4.08806e-09, -0.0361, 0.0002],
        "mass": 0.016,
        "iquat": [0.706755, 0.706755, 0.0223155, 0.0223155],
        "inertia": [3.37527e-06, 2.863e-06, 1.54873e-06]
      },
      "joint": {
        "name": "j3",
        "range": [-0.366, 2.042],
        "actfrcrange": [-0.95, 0.95]
      },
      "geoms": [
        {
          "pos": [0.0132864, -0.00611424, 0.0145],
          "quat": [0, 1, 0, 0],
          "meshname": "fingertip"
        },
        {
          "pos": [0.0132864, -0.00611424, 0.0145],
          "quat": [0, 1, 0, 0],
          "meshname": "fingertip"
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