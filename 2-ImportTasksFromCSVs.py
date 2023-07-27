import os
import clr
import csv
import glob
clr.AddReference("Autodesk.Navisworks.Timeliner")
from Autodesk.Navisworks.Api.Timeliner import TimelinerTask, TimelinerSelection
from datetime import datetime



#get csv file of activities
timeline = doc.Timeliner

#ffp = glob.glob(os.getcwd() + '/*.csv')[0]
ffp = 'D:/01_Projects/40.Hudayriat PDA/Schedule_rev2.csv'

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
	curr = indent
	
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
		
	#EEEEEEEEEEEEE
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
		
	prev = curr


#timeline.TasksRoot.Children[0].Children[idx] #parent
#parent.Children[0] #child
#child.Children[childid] #child_son =
#timeline.TasksRoot.Children[0].Children[idx].Children[0].Children[childid]

def create_task():


def recurse_parse(indent, parent, child = None):

	pass


