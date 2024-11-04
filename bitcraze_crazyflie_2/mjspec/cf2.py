import mujoco as mj

class CF2(object):
  def __init__(self,props:dict,asset_path:str):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False
    self.model = self.spec.worldbody

    #add material
    for material in props["material"]:
      self.spec.add_material(**material)
    #add meshes
    for mesh in  props["mesh"]:
      for idx in range(mesh["range"][1]):
        filename = mesh["prefix"]+str(idx)
        self.spec.add_mesh(name=filename, file=asset_path+filename+'.obj')



    # defaults
    main = self.spec.default()
    main.geom.type = mj.mjtGeom.mjGEOM_MESH
    main.site.group = 5

    # motor actuation setting
    main.actuator.gaintype = mj.mjtGain.mjGAIN_FIXED
    main.actuator.biastype = mj.mjtBias.mjBIAS_NONE
    main.actuator.dyntype  = mj.mjtDyn.mjDYN_NONE
    main.actuator.trntype = mj.mjtTrn.mjTRN_SITE

    # add body
    body = self.model.add_body( **props['body'])

    # add freejoint
    body.add_freejoint()
    # add geom
    geoms_vis=props['geoms'][0]
    for idx in range(geoms_vis['range'][1]):
      geom = {
        'name' : geoms_vis['prefix']+str(idx),
        'meshname' : geoms_vis['prefix']+str(idx),
        'material': geoms_vis['materials'][idx]
      } | props['geom_vis_default']
      body.add_geom(**geom)

    geoms_col=props['geoms'][1]
    for idx in range(geoms_col['range'][1]):
      geom = {
        'name' : geoms_col['prefix']+str(idx),
        'meshname' : geoms_col['prefix']+str(idx)
      } | props['geom_col_default']
      body.add_geom(**geom)

    # add site
    for site in props['sites']:
      body.add_site(**site)
    # add actuator
    # https://github.com/google-deepmind/mujoco/blob/1d58576d284f2cfb33ba872de5fd23fe1e54e47e/src/xml/xml_native_reader.cc#L2175
    # unit gain
    # actuator->gainprm[0] = 1;

    # implied parameters
    # actuator->dyntype = mjDYN_NONE;
    # actuator->gaintype = mjGAIN_FIXED;
    # actuator->biastype = mjBIAS_NONE;

    for actuator in  props["actuation"]:
      self.spec.add_actuator(**actuator)

    # Todo: add sensor
    # self.spec.add_sensor(needstage=mj.mjtStage.mjSTAGE_ACC,name="body_gyro")



def create_cf2(data:dict,asset_path):

  cf2 = CF2(props=data,
            asset_path=asset_path)
  cf2.spec.worldbody.add_light(name="top", pos=[0, 0, 1])
  model = cf2.spec.compile()
  xml = cf2.spec.to_xml()
  with open("cf2.xml", "w") as file:
   # Write content to the file
   file.write(xml)

  return model