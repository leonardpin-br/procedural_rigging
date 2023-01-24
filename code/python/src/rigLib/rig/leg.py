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

    # make rig module
    rigmodule = module.Module(prefix=prefix, baseObj=baseRig)

    # make attach groups
    bodyAttachGrp = mc.group(n="{}BodyAttach_grp".format(prefix),
                             em=1,
                             p=rigmodule.partsGrp)
    baseAttachGrp = mc.group(n="{}BaseAttach_grp".format(prefix),
                             em=1,
                             p=rigmodule.partsGrp)

    # make controls

    if scapulaJnt:
        scapulaCtrl = control.Control(prefix="{}Scapula".format(prefix),
                                      translateTo=scapulaJnt,
                                      rotateTo=scapulaJnt,
                                      scale=(rigScale * 3),
                                      parent=rigmodule.controlsGrp,
                                      shape="sphere",
                                      lockChannels=["ty", "rx", "rz", "s", "v"])

    footCtrl = control.Control(prefix="{}Foot".format(prefix),
                               translateTo=legJoints[2],
                               scale=(rigScale * 3),
                               parent=rigmodule.controlsGrp,
                               shape="circleY")

    ballCtrl = control.Control(prefix="{}Ball".format(prefix),
                               translateTo=legJoints[3],
                               rotateTo=legJoints[3],
                               scale=(rigScale * 2),
                               parent=footCtrl.C,
                               shape="circleZ")

    poleVectorCtrl = control.Control(prefix="{}PV".format(prefix),
                                     translateTo=pvLocator,
                                     scale=rigScale,
                                     parent=rigmodule.controlsGrp,
                                     shape="sphere")

    toeIkControls = []
    for topToeJnt in topToeJoints:
        toePrefix = name.removeSuffix(topToeJnt)[:-1]
        toeEndJnt = mc.listRelatives(topToeJnt, ad=1, type="joint")[0]

        toeIkCtrl = control.Control(prefix=toePrefix,
                                    translateTo=toeEndJnt,
                                    scale=rigScale,
                                    parent=footCtrl.C,
                                    shape="circleY")
        toeIkControls.append(toeIkCtrl)