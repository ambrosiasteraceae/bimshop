import clr
clr.AddReference("Autodesk.Navisworks.Timeliner")
from Autodesk.Navisworks.Api.Timeliner import TimelinerTask, TimelinerSelection
mapping = {
'HPDA.CON.CP.10040':['00 BEAMS PC1','00 BEAMS PC2'],
'HPDA.CON.CP.10050':['00 IN SITU CONCRETE - BEAMS', '00 IN SITU CONCRETE - PILES'],
'HPDA.CON.CP.10090':'00 IN SITU CONCRETE - SLAB',
'HPDA.CON.CP.10020':'00 METAL FORMWORK',
'HPDA.CON.CP.10010':'00 PILES',
'HPDA.CON.CP.10080':['00 SLABS - SL1', '00 SLABS - SL2', '00 SLABS - SL3', '00 SLABS - SL4A', '00 SLABS - SL4B', '00 SLABS - SL5A', '00 SLABS - SL5B', '00 SLABS - SL6A', '00 SLABS - SL6B', '00 SLABS - SL7A', '00 SLABS - SL7B', '00 SLABS - SL8A', '00 SLABS - SL8B'],
'HPDA.CON..DM.10000':'10.10 P3 - EXISTING SOUTH GROYNE - CUT',
'HPDA.CON.NG.10020':'11.10 P3 - NORTH GROYNE QR',
'HPDA.CON.NG.10040':'11.20 P3 - NORTH GROYNE AR',
'HPDA.CON.BW.NS.BP.10000':'12.00 P3 - BEACH RECLAMATION - FILL',
'HPDA.CON.BW.NS.BS.10000':'13.00 P3 - BEACH QUALITY SAND'}

def load_references():
	import os
	import json
	with open(os.path.join(os.getcwd(), 'references.json')) as f:
		return json.load(f)

references = load_references()
print(references)
timeline = doc.Timeliner

def create_task(s):
	task = TimelinerTask()
	task.DisplayName = s.DisplayName
	print(s.DisplayName)
	task.DisplayId = references[s.DisplayName]
	task.SimulationTaskTypeName = 'Construct' 
	task.User1 = 'hidden'
	return task
sets = doc.SelectionSets.Value



def process_task(t):
	if t.DisplayName in mapping.keys():
		val = mapping[t.DisplayName]
		print(val)
		for s in sets:
			if isinstance(val, list):
				for v in val:
					if v in s.DisplayName:
						task = create_task(s)
						timeline.TaskAddCopy(t,task)
			else:
				if val in s.DisplayName:
					task = create_task(s)
					timeline.TaskAddCopy(t,task)


def recursive_parse(path):
	for t in path.Children:
		if t.Children:
			recursive_parse(t)
		else:
			process_task(t)
			

						
				
				

recursive_parse(timeline.TasksRoot)
