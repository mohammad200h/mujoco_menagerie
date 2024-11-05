
import mujoco as mj
import typing
from bar_linkage import (Driver,SpringLink)

def create_tree(root_body,props:typing.List[dict]):
  body = root_body
  for b in props['bodies']:
    b_props = b.copy()
    b_props.pop("geoms",None)
    b_props.pop("joint",None)
    b_props.pop("site",None)

    print(f"b_props::{b_props}")
    body = body.add_body(**b_props)
    for g in b['geoms']:
      if g["type"]  =="mesh":
        g["type"] =  mj.mjtGeom.mjGEOM_MESH
      elif g["type"]  =="box":
        g["type"] =  mj.mjtGeom.mjGEOM_BOX
      body.add_geom(**g)

    if 'joint' in b.keys():
      body.add_joint(**b['joint'])
    if 'site' in b.keys():
      if b['site']['type']=="sphere":
           b['site']['type'] = mj.mjtGeom.mjGEOM_SPHERE
      body.add_site(**b['site'])

  return body

class Robotiq_2f85(object):
  def __init__(self,props:dict,asset_path:str):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False
    self.model = self.spec.worldbody

    #base specific props
    b_props = props['base']

    #add mesh
    for mesh in b_props["meshes"]:
      self.spec.add_mesh(name=mesh,file=asset_path+mesh+".stl")

    # add material
    self.spec.add_material(**b_props['material'])

    # defaults
    main = self.spec.default()
    main.mesh.scale = [0.001, 0.001, 0.001]
    main.joint.axis = [1,0,0]

    # applying defaults to bodies
    for b in b_props['bodies']:
      b['geoms'][0] |= props['geom_vis_default']
      b['geoms'][1] |= props['geom_col_default']
      if b['name'] =='driver':
        b['joint'] |= b_props['joint_driver_default']
      elif b['name'] == 'coupler':
        b['joint'] |= b_props['joint_coupler_default']

    # creating tree
    body = create_tree(self.model,b_props)

    print(f"body::name::{body.name}")
    print(f"body::quat::{body.quat}")

    # attaching right side
    # for f_prop in b_props['frames']:
    #   frame = body.add_frame(**f_prop)
    #   if "driver" in f_prop['name']:
    #     frame.attach_body(Driver(props,asset_path).model,f_prop['name'],'')
    #   elif "spring_link" in f_prop['name']:
    #     frame.attach_body(SpringLink(props,asset_path).model,f_prop['name'],'')






def create_robotiq_2f85(data,asset_path):
  robotiq_2f85 = Robotiq_2f85(props=data,
                  asset_path=asset_path)
  model = robotiq_2f85.spec.compile()
  xml = robotiq_2f85.spec.to_xml()
  with open("robotiq_2f85.xml", "w") as file:
   # Write content to the file
   file.write(xml)

  return model


