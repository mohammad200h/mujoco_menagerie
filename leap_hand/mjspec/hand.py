from finger import Finger
import mujoco as mj
import numpy as np

class Hand(object):
  def __init__(self,asset_path:str,
               prop:dict,
               file_name:str,
               finger_data:dict,
               thumb_data:dict
              ):
    self.spec = mj.MjSpec()
    self.spec.compiler.degree = False

    # defaults
    main = self.spec.default()

    main.geom.type = mj.mjtGeom.mjGEOM_MESH
    # position actuation setting
    kp = 20
    dampratio = 1
    main.actuator.trntype = mj.mjtTrn.mjTRN_JOINT
    main.actuator.gaintype = mj.mjtGain.mjGAIN_FIXED
    main.actuator.biastype = mj.mjtBias.mjBIAS_AFFINE
    main.actuator.gainprm[0] =  kp
    main.actuator.biasprm[1] = -kp
    main.actuator.biasprm[2] = dampratio

    # add mesh
    self.spec.add_mesh(name=file_name, file=asset_path+file_name+'.stl')

    # add material
    self.spec.add_material(name='black',rgba=[.2, .2, .2, 1])

    self.model = self.spec.worldbody
    #body
    body = self.model.add_body( **prop['body'])
    #geoms
    for g in prop['geoms']:
      body.add_geom(**g)

    # Frames
    finger_frame_quat = prop["finger_frame_quat"]
    thumb_frame_quat = prop["thumb_frame_quat"]
    frames = prop["frames_pos"]

    # attaching fingers
    frame_names = ["FirstFinger","MiddleFinger","RingFinger"]
    for idx,frame in enumerate(frames[:-1]):
      finger_prefix = finger_data['fingers_prefix'][idx]
      f = body.add_frame(name=frame_names[idx],pos=frame, quat=finger_frame_quat)
      f.attach_body(Finger(finger_data['props'],asset_path,finger_data['filenames']).model,finger_prefix,'')

    # attaching thumb
    thumb_prefix = thumb_data['th_prefix']
    f = body.add_frame(name="Thumb",pos=frames[-1], quat=thumb_frame_quat)
    f.attach_body(Finger(thumb_data['props'],asset_path,thumb_data['filenames']).model,thumb_prefix,'')

    # palm contact excludes
    for b2 in prop["p_contacts"]["bodyname2"]:
      self.spec.add_exclude(bodyname1=prop["p_contacts"]["bodyname1"],
                            bodyname2=b2)
    # other contacts
    for prefix in prop["contacts"]["prefix"]:
      b1 = prefix+prop["contacts"]["bodyname1"]
      b2 = prefix+prop["contacts"]["bodyname2"]
      self.spec.add_exclude(bodyname1=b1,
                            bodyname2=b2)

    # https://github.com/google-deepmind/mujoco/blob/1d58576d284f2cfb33ba872de5fd23fe1e54e47e/src/xml/xml_native_reader.cc#L2186
    # ReadAttr(elem, "kp", 1, actuator->gainprm, text);
    # actuator->biasprm[1] = -actuator->gainprm[0];
    # (ReadAttr(elem, "kv", 1, &kv, text))
    # actuator->gaintype = mjGAIN_FIXED;
    # actuator->biastype = mjBIAS_AFFINE;
    #  if (dampratio > 0) actuator->biasprm[2] = dampratio;
    # position actuator

    # inputs to add_actuator:
    # Valid options are: name, gaintype, gainprm, biastype, biasprm, dyntype, dynprm, actdim,
    # actearly, trntype, gear, target, refsite, slidersite, cranklength, lengthrange, inheritrange,
    # ctrllimited, ctrlrange, forcelimited, forcerange, actlimited, actrange, group, userdata, plugin, info.

    actuators = thumb_data['props']['actuators']
    for idx in range(actuators['range'][1]):
      name = thumb_prefix+actuators['name']+str(idx)
      target = thumb_prefix+actuators['target']+str(idx)
      self.spec.add_actuator(name= name,target= target)


    actuators = finger_data['props']['actuators']
    for finger_prefix in finger_data['fingers_prefix']:
      for idx in range(actuators['range'][1]):
        name = finger_prefix+actuators['name']+str(idx)
        target = finger_prefix+actuators['target']+str(idx)
        self.spec.add_actuator(name= name,target= target)



def create_hand(leap_data:dict, asset_path:str):
  # default data
  geom_vis_default = leap_data['geom_vis_default']
  geom_col_default = leap_data['geom_col_default']

  # finger data
  tree_props = [leap_data['mcp_joint'],
              leap_data['pip'],
              leap_data['dip'],
              leap_data['fingertip']
  ]
  actuators = leap_data['finger_actuators']

  # adding defaults to geoms
  for prop in tree_props:
    prop['geoms'][0] |= geom_vis_default
    prop['geoms'][1] |= geom_col_default

  ff_props = {
      'tree':tree_props,
      'actuators': actuators
  }

  ff_filenames = ['mcp_joint','pip','dip','fingertip']

  # thumb data
  tree_props = [leap_data['pip_4'],
              leap_data['thumb_pip'],
              leap_data['thumb_dip'],
              leap_data['thumb_fingertip']
  ]
  actuators = leap_data['thumb_actuators']

  # adding defaults to geoms
  for prop in tree_props:
    prop['geoms'][0] |= geom_vis_default
    prop['geoms'][1] |= geom_col_default

  th_props = {
      'tree':tree_props,
      'actuators': actuators
  }

  th_filenames = ['pip','thumb_pip','thumb_dip','thumb_fingertip']

  # hand data
  hand_prop = leap_data['hand']
  file_name = "palm_lower_left"

  hand_prop['geoms'][0] |= geom_vis_default
  hand_prop['geoms'][1] |= geom_col_default

  finger_data = {
    'props':ff_props,
    'filenames':ff_filenames,
    'fingers_prefix':leap_data['fingers_prefix']
  }
  thumb_data = {
      'props':th_props,
      'filenames':th_filenames,
      'th_prefix':leap_data['thump_prefix']
  }

  actuators = leap_data['thumb_actuators']

  # creating hand
  hand = Hand(asset_path,
              hand_prop,
              file_name,
              finger_data,
              thumb_data
        )

  hand.spec.worldbody.add_light(name="top", pos=[0, 0, 1])
  model = hand.spec.compile()
  xml = hand.spec.to_xml()
  with open("leap.xml", "w") as file:
   # Write content to the file
   file.write(xml)


  return model
