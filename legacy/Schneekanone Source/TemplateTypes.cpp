/******************************************************************************TemplateTypes.c   ******************************************************************************/#include "TemplateTypes.h"void	ConvertToMoveObject(MoveObjectRec * moveObject,					FixedObjectRec * fixedObject){	MoveObjectRec	retObject;		moveObject->objectPosX = fixedObject->objectPosX;	moveObject->objectPosY = fixedObject->objectPosY;	moveObject->spriteID = fixedObject->spriteID;	moveObject->spriteCount = fixedObject->spriteCount;	moveObject->deltaX = fixedObject->deltaX;	moveObject->deltaY = fixedObject->deltaY;	moveObject->moveX = 0;	moveObject->moveY = 0;	moveObject->moveDelay = -1;	moveObject->moveDelayMult = 1;	moveObject->baseX = -1;	moveObject->baseY = -1;}