#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""komodo dragon rig setup.

Main module.
"""

import maya.cmds as mc

from rigLib.base import control
from rigLib.base import module
from rigLib.rig import spine

from . import project
from . import komodo_deform


sceneScale = project.sceneScale
mainProjectPath = project.mainProjectPath

modelFilePath = "%s/%s/model/%s_model.mb"
builderSceneFilePath = "%s/%s/builder/%s_builder.mb"

rootJnt = "root1_jnt"
headJnt = "head1_jnt"


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
