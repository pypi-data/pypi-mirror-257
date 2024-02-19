import typing
from . import anim
from . import object
from . import vertexpaint_dirt
from . import image
from . import screen_play_rendered_anim
from . import bmesh
from . import spreadsheet
from . import mesh
from . import node
from . import wm
from . import freestyle
from . import clip
from . import console
from . import assets
from . import file
from . import geometry_nodes
from . import object_align
from . import constraint
from . import uvcalc_lightmap
from . import add_mesh_torus
from . import presets
from . import userpref
from . import object_quick_effects
from . import uvcalc_follow_active
from . import view3d
from . import sequencer
from . import uvcalc_transform
from . import rigidbody
from . import object_randomize_transform

GenericType = typing.TypeVar("GenericType")

def register(): ...
def unregister(): ...
