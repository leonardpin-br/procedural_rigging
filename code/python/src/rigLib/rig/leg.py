# -*- coding: utf-8 -*-
u"""leg @ rig
"""

import maya.cmds as mc

from .. base import module
from .. base import control

from .. utils import joint
from .. utils import name


def build(legJoints,
          topToeJoints,
          pvLocator,
          scapulaJnt="",
          prefix="l_leg",
          rigScale=1.0,
          baseRig=None
          ):
    u"""_summary_

    Args:
        legJoints (``list[str]``): Shoulder, elbow, hand, toe, end toe.
        topToeJoints (``list[str]``): Top metacarpal toe joints.
        pvLocator (``str``): Reference locator for position of Pole Vector control.
        scapulaJnt (``str, optional``): Scapula joint, parent of top leg joint. Defaults to "".
        prefix (``str, optional``): Prefix to name new objects. Defaults to "l_leg".
        rigScale (``float, optional``): Scale factor for size of controls. Defaults to 1.0.
        baseRig (``rigLib.base.module.Base, optional``): Instance of ``rigLib.base.module.Base``. Defaults to None.

    Returns:
        Dictionary with rig module objects.
    """

