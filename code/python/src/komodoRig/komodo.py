# -*- coding: utf-8 -*-
u"""komodo dragon rig setup.

Main module.
"""

import maya.cmds as mc

from rigLib.base import control
from rigLib.base import module

from rigLib.rig import spine
from rigLib.rig import neck
from rigLib.rig import ikChain
from rigLib.rig import leg

from rigLib.utils import joint

from . import project
from . import komodo_deform


sceneScale = project.sceneScale
mainProjectPath = project.mainProjectPath

modelFilePath = "%s/%s/model/%s_model.mb"
builderSceneFilePath = "%s/%s/builder/%s_builder.mb"

rootJnt = "root1_jnt"
headJnt = "head1_jnt"
pelvisJnt = "pelvis1_jnt"
jawJnt = "jaw1_jnt"


def build(characterName):

    # new scene
    mc.file(new=True, f=True)

    # import builder scene
    builderFile = builderSceneFilePath % (
        mainProjectPath, characterName, characterName)
    mc.file(builderFile, i=1)

    # make base
    baseRig = module.Base(characterName=characterName,
                          scale=sceneScale, mainCtrlAttachObj=headJnt)

    # import model
    modelFile = modelFilePath % (mainProjectPath, characterName, characterName)
    mc.file(modelFile, i=1)

    # Parent model
    modelGrp = "%s_model_grp" % characterName
    mc.parent(modelGrp, baseRig.modelGrp)

    # Parent skeleton
    mc.parent(rootJnt, baseRig.jointsGrp)

    # deform setup
    komodo_deform.build(baseRig, characterName)

    # control setup
    makeControlSetup(baseRig)


def makeControlSetup(baseRig):
    """make control setup

    Args:
        baseRig (`rigLib.base.module.Base`): Instance of `rigLib.base.module.Base`.
    """

    # spine
    spineJoints = ['spine1_jnt', 'spine2_jnt', 'spine3_jnt',
                   'spine4_jnt', 'spine5_jnt', 'spine6_jnt']
    spineRig = spine.build(spineJoints=spineJoints,
                           rootJnt=rootJnt,
                           spineCurve="spine_crv",
                           bodyLocator="body_loc",
                           chestLocator="chest_loc",
                           pelvisLocator="pelvis_loc",
                           prefix="spine",
                           rigScale=sceneScale,
                           baseRig=baseRig
                           )

    # neck
    neckJoints = ['neck1_jnt', 'neck2_jnt', 'neck3_jnt',
                  'neck4_jnt', 'neck5_jnt', 'neck6_jnt']
    neckRig = neck.build(neckJoints,
                         headJnt=headJnt,
                         neckCurve="neck_crv",
                         prefix="neck",
                         rigScale=sceneScale,
                         baseRig=baseRig
                         )
    mc.parentConstraint(spineJoints[-2], neckRig["baseAttachGrp"], mo=1)
    mc.parentConstraint(spineRig["bodyCtrl"].C, neckRig["bodyAttachGrp"], mo=1)

    # tail
    tailJoints = joint.listHierarchy("tail1_jnt")
    tailRig = ikChain.build(chainJoints=tailJoints,
                            chainCurve="tail_crv",
                            prefix="tail",
                            rigScale=sceneScale,
                            smallestScalePercent=0.4,
                            fkParenting=False,
                            baseRig=baseRig)
    mc.parentConstraint(pelvisJnt, tailRig["baseAttachGrp"], mo=1)

    # tongue
    tongueJoints = joint.listHierarchy("tongue1_jnt")
    tongueRig = ikChain.build(chainJoints=tongueJoints,
                              chainCurve="tongue_crv",
                              prefix="tongue",
                              rigScale=sceneScale * 0.2,
                              smallestScalePercent=0.3,
                              fkParenting=True,
                              baseRig=baseRig)
    mc.parentConstraint(jawJnt, tongueRig["baseAttachGrp"], mo=1)
