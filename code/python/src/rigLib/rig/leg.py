# -*- coding: utf-8 -*-
u"""leg @ rig
"""

import maya.cmds as mc

from ..base import module
from ..base import control

from ..utils import joint
from ..utils import name


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

    # make IK handles

    if scapulaJnt:
        scapulaIk = mc.ikHandle(n="{}Scapula_ikh".format(prefix),
                                sol="ikSCsolver",
                                sj=scapulaJnt,
                                ee=legJoints[0])[0]

    legIk = mc.ikHandle(n="{}Main_ikh".format(prefix),
                        sol="ikRPsolver",
                        sj=legJoints[0],
                        ee=legJoints[2])[0]

    ballIk = mc.ikHandle(n="{}Ball_ikh".format(prefix),
                         sol="ikSCsolver",
                         sj=legJoints[2],
                         ee=legJoints[3])[0]

    mainToeIk = mc.ikHandle(n="{}MainToe_ikh".format(prefix),
                            sol="ikSCsolver",
                            sj=legJoints[3],
                            ee=legJoints[4])[0]

    mc.hide(legIk, ballIk, mainToeIk)

    for i, topToeJnt in enumerate(topToeJoints):
        toePrefix = name.removeSuffix(topToeJnt)[:-1]
        toeJoints = joint.listHierarchy(topToeJnt)

        toeIk = mc.ikHandle(n="{}_ikh".format(toePrefix),
                            sol="ikSCsolver",
                            sj=toeJoints[1],
                            ee=toeJoints[-1])[0]
        mc.hide(toeIk)
        mc.parent(toeIk, toeIkControls[i].C)

    # attach controls

    mc.parentConstraint(bodyAttachGrp, poleVectorCtrl.Off, mo=1)

    if scapulaJnt:
        mc.parentConstraint(baseAttachGrp, scapulaCtrl.Off, mo=1)

    # attach objects to controls

    mc.parent(legIk, ballCtrl.C)
    mc.parent(ballIk, mainToeIk, footCtrl.C)

    mc.poleVectorConstraint(poleVectorCtrl.C, legIk)

    if scapulaJnt:
        mc.parent(scapulaIk, scapulaCtrl.C)
        mc.pointConstraint(scapulaCtrl.C, scapulaJnt)

    # make pole vector connection line

    pvLinePos1 = mc.xform(legJoints[1], q=1, t=1, ws=1)
    pvLinePos2 = mc.xform(pvLocator, q=1, t=1, ws=1)
    poleVectorCrv = mc.curve(n="{}Pv_crv".format(prefix),
                             d=1,
                             p=[pvLinePos1, pvLinePos2])
    mc.cluster("{}.cv[0]".format(poleVectorCrv),
                n="{}Pv1_cls".format(prefix),
                wn=[legJoints[1], legJoints[1]],
                bs=True)
    mc.cluster("{}.cv[1]".format(poleVectorCrv),
                n="{}Pv2_cls".format(prefix),
                wn=[poleVectorCtrl.C, poleVectorCtrl.C],
                bs=True)
    mc.parent(poleVectorCrv, rigmodule.controlsGrp)
    mc.setAttr("{}.template".format(poleVectorCrv), 1)

    return {"module": rigmodule, "baseAttachGrp": baseAttachGrp, "bodyAttachGrp": bodyAttachGrp}
