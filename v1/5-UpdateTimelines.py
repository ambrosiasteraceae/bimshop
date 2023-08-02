
timeline = doc.Timeliner


def current_task_state():
	"""
	Reads the updated schedule and returns a dictionary with
				referenceid: hiddenstate pairs
	"""
	import csv
	import os
	task_state = {}
	with open(os.path.join(os.getcwd(), 'UpdatedSchedule.csv')) as csvfile:
		reader = csv.DictReader(csvfile, delimiter = ',')
		for row in reader:
			if row['DisplayId']:
				task_state[row['DisplayId']] = row['User1']
	return task_state
	
task_state = current_task_state()

def generate_parent_tasks():
    import os
    import clr
    import csv
    import glob
    clr.AddReference("Autodesk.Navisworks.Timeliner")
    from Autodesk.Navisworks.Api.Timeliner import TimelinerTask, TimelinerSelection
    from datetime import datetime



    ffp = glob.glob(os.getcwd() + '/*.csv')[0]


    def read_tasks(ffp):
        tasks = []
        from_format = "%d-%b-%y"
        to_format = "%d/%m/%y"
        with open(ffp) as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            for row in reader:
                row['Indent'] = int(row['Indent'])
                row['ActivityId'] = row['ActivityId'].strip()
                row['ActivityName'] = row['ActivityName'].strip()
                row['Start'] = datetime.strptime(row['Start'], from_format)
                row['Finish'] =datetime.strptime(row['Finish'], from_format)
                tasks.append(row)
                #date = datetime.strptime(row[4], from_format)
                #print(datetime.strftime(date, to_format))
                #activities.append(row[0].strip())
        return tasks

    tasks = read_tasks(ffp)
    gen = (t for t in tasks)
    curr = None
    prev = None
    indent = 0
    idx = 0
    timeline.TasksClear()
    for i,row in enumerate(tasks):

        task = TimelinerTask()
        indent = row['Indent']
        task.DisplayId = row['ActivityName']
        task.DisplayName = row['ActivityId']
        task.PlannedStartDate = row['Start']
        task.PlannedEndDate = row['Finish']
        
        if indent == 0:
            timeline.TaskInsertCopy(idx, task)
            grand_parent = timeline.TasksRoot.Children[idx]
            print(grand_parent.DisplayName)
            continue
        
        if indent == 1:
            #idx = 0
            timeline.TaskAddCopy(grand_parent, task)
            parent = timeline.TasksRoot.Children[0].Children[idx]
            idx+=1
            
            
        if indent == 2:
            timeline.TaskAddCopy(parent, task)
            child = parent.Children[0]
            childid=0
            
        if indent ==3:
            timeline.TaskAddCopy(child,task)
            child_son = child.Children[childid]
            childid+=1
        
        if indent==4:
            timeline.TaskAddCopy(child_son, task)
 
def generate_tasks():
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


	def create_task(s):
		task = TimelinerTask()
		task.DisplayName = s.DisplayName
		print(s.DisplayName)
		task.DisplayId = references[s.DisplayName]
		task.SimulationTaskTypeName = 'Construct' 
		task.User1 = task_state[references[s.DisplayName]]
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
	
generate_parent_tasks()
import time
time.sleep(2)
generate_tasks()



def unhide():
	elem = doc.Models[0].RootItem
	collector = ModelItemCollection()
	for parent in elem.Children:
		for child in parent.Children:
			collector.Add(child)
	doc.Models.SetHidden(collector,False)


def map_mitems_func():
	map_modelitems = {}
	mitems = doc.Models[0].RootItem.Children
	for modelItem in mitems:
		for child in modelItem.Children:
			map_modelitems[child.InstanceGuid.ToString()] = child
	return map_modelitems

def recursive_parse(path):
	for t in path.Children:
		if t.Children:
			recursive_parse(t)
		else:
			check_task(t)

def check_task(task):
        #get task state
        if task.User1:
	        state = task_state[task.DisplayId]
	        print(state)
	        if state == "hidden":
	            hidden.Add(map_modelitems[task.DisplayId])
	        return
        return

timeline = doc.Timeliner
unhide()

map_modelitems = map_mitems_func()
hidden = ModelItemCollection()
recursive_parse(timeline.TasksRoot)

doc.Models.SetHidden(hidden,True)


	
