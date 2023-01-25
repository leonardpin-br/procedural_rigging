# -*- coding: utf-8 -*-
u"""headParts @ rig
"""

import maya.cmds as mc

from .. base import module
from .. base import control


def build(headJnt,
          jawJnt,
          muzzleJoints,
          leftEyeJnt,
          rightEyeJnt,
          prefix="headParts",
          rigScale=1.0,
          baseRig=None
          ):
    u"""_summary_

    Args:
        headJnt (str): Name of head joint.
        jawJnt (str): Name of jaw joint.
        muzzleJoints (list[str]): List with 2 muzzle joints chain.
        leftEyeJnt (str): Name of left eye joint.
        rightEyeJnt (str): Name of right eye joint.
        prefix (str, optional): Prefix to name new objects. Defaults to "headParts".
        rigScale (float, optional): Scale factor for size of controls. Defaults to 1.0.
        baseRig (``rigLib.base.module.Base, optional``): Instance of ``rigLib.base.module.Base``. Defaults to None.

    Returns:
        Dictionary with rig module objects.

        {"module": `rigLib.base.module.Module`}
    """

    # make rig module
    rigmodule = module.Module(prefix=prefix, baseObj=baseRig)

    # make attach groups

    headAttachGrp = mc.group(n="{}BaseAttach_grp".format(prefix),
                             em=1,
                             p=rigmodule.controlsGrp)
    mc.parentConstraint(headJnt, headAttachGrp, mo=1)

    # make controls

    jawCtrl = control.Control(prefix="jaw",
                              translateTo=jawJnt,
                              rotateTo=jawJnt,
                              scale=(rigScale * 4),
                              parent=headAttachGrp,
                              shape="circleY")

    muzzleCtrl1 = control.Control(prefix="muzzle1",
                                  translateTo=muzzleJoints[0],
                                  rotateTo=muzzleJoints[0],
                                  scale=rigScale,
                                  parent=headAttachGrp,
                                  lockChannels=["t", "s", "v"])

    muzzleCtrl2 = control.Control(prefix="muzzle2",
                                  translateTo=muzzleJoints[1],
                                  rotateTo=muzzleJoints[1],
                                  scale=rigScale,
                                  parent=muzzleCtrl1.C,
                                  lockChannels=["t", "s", "v"])

    leftEyeCtrl = control.Control(prefix="l_eye",
                                  translateTo=leftEyeJnt,
                                  rotateTo=leftEyeJnt,
                                  scale=rigScale,
                                  parent=headAttachGrp,
                                  shape="circleZ",
                                  lockChannels=["t", "s", "v"])

    rightEyeCtrl = control.Control(prefix="r_eye",
                                   translateTo=rightEyeJnt,
                                   rotateTo=rightEyeJnt,
                                   scale=rigScale,
                                   parent=headAttachGrp,
                                   shape="circleZ",
                                   lockChannels=["t", "s", "v"])

    # attach joints

    mc.parentConstraint(jawCtrl.C, jawJnt)
    mc.parentConstraint(muzzleCtrl1.C, muzzleJoints[0])
    mc.parentConstraint(muzzleCtrl2.C, muzzleJoints[1])
    mc.parentConstraint(leftEyeCtrl.C, leftEyeJnt)
    mc.parentConstraint(rightEyeCtrl.C, rightEyeJnt)

    return {"module": rigmodule}
