# -*- coding: utf-8 -*-
u"""ikChain @ rig
"""

import maya.cmds as mc

from .. base import module
from .. base import control


def build(chainJoints,
          chainCurve,
          prefix="tail",
          rigScale=1.0,
          smallestScalePercent=0.5,
          fkParenting=True,
          baseRig=None
          ):
    """_summary_

    Args:
        chainJoints (list[str]): List of chain joints.
        chainCurve (str): Name of chain cubic curve.
        prefix (str, optional): Prefix to name new objects. Defaults to "tail".
        rigScale (float, optional): Scale factor for size of controls. Defaults to 1.0.
        smallestScalePercent (float, optional): Scale of smallest control at the end of chain compared to rigScale. Defaults to 0.5.
        fkParenting (bool, optional): Parent each control to previous one to make FK chain. Defaults to True.
        baseRig (`rigLib.base.module.Base`, optional): Instance of `rigLib.base.module.Base`. Defaults to None.

    Returns:
        Dictionary with rig module objects.
    """
