/****************************************************************************** CMove.h   ******************************************************************************/#pragma onceclass CStep{	char	fHorz;	char	fVert;	public:	char	GetHorz() { return fHorz; }	char	GetVert() { return fVert; }	void	SetStep(short horz, short vert)	{		fHorz = horz;		fVert = vert;	}};class CMove {	short	fIndex;	short	fLength;		CStep *	fSteps;	public:				CMove(short horz = 0, short vert = 0);		virtual	~CMove();		void		SetMove(short horz, short vert);	CStep		Move();};