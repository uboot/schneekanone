/****************************************************************************** CSchneeObjectList.h   ******************************************************************************/#pragma once#include "CObjectList.h"class CSchneeObjectList : public CObjectList {		public:				CSchneeObjectList(long initialItems = 4);	virtual	~CSchneeObjectList();		void		InsertAtNthPosition(void * object, long index);	void		MoveToAnotherPosition(long source, long destination);};