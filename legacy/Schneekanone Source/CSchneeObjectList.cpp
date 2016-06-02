/****************************************************************************** CSchneeObjectList.cp   ******************************************************************************/#pragma once#include "CSchneeObjectList.h"CSchneeObjectList::CSchneeObjectList(long initialItems)				  : CObjectList(initialItems ){	// code}CSchneeObjectList::~CSchneeObjectList(){	// code}void	CSchneeObjectList::InsertAtNthPosition(void * object, long index){	fArray[index - 1] = (long *)object;}void	CSchneeObjectList::MoveToAnotherPosition(long source, long destination){	void *	tempObject;		if( ! (source < 1 || source > fCount) ||		 	(destination < 1 || destination > fCount) )		if(source < destination)		{			tempObject = fArray[source - 1];					BlockMove(ObjectPtr(source + 1),					ObjectPtr(source),					(destination - source) * sizeof(void *) );					InsertAtNthPosition(tempObject, destination);		}		else if(source > destination)		{			tempObject = fArray[source - 1];						BlockMove(ObjectPtr(destination),					ObjectPtr(destination + 1),					(source - destination) * sizeof(void *) );					InsertAtNthPosition(tempObject, destination);		}}