# =============================================================================
# (C) Copyright 2014
# Australian Centre for Microscopy & Microanalysis
# The University of Sydney
# =============================================================================
# File:   properties.py
# Date:   2014-07-01
# Author: Varvara Efremova
#
# Description:
# AtomBlend Blender global property definitions.
# =============================================================================
import bpy

from bpy.types import PropertyGroup
from bpy.props import BoolProperty, StringProperty, EnumProperty, FloatProperty, FloatVectorProperty

# TODO this should go in some global settings module
DEFAULT_COLOR = (0, 0.144, 0.554)

# === Global scene properties ===
# Array for APTloader objects
bpy.types.Scene.aptdata = {}

# === Custom AtomBlend object RNA properties ===
# Define AtomBlend-specific RNA props for every object

# Defines object type in AtomBlend framework
# Default: BLENDER for objects independent of AtomBlend
dtypes = [('BLENDER', "Blender",  "Blender"),
          ('DATA',    "Dataset",  "Dataset"),
          ('BOUND',   "Boundbox", "Boundbox")]
bpy.types.Object.datatype = EnumProperty(
        name = "Type of object (AtomBlend)",
        items = dtypes,
        default = 'BLENDER'
        )

# Type of visualisation applied
vtypes = [('NONE',  "None",  "None"),
          ('HALO',  "Halo",  "Halo"),
          ('DUPLI', "Dupli", "Dupli")]
bpy.types.Object.vistype = EnumProperty(
        name = "Type of visualisation (AtomBlend)",
        items = vtypes,
        default = 'NONE'
        )

# === General panel properties ===
class VIEW3D_PT_pos_panel_props(PropertyGroup):
    """ POS reader panel property group

    Properties:
    pos_filename -- POS file path
    rng_filename -- RNG file path
    plot_type -- Enumerator in ['ISO', 'EA', 'ION']
                 Plot by isotope, atom, or ion
    atoms, rngs, ions -- Enumerators for atoms/rngs/ions loaded from files
    """

    pos_filename = StringProperty(\
            name = "",
            description = "Input .pos file",
            default = "/"
        )

    rng_filename = StringProperty(\
            name = "",
            description = "Input .rng file",
            default = "/"
        )

    # Function to return enum list of loaded pos files from current context
    def aptdata_enum(self, context):
        items = []
        for key in context.scene.aptdata:
            items.append((key, key, key))
        return items

    file_list = EnumProperty(name="File", items=aptdata_enum)

    plot_options = [('EA', "Atomic", "Atomic"), ('ION', "Ionic", "Ionic"), ('ISO', "Isotopic", "Isotopic")]
    plot_type = EnumProperty(name="Bake options", items=plot_options)

    # Boundbox padding
    boundbox_padding = FloatProperty(
            name="Padding",
            description="Bounding box padding",
            default=0.5,
            min=0.0, max=100.0,
            )

    animation_scale     = FloatProperty(default=80, min=0)
    animation_clip_dist = FloatProperty(default=500, min=0)
    animation_time      = FloatProperty(default=4, min=0)
    animation_fps       = FloatProperty(default=25, min=0)

    animation_offsetx    = FloatProperty(default=100)
    animation_offsetz    = FloatProperty(default=50)

    analysis_isosurf_rangefrom = FloatProperty(default=0,  min=0)
    analysis_isosurf_rangeto   = FloatProperty(default=1, min=0)
