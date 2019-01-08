def getSet(sets, setCode):
	return next(s.name for s in sets if s.setName == setCode)

def getSetCode(sets, setName):
	return next((s.setName for s in sets if s.name == setName), "")