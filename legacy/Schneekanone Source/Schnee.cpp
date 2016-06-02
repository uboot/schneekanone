/****   Schnee.cp**  	Copyright � 1996-1997 Fuchs Matthias*	All rights reserved.***   ***/#include <Traps.h>#include "Error.h"#include "CGame.h"#include "ErrorHandler.h"#include "CPlayer.h"#include "CEnemy.h"#include "CPlayField.h"#include "CSpriteGroup.h"#include "CSoundFX.h"#include "Global.h"#include "CommonUtilities.h"#include "Assert.h"//============================== Defines ==========================================#define kGameWindowHeight		480#define kGameWindowWidth		640#define kMaxNumberofMasterPointers  10#define kWrongHardwareOrSystemErr   1000#define kApplStackSize              40000#define kCantRunALRT_id             3000#define kMemoryNeededForCode        100000#define kAppleMenuID            128#define kAboutItem              1    #define kFileMenuID             129#define	kPlayGame				1#define kResumeGame				2#define kLoadGame				4#define kSaveGame				5#define kQuit                   7    #define kEditMenuID             130    #define kAboutBoxALRT_ID        4000#define kAppInBackgroundSleepAmount         60#define kAppInForegroundSleepAmount			 0//=================================Global variables========================================CSoundFX *			gSchneeSndFX = nil;CPlayField *		gPiste = nil;SystemStatsRec  	gSystemStats;Boolean        	gAppIsRunning = TRUE;Boolean        	gAppIsInBackground = FALSE;WindowPtr       	gMainWindow;StandardFileReply	gLastReply;Boolean			gFirstFile = true;CGame				gCurrentGame;//======================================Forward prototypes================================void 	DealWithMenuCommand(long menuItem_Id);void 	DealWithNullEvent(void);void 	DealWithAppleMenuCommand(short menuItem);void 	DealWithFileMenuCommand(short menuItem);void 	DealWithEditMenuCommand(short menuItem);void 	DealWithMouseEvent(const EventRecord * eventPtr);void 	DealWithActivateEvent( WindowPtr activateWindowPtr);void 	DealWithUpdateEvent(WindowPtr updateWindowPtr);void 	DealWithKeyEvent(char key,short modifiers);static void			AppleEventInit(void);static pascal OSErr	DoOpenApp(const AppleEvent *theAppleEvent,								AppleEvent *reply, long refCon);static pascal OSErr	DoOpenDoc(const AppleEvent *theAppleEvent,								AppleEvent *reply, long refCon);static pascal OSErr	DoPrintDoc(const AppleEvent *theAppleEvent,								AppleEvent *reply, long refCon);static pascal OSErr	DoQuitApp(const AppleEvent *theAppleEvent,								AppleEvent *reply, long refCon);static OSErr			MyGotRequiredParams(const AppleEvent *theAppleEvent);void	ShutdownSound(void);Boolean	StartUpSound(void);void	ProcessSounds(void);/************************************************************ DiggerErrorHandler	Macsbug's based error handler   ************************************************************/void DiggerErrorHandler(OSErr error, long refcon){	DebugStr("\pFatal Error. See Ya!");	ExitToShell();}	/*********************************************************** InitMacApplication    Intialize all the mac managers used by this application.***********************************************************/             static  void    InitMacApplication(short numberMasterPtrs,                     long stackSize){    long newApplLimit;    EventRecord tempEvent;        // set the stack to the size asked for.      // Unless the caller was stupid enough to pass in a     // stack size smaller than the default.    if (stackSize > LMGetDefltStack())    {        newApplLimit = (long) GetApplLimit() -                                                      (stackSize - LMGetDefltStack());        SetApplLimit( (Ptr) newApplLimit);    }        // Stack is setup, so now lets expand out our heap to       // its maximum size    MaxApplZone();        // Heap has been stretched out, lets create all those       // master pointers that the caller asked for    while (numberMasterPtrs--)        MoreMasters();    // Fire up the those mac manager that we will really,       // really need.    InitGraf(&qd.thePort);    InitFonts();    InitWindows();    InitMenus();    TEInit();    InitDialogs((long)NULL);    // Clean up the cursor.    InitCursor();        // Clear out any stray events that might be lying     // around    FlushEvents(everyEvent, 0);        AppleEventInit();    // Hack: to wake up multi-finder type enviroments we        // need to ask for a few events so multifinder will     // get a clue and realize we are the frontmost     // application.    (void)EventAvail(everyEvent, &tempEvent);    (void)EventAvail(everyEvent, &tempEvent);    (void)EventAvail(everyEvent, &tempEvent);}/*********************************************************** GatherSystemStats    Fill in the statistics of the system and hardware the app is running on***********************************************************/static  void    GatherSystemStats(SystemStatsRec * systemStats){    OSErr       err;    SysEnvRec   environs;    long        response;    err = SysEnvirons( 1, &environs);    systemStats->hasWNE = WNEIsImplemented();    systemStats->hasGestalt = MyTrapAvailable( _Gestalt);    systemStats->hasScriptMgr = MyTrapAvailable(_ScriptUtil);        // assume only Roman script    systemStats->scriptsInstalled =  1;    err = SysEnvirons( 1, &environs);    if (err == noErr)    {        systemStats->hasColorQD = environs.hasColorQD;        systemStats->hasFPU = environs.hasFPU;        systemStats->systemVersion =                                 environs.systemVersion;    }    else    {        systemStats->hasColorQD = FALSE;        systemStats->hasFPU = FALSE;        systemStats->systemVersion = 0;    }    // get stats on features that require Gestalt in order    // to interrogate their existence    if (systemStats->hasGestalt)    {        systemStats->hasAppleEvents = Gestalt(                                    gestaltAppleEventsAttr,                                     &response) == noErr;        systemStats->hasAliasMgr = Gestalt(                                                                 gestaltAliasMgrAttr,                                    &response) == noErr;        systemStats->hasEditionMgr = Gestalt(                                                               gestaltEditionMgrAttr,                                    &response) == noErr;        systemStats->hasHelpMgr = Gestalt(                                                                  gestaltHelpMgrAttr,                                    &response) == noErr;                if (Gestalt(gestaltQuickdrawVersion, &response))            response = 0;        systemStats->has32BitQD = response >=                             gestalt32BitQD ? TRUE:FALSE;                if (systemStats->hasScriptMgr)        {            err = Gestalt( gestaltScriptCount, &response);            if (err == noErr)                systemStats->scriptsInstalled =                                         (short) response;        }    }    else    {        // If we don't have Gestalt, then we can't have                 // any System 7 features                systemStats->hasAppleEvents = FALSE;        systemStats->hasAliasMgr = FALSE;        systemStats->hasEditionMgr = FALSE;        systemStats->hasHelpMgr = FALSE;        systemStats->has32BitQD = FALSE;        if (systemStats->hasScriptMgr)            systemStats->scriptsInstalled =                                 GetEnvirons( smEnabled);                }    if(Gestalt(gestaltQuickTime,&response) == noErr)        systemStats->hasQuickTime = TRUE;    else        systemStats->hasQuickTime = FALSE;}/***********************************************************    DealWithMouseEvent        Dispatch the mouse event   ***********************************************************/void    DealWithMouseEvent(const EventRecord * eventPtr){    WindowPtr whichWindow;    short partCode;    // find out where the user clicked    partCode = FindWindow(eventPtr->where, &whichWindow);    switch(partCode)    {        case inMenuBar:        	if(!gCurrentGame.PlayerDead())        		EnableItem(GetMenu(kFileMenuID), kResumeGame);        	else        		DisableItem(GetMenu(kFileMenuID), kResumeGame);        		            DealWithMenuCommand(MenuSelect(eventPtr->where));        break;                    case inSysWindow:                   SystemClick(eventPtr, whichWindow);        break;    }}/*********************************************************** RunApplication    Event loop code for the application.  All events are gathered and then examined.  From the examination the event is dispatched off to a function that will deal that  specific event type.***********************************************************/static  void    RunApplication(void){    long        appSleepTime;    Boolean     gotAnEvent;    EventRecord event;    RgnHandle   WNE_MouseRgn = NewRgn();    long        timeWaitNextEvent;    long        max_WNE_Time = 0;    long        maxFrameRate = 0;    long        minFrameRate = 30000;    long        startTime;    long        frameCount = 0;    long        WNE_Time;        startTime = TickCount();	if(!StartUpSound())		return;    // make sure app is supposed to be running.    while(gAppIsRunning)            {        if (gSystemStats.hasWNE)        {            frameCount++;                        if(gAppIsInBackground)                appSleepTime = kAppInBackgroundSleepAmount;            else                appSleepTime = kAppInForegroundSleepAmount;                        timeWaitNextEvent = TickCount();            gotAnEvent = WaitNextEvent(everyEvent,                                                              &event,                                         appSleepTime,                                        WNE_MouseRgn);            WNE_Time = TickCount() - timeWaitNextEvent;            max_WNE_Time = Max(WNE_Time, max_WNE_Time);                        if(TickCount() >= startTime + 60)            {                maxFrameRate = Max(frameCount,maxFrameRate);                minFrameRate = Min(frameCount,minFrameRate);                startTime = TickCount();                frameCount = 0;            }        }        else        {        // give a slice of time to DA's and drivers.            SystemTask();                                       gotAnEvent = GetNextEvent(everyEvent,&event);        }        if (gotAnEvent)        {            switch(event.what)            {                case mouseDown:                             DealWithMouseEvent(&event);                break;                                                case keyDown:                case autoKey:                    DealWithKeyEvent((char)                        (event.message &charCodeMask),                             event.modifiers);                break;                                case updateEvt:                     DealWithUpdateEvent((WindowPtr)                            event.message);                break;                                                case activateEvt:                               DealWithActivateEvent((WindowPtr)                            event.message);                break;                case diskEvt:                    Point loc = {100,100};                                    	if (HiWord(event.message != noErr))                    {                    	DILoad();                    	DIBadMount(loc, event.message);                    	DIUnload();                    }                break;                case osEvt:                     if ((event.message >> 24) ==                         suspendResumeMessage)                {                               if ((event.message & resumeFlag) != 0)                    {                        gAppIsInBackground = FALSE;                        ShowWindow(gMainWindow);					}                    else                    {                        gAppIsInBackground = TRUE;                        HideWindow(gMainWindow);					}                }                break;                                     case kHighLevelEvent: 					if (AEProcessAppleEvent(&event) != noErr)					{ /* error - ignored */ };				break; 				                          default:                break;            }        }        else        {            DealWithNullEvent();        }    }       	ShutdownSound();    if (WNE_MouseRgn != NULL)        DisposeRgn(WNE_MouseRgn);        }/*********************************************************** HaveEnoughMemoryToRun        Verify that the app's memory partition is big enough     to run the application    ***********************************************************/staticBoolean HaveEnoughMemoryToRun(void){    long memoryNeededToRun;    long actualAmountMemory;    GDHandle mainGDeviceHndl;    Rect screenRect;    short pixelSize;    Boolean haveEnoughMemory;    if (gSystemStats.hasColorQD)    {        mainGDeviceHndl = GetMainDevice();        screenRect = (*mainGDeviceHndl)->gdRect;        pixelSize =             (**(**mainGDeviceHndl).gdPMap).pixelSize;    }    else    {        screenRect = qd.screenBits.bounds;        pixelSize = 1;    }    // determine how big an offscreen buffer the size of        // the main screen (the one with the menu bar) and     // main screen bits deep will use up in memory.     memoryNeededToRun = ((((screenRect.right -                             screenRect.left) *                            (screenRect.bottom -                                                    screenRect.top)) *                             pixelSize) / 8);                                // add enough above the offscreen to fit the code and       // other misc. stuff into the heap.    memoryNeededToRun += kMemoryNeededForCode;    actualAmountMemory = (long)GetApplLimit() -                                         (long)ApplicZone();    haveEnoughMemory = (actualAmountMemory >                                         memoryNeededToRun);    if (!haveEnoughMemory)        PostErrorAlert(memFullErr);    return haveEnoughMemory;}/*********************************************************** ShutdownApplication     App is about to quit, we need to shutdown,dispose or free anything that needs to be shutdown,disposed of or freed before we quit. Mostly we should just undo whatever was done in the function "InitThisApplication."    ***********************************************************/staticvoid ShutdownApplication(void){    DisposeWindow(gMainWindow);}/*********************************************************** BuildMenuBar        Install the main menu bar for this application    ***********************************************************/static  void BuildMenuBar(void){    #define kMainMenuBar_ID 128    Handle menuBarH;    menuBarH = GetNewMBar(kMainMenuBar_ID);    if (menuBarH != NULL)    {        MenuHandle  animationMenuH;        SetMenuBar(menuBarH);        AddResMenu(GetMHandle(kAppleMenuID), 'DRVR');        DrawMenuBar();            }    else        PostFatalError(resNotFound);}/*********************************************************** BuildMainWindow     Build a window that will be the main playfield for our game    ***********************************************************/staticvoid    BuildMainWindow(void){    #define kMainWindow_ID  128        	gMainWindow = GetNewCWindow(kMainWindow_ID, NULL, (WindowPtr)-1L);    if (gMainWindow != NULL)    {        GDHandle mainGDeviceHndl;        Rect    screenRect, windowRect;                mainGDeviceHndl = GetMainDevice();        screenRect = (*mainGDeviceHndl)->gdRect;        screenRect.top += GetMBarHeight();        SetRect(&windowRect,0,0,kGameWindowWidth,                                                           kGameWindowHeight);        CenterRectWithinRect(&screenRect, &windowRect);        SizeWindow(gMainWindow, kGameWindowWidth,                                                           kGameWindowHeight,                                     false);        MoveWindow(gMainWindow, windowRect.left,                                 windowRect.top, false);    }    else    {        PostFatalError(resNotFound);    }}/*********************************************************** CanOurAppRun     Verify that this machine has the "right stuff" for our app to run. The right stuff in at least system software, memory and roms.    ***********************************************************/staticBoolean CanOurAppRun(void){    Boolean canRun = true;    // We require a system running with at least 32 bit         // QuickDraw        canRun = gSystemStats.has32BitQD;    // we saw that we have enough system to run, now make       // sure we have enough of the good stuff.    canRun &= HaveEnoughMemoryToRun();        // make sure the main device is set at 256 colors    {    	GDHandle	gdh;    	OSErr		err;    		   	gdh = GetMainDevice();    	if(  (*(*gdh)->gdPMap)->pixelSize != 8)    	{    		HIG_PositionDialog('ALRT', 200);    		NoteAlert(200, nil);    		canRun = FALSE;    	}	    }    return canRun;}/*********************************************************** InitThisApplication     Do any one time initializations that the application needs running.    ***********************************************************/staticvoid InitThisApplication(void){    BuildMenuBar();    BuildMainWindow();	gCurrentGame.InitGame();	    // Make the main window visible     ShowWindow(gMainWindow);    SetPort(gMainWindow);        EraseRect(&gMainWindow->portRect);    }/************************************************************ myDlogFilter	Dialog filter that keeps the sounds playing   ************************************************************/static pascal Boolean myDlogFilter( DialogPtr dlg, EventRecord * theEvent, short * itemHit){	gSchneeSndFX->SoundFXTask();	return FALSE;}/*********************************************************** DealWithNullEvent        Here is where the application does whatever it does     with null events. In our case we keep the animation    running.       ***********************************************************/void DealWithNullEvent(void){}/*********************************************************** DealWithMenuCommand     Here is where the application does whatever it does with null events. In our case we keep the animation running.       ***********************************************************/void DealWithMenuCommand(long menuItem_Id){    short menuId = HiWord(menuItem_Id);    short menuItem = LoWord(menuItem_Id);    switch (menuId)    {        case kAppleMenuID:            DealWithAppleMenuCommand(menuItem);            break;        case kFileMenuID:            DealWithFileMenuCommand(menuItem);            break;        case kEditMenuID:            DealWithEditMenuCommand(menuItem);            break;    }    HiliteMenu(0);}/*********************************************************** DealWithAppleMenuCommand        Either display the about box or open a desk accesory  ***********************************************************/void DealWithAppleMenuCommand(short menuItem){    Str255 deskAccName;    switch (menuItem)    {        case kAboutItem:            HIG_PositionDialog( 'ALRT', kAboutBoxALRT_ID);            Alert(kAboutBoxALRT_ID, NULL);            break;        default:            GetItem(GetMHandle(kAppleMenuID), menuItem,                                             deskAccName);            OpenDeskAcc(deskAccName);            break;    }}/*********************************************************** DealWithFileMenuCommand          ***********************************************************/void DealWithFileMenuCommand(short menuItem){    switch (menuItem)    {    	case kPlayGame:    		gCurrentGame.ResetGame();    		gCurrentGame.Game();    		break;    		    	case kResumeGame:    		gCurrentGame.Game();    		break;    		    	case kLoadGame:    		gCurrentGame.LoadGame(true);    		break;    		    	case kSaveGame:    		gCurrentGame.SaveGame(true);    		break;    		        case kQuit:            gAppIsRunning = false;            break;    }}/*********************************************************** DealWithEditMenuCommand          ***********************************************************/void DealWithEditMenuCommand(short menuItem){    // make sure desk accessories get access to edit menu       // commands    SystemEdit(menuItem);}/*********************************************************** DealWithActivateEvent          ***********************************************************/void DealWithActivateEvent( WindowPtr activateWindowPtr){}/*********************************************************** DealWithUpdateEvent   ***********************************************************/void DealWithUpdateEvent(WindowPtr updateWindowPtr){    if (updateWindowPtr == gMainWindow)    {        SetPort(gMainWindow);        BeginUpdate(gMainWindow);        		if(gPiste)		{			gPiste->HandlePlayFieldUpdate(&gMainWindow->portRect);		}        EndUpdate(gMainWindow);    }}/*********************************************************** DealWithKeyEvent   ***********************************************************/void DealWithKeyEvent(char key,short modifiers){    if ((modifiers & cmdKey) != 0)    	DealWithMenuCommand(MenuKey(key));}/*********************************************************** main    C's natural entry point.  In here the application will be intialized, ran and then killed (exited).  Dispatching is all that happens here.***********************************************************/void    main(void){    // Install error handler    SetSLVGErrorHandler(DiggerErrorHandler, 0L);    // fire up all the mac managers.    InitMacApplication(kMaxNumberofMasterPointers,                                                                          kApplStackSize);        // Check out the current stats of the machine and     // system the app is running on. These stats are        // stored in the global structure "gSystemStats."    GatherSystemStats(&gSystemStats);        // verify that we have the needed resources to run      // this application.    if(CanOurAppRun())    {        // After the system has been checked out do any                 // one time intialization that is needed for                // this specific application        InitThisApplication();                // Run the event loop that drives our application.        RunApplication();                // user must have selected quit.  Let's do any              // application specific shutting down here.        ShutdownApplication();    }    else    {        // can't run on this system.  Inform the user         // and let's get our butts out of here                PostErrorAlert(kWrongHardwareOrSystemErr);    }     	ExitToShell();}/************************************************************ KillOffCurrentPlayer	Player has tripped up. Reflect that and start the 	level over.   ***********************************************************void	KillOffCurrentPlayer(void){	gPlayerLives--;		gLifeCountSprite->Refresh();	CMonster::ResetMonstersToStart();	if(gPlayerLives)	{		gPlayerSprite->InitPlayer();		PerformLevelGetReady(2);	}	gDiggerPlayfield->HandlePlayFieldUpdate(&gMainWindow->portRect);}*//************************************************************ PerformGameOverCelebration	Player lost all their lives. Celebrate   ***********************************************************void	PerformGameOverCelebration(void){	DialogPtr	gameOverDlg;	short		itemHit;		gSchneeSndFX->PlaySnd(kGameOverLaugh, kAlarmPriority);	ProcessSounds();		HIG_PositionDialog('DLOG', 128);	gameOverDlg = GetNewDialog(128, nil, (WindowPtr)-1);	ModalDialog((ModalFilterUPP)myDlogFilter, &itemHit);	DisposDialog(gameOverDlg);	}*//************************************************************ RemoveGemFromPlayField	Gem timer has either run out or the player reached	the gem in time. Either way hide it away.   ***********************************************************void	RemoveGemFromPlayField(void){	gBonusSprite->Hide();}*//************************************************************ ShutdownSound	Quitting, so shut down the sound system   ************************************************************/void	ShutdownSound(void){	delete(gSchneeSndFX);	gSchneeSndFX = nil;}/************************************************************ StartUpSound	Fire up the sound section   ************************************************************/Boolean	StartUpSound(void){	gSchneeSndFX = new CSoundFX;	if(gSchneeSndFX)		return TRUE;	else		return FALSE;}/************************************************************ Apple Events	************************************************************/static void AppleEventInit(){	OSErr				error;		error = AEInstallEventHandler(kCoreEventClass, kAEOpenApplication, &DoOpenApp, 0, false);	error = AEInstallEventHandler(kCoreEventClass, kAEOpenDocuments, &DoOpenDoc, 0, false);	error = AEInstallEventHandler(kCoreEventClass, kAEPrintDocuments, &DoPrintDoc, 0, false);	error = AEInstallEventHandler(kCoreEventClass, kAEQuitApplication, &DoQuitApp, 0, false);}static pascal OSErr DoOpenApp(const AppleEvent *theAppleEvent, AppleEvent *reply, long refCon){/*What am I supposed to do here?*/	return MyGotRequiredParams(theAppleEvent);}static pascal OSErr DoOpenDoc(const AppleEvent *theAppleEvent, AppleEvent *reply, long refCon){	OSErr		err;	AEDescList	fileSpecList;	short		i;	long		count;	Size		actual;	FSSpec		desc;	AEKeyword	keyword;	DescType	type;	err = AEGetParamDesc(theAppleEvent, keyDirectObject, typeAEList, &fileSpecList);		err = AECountItems(&fileSpecList, &count);	for (i = 1; i <= count; i++)	{		err = AEGetNthPtr(&fileSpecList, i, typeFSS, &keyword, &type, (Ptr)&desc, sizeof(FSSpec), &actual);		if (err == noErr)		{/* Copy the file desciption into lastReply so Open can get it from there. */			gLastReply.sfFile = desc;			gLastReply.sfGood = true;			gCurrentGame.LoadGame(false);/* Since we only allow one file at a time, let's exit DoOpenDoc once we have one. */			return MyGotRequiredParams(theAppleEvent);		}	}	return MyGotRequiredParams(theAppleEvent);}static pascal OSErr DoPrintDoc(const AppleEvent *theAppleEvent, AppleEvent *reply, long refCon){	return errAEEventNotHandled;}static pascal OSErr DoQuitApp(const AppleEvent *theAppleEvent, AppleEvent *reply, long refCon){	gAppIsRunning = false;			/*If I'm told to quit, I'll quit.*/	return MyGotRequiredParams(theAppleEvent);}static OSErr MyGotRequiredParams(const AppleEvent *theAppleEvent){	DescType returnedType;	Size actualSize;	if ( AEGetAttributePtr(theAppleEvent, keyMissedKeywordAttr, typeWildCard, &returnedType, nil, 0, &actualSize) == errAEDescNotFound )		return noErr;	else		return errAEParamMissed;}