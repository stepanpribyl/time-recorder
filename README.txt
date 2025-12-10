tlačítka projektů + SHARED=SPECIAL (rozdělen úěrným dílem mezi zbývající projekty)
tlačítka další:
	STOP/BREAK - ends current activity, waits for choosing a new one
	RESUME SESSION (load session json)
	PROCESS - counts lengths of blocks, creates a summary, creates a picture result
	
	
Session:
	Datetime start
	TimeBlocks
		list of dicts:	tstart, tend, project, description
	Results
		project: length
		
	
Projects:
	project ID: 
		name
		color hexa