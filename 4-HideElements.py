
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
task_state = current_task_state()
map_modelitems = map_mitems_func()
hidden = ModelItemCollection()
recursive_parse(timeline.TasksRoot)

doc.Models.SetHidden(hidden,True)


	
