import os
import clr
import csv
import itertools

clr.AddReference("Autodesk.Navisworks.Timeliner")
from Autodesk.Navisworks.Api.Timeliner import TimelinerTask, TimelinerSelection
from datetime import datetime


ffp = os.path.join(os.getcwd(), 'InitialSchedule.csv')


def read_tasks(ffp):
    tasks = []
    from_format = "%d-%b-%y"
    to_format = "%d/%m/%y"
    with open(ffp) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            row['Indent'] = str(row['Indent'])
            row['ActivityId'] = row['ActivityId'].strip()
            row['ActivityName'] = row['ActivityName'].strip()
            row['Start'] = datetime.strptime(row['Start'], from_format)
            row['Finish'] = datetime.strptime(row['Finish'], from_format)
            tasks.append(row)
            print(row['ActivityId'])

    return tasks

def get_last_task(root):
    """
    Parses with recursion to the last item in the root tree
    """
    child = list(root.Children)[-1]
    #print('Child is', child.DisplayName)
    if child.Children:
        return get_last_task(child)
    return child


def create_task(row):
    task = TimelinerTask()
    indent = row['Indent']
    task.DisplayId = row['ActivityName']
    task.DisplayName = row['ActivityId']
    task.PlannedStartDate = row['Start']
    task.PlannedEndDate = row['Finish']
    #task.User2 = row['Indent']
    return task


def filter_indent_lvl(parent, task, curr, prev=0):
    """
	parent - parent task
	curr - current indent level
	prev - previous indent level
	"""
    if curr == prev:
        pass
    elif curr > prev:
        child = get_last_task(timeline.TasksRoot)
        parent.append(child)
    else:
        diff = prev - curr
        index = len(parent) - diff
        parent = parent[:index]
    prev = curr
    return parent, prev


def create_timeline(parent, task):
    if parent:
		#pparent = get_last_task(MASTER)
        timeline.TaskAddCopy(parent[-1], task)
        return
    global counter
    timeline.TaskInsertCopy(next(counter), task)


def parse_csv(tasks):
    parent = []
    prev = 0
    counter = itertools.count()
    for row in tasks:
        curr = int(row['Indent'])
        task = create_task(row)
        parent, prev = filter_indent_lvl(parent, task, curr, prev)
        create_timeline(parent, task)

timeline = doc.Timeliner
counter = itertools.count()
tasks = read_tasks(ffp)
timeline.TasksClear()
parse_csv(tasks)










