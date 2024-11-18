import typing
import mujoco as mj
from data.fingerData import FingerData

class FingerBase:
  def __init__(self,data:FingerData):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False
    self.model = self.spec.worldbody

    # material
    self.spec.add_material(**data.material)

    # meshes
    for mesh in data.meshes:
      self.spec.add_mesh(
        name=mesh,
        file = data.asset_path + mesh + data.mesh_format
      )

    # defaults
    main = self.spec.default()
    main.geom.type = mj.mjtGeom.mjGEOM_MESH
    main.joint.axis = [0, 0, -1]
    main.joint.armature = data.joint_armature

    # tree
    body = self.model
    for prop in data.bodies:
      body = body.add_body(**prop['body'])
      body.add_joint(**prop['joint'])
      for geom in prop['geoms']:
        body.add_geom(**geom)
      if  "site" in prop:
        body.add_site(**prop['site'])

class FingerSensor(FingerBase):
  def __init__(self, data: FingerData,
    jpos = False,
    jvel = False,
    touch = False,
    force = False
  ):
    super().__init__(data)

    # joint position sensors
    if jpos:
      for j in data.joints:
        self.spec.add_sensor(
          name = j + data.joint_pos_sensor["suffix"],
          objname = j,
          type = mj.mjtSensor.mjSENS_JOINTPOS,
          objtype = mj.mjtObj.mjOBJ_JOINT
        )

    # joint velocity sensors
    if jvel:
      for j in data.joints:
        self.spec.add_sensor(
          name = j + data.joint_vel_sensor["suffix"],
          objname = j,
          type = mj.mjtSensor.mjSENS_JOINTVEL,
          objtype = mj.mjtObj.mjOBJ_JOINT
        )

    # force and touch sensor
    if touch:
      self.spec_add_sensor(**data.touch_sensor)
    if force:
      self.spec_add_sensor(**data.force_sensor)

class Finger(FingerSensor):
  def __init__(self, data: FingerData,**kwargs):
    super().__init__(data,**kwargs)

    # defaults
    main = self.spec.default()
    # position actuation setting
    main.actuator.trntype = mj.mjtTrn.mjTRN_JOINT
    main.actuator.gaintype = mj.mjtGain.mjGAIN_FIXED
    main.actuator.biastype = mj.mjtBias.mjBIAS_AFFINE
    main.actuator.gainprm[0] =  data.kp
    main.actuator.biasprm[1] = -data.kp
    main.actuator.biasprm[2] = data.dampratio


    for j in data.joints:
      self.spec.add_actuator(
        name = data.actuator_suffix+j,
        target = j
      )