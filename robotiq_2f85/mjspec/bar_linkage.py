import mujoco as mj
import typing

def create_tree(root_body,props:typing.List[dict]):
  body = root_body
  for b in props['bodies']:
    b_props = b.copy()
    b_props.pop("geoms",None)
    b_props.pop("joint",None)
    body = body.add_body(**b_props)
    for g in b['geoms']:
      if g["type"]  =="mesh":
        g["type"] =  mj.mjtGeom.mjGEOM_MESH
      elif g["type"]  =="box":
        g["type"] =  mj.mjtGeom.mjGEOM_BOX
      body.add_geom(**g)

    if 'joint' in b.keys():
      body.add_joint(**b['joint'])


class Driver(object):
  def __init__(self,props:dict,asset_path:str):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False
    self.model = self.spec.worldbody

    #driver specific props
    d_props = props['driver']

    #add mesh
    for mesh in d_props["meshes"]:
      self.spec.add_mesh(name=mesh,file=asset_path+mesh+".stl")

    #add material
    for material in d_props["materials"]:
      self.spec.add_material(**material)

    # defaults
    main = self.spec.default()
    main.mesh.scale = [0.001, 0.001, 0.001]
    main.joint.axis = [1,0,0]

    # applying defaults to bodies
    # TODO: so I think dictionaries work with reference -> double check that I am right
    for b in d_props['bodies']:
      b['geoms'][0] |= props['geom_vis_default']
      b['geoms'][1] |= props['geom_col_default']
      if b['name'] =='driver':
        b['joint'] |= d_props['joint_driver_default']
      elif b['name'] == 'coupler':
        b['joint'] |= d_props['joint_coupler_default']

    # creating tree
    create_tree(self.model,d_props)


class SpringLink(object):
  def __init__(self,props:dict,asset_path:str):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False
    self.model = self.spec.worldbody

    #spring_link specific props
    s_props = props['spring_link']

    #add mesh
    for mesh in s_props["meshes"]:
      self.spec.add_mesh(name=mesh,file=asset_path+mesh+".stl")

    #add material
    self.spec.add_material(**s_props["material"])

    # defaults
    main = self.spec.default()
    main.mesh.scale = [0.001, 0.001, 0.001]
    main.joint.axis = [1,0,0]

    # applying defaults to bodies
    for b in s_props['bodies']:
      # pads
      if b['name'] == 'pad':
        b['geoms'][0] |= s_props['geom_col_pad_box_1']
        b['geoms'][1] |= s_props['geom_col_pad_box_2']
        continue
      # silicon pad
      elif b['name'] == 'silicone_pad':
        b['geoms'][0] |= props['geom_vis_default']
        continue

      # every other body
      b['geoms'][0] |= props['geom_vis_default']
      b['geoms'][1] |= props['geom_col_default']
      if b['name'] =='spring_link':
        b['joint'] |= s_props['joint_spring_link_default']
      elif b['name'] == 'follower':
        b['joint'] |= s_props['joint_follower_default']

    # creating tree
    create_tree(self.model,s_props)

def create_driver(data:dict,asset_path:str):
  driver = Driver(props=data,
                  asset_path=asset_path)
  model = driver.spec.compile()
  xml = driver.spec.to_xml()
  with open("driver.xml", "w") as file:
   # Write content to the file
   file.write(xml)

  return model

def create_spring_link(data:dict,asset_path:str):
  spring_link = SpringLink(props=data,
                  asset_path=asset_path)
  model = spring_link.spec.compile()
  xml = spring_link.spec.to_xml()
  with open("spring_link.xml", "w") as file:
   # Write content to the file
   file.write(xml)

  return model