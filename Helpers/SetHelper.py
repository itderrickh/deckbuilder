def getSet(sets, setCode):
	return next(s.shortName for s in sets if s.setName == setCode)

def getSetCode(sets, setName):
	return next((s.setName for s in sets if s.shortName == setName), "")