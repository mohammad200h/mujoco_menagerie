import mujoco as mj

class Arena(object):
  def __init__(self):
    self.spec = mj.MjSpec()
    self.model = self.spec.worldbody

    # Make arena with textured floor.
    chequered = self.spec.add_texture(
      name="chequered", type=mj.mjtTexture.mjTEXTURE_2D,
      builtin=mj.mjtBuiltin.mjBUILTIN_CHECKER,
      width=300, height=300, rgb1=[.2, .3, .4], rgb2=[.3, .4, .5])
    grid = self.spec.add_material(
      name='grid', texrepeat=[5, 5], reflectance=.2
    ).textures[mj.mjtTextureRole.mjTEXROLE_RGB] = 'chequered'

    self.model.worldbody.add_geom(
      type=mj.mjtGeom.mjGEOM_PLANE,
      size=[2, 2, .1], material='grid')

    for x in [-2, 2]:
      self.model.worldbody.add_light(pos=[x, -1, 3], dir=[-x, 1, -2])

def create_arena():
  arena = Arena()

  return arena