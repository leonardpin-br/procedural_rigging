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
    u"""_summary_

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

    # make rig module
    rigmodule = module.Module(prefix=prefix, baseObj=baseRig)

    # make chain curve clusters
    chainCurveCVs = mc.ls("{}.cv[*]".format(chainCurve), fl=1)
    numChainCVs = len(chainCurveCVs)
    chainCurveClusters = []

    for i in range(numChainCVs):
        clusterWithNumber = "Cluster%d" % (i + 1)
        cls = mc.cluster(chainCurveCVs[i], n="{}{}".format(prefix, clusterWithNumber))[1]
        chainCurveClusters.append(cls)
    mc.hide(chainCurveClusters)

    # parent chain curve
    mc.parent(chainCurve, rigmodule.partsNoTransGrp)

    # make attach groups
    baseAttachGrp = mc.group(n="{}BaseAttach_grp".format(prefix), em=1, p=rigmodule.partsGrp)
    mc.delete(mc.pointConstraint(chainJoints[0], baseAttachGrp))

    # make controls
    chainControls = []
    controlScaleIncrement = (1.0 - smallestScalePercent) / numChainCVs
    mainCtrlScaleFactor = 5.0

    for i in range(numChainCVs):
        crtlScale = rigScale * mainCtrlScaleFactor * (1.0 - (i * controlScaleIncrement))
        prefixNumber = "%d" % (i + 1)
        ctrl = control.Control(prefix="{}{}".format(prefix, prefixNumber),
                                translateTo=chainCurveClusters[i],
                                scale=crtlScale,
                                parent=rigmodule.controlsGrp,
                                shape="sphere")