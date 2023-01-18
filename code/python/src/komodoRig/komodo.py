#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""komodo dragon rig setup.

Main module.
"""
import sys
import maya.cmds as mc

from rigLib.base import control
from rigLib.base import module

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
