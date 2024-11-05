import typing
import mujoco as mj

def create_tree(root_body,props:typing.List[dict]):
  body = root_body
  for prop in props:
    body = body.add_body(**prop['body'])
    for g in prop['geoms']:
      body.add_geom(**g)

    if 'joint' in prop.keys():
      body.add_joint(**prop['joint'])


class Finger(object):
  def __init__(self,props,asset_path:str,filenames:typing.List[str]):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False
    self.model = self.spec.worldbody

    # add meshes
    for filename in filenames:
      self.spec.add_mesh(name=filename, file=asset_path+filename+'.stl')

    # add material
    self.spec.add_material(name='black',rgba=[.2, .2, .2, 1])

    # defaults
    main = self.spec.default()

    main.geom.type = mj.mjtGeom.mjGEOM_MESH

    main.joint.axis = [0, 0, -1]
    main.joint.armature = 0.01

    # creating tree
    create_tree(self.model,props['tree'])

