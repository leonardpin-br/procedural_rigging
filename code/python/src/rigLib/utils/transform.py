# -*- coding: utf-8 -*-
u"""transform @ utils

Functions to manipulate and create transforms.
"""

import maya.cmds as mc

from . import name

def makeOffsetGrp(object, prefix=""):
    """Make offset group for given object.

    Args:
        object (:obj:`transform`): Transform object to get offset group.
        prefix (str, optional): Prefix to name new objects. Defaults to "".

    Returns:
        str: Name of new offset group.
    """

    if not prefix:
        prefix = name.removeSuffix(object)

    offsetGrp = mc.group(n=prefix + "Offset_grp", em=1)

    objectParents = mc.listRelatives(object, p=1)

    if objectParents:
        mc.parent(offsetGrp, objectParents[0])

    # Match object transform.
    mc.delete(mc.parentConstraint(object, offsetGrp))
    mc.delete(mc.scaleConstraint(object, offsetGrp))

    # Parent object under offset group.
    mc.parent(object, offsetGrp)

    return offsetGrp