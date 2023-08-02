import os
import clr
import csv
import itertools

clr.AddReference("Autodesk.Navisworks.Timeliner")
from Autodesk.Navisworks.Api.Timeliner import TimelinerTask, TimelinerSelection
from datetime import datetime


timeline = doc.Timeliner
timeline.TasksClear()

ffp = os.path.join(os.getcwd(), 'FinalSchedule.csv')
DATEFIELDS = ['Planned Start', 'Planned End', 'Actual Start', 'Actual End']
DATEATTRS= ['PlannedStartDate', 'PlannedEndDate', 'ActualStartDate', 'ActualEndDate']
def read_tasks(ffp):
    tasks = []
    from_format = "%d/%m/%Y"
    from_format_hours = "%d/%m/%Y/%H"
    with open(ffp) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            row['Task Nesting'] = str(row['Task Nesting'])
            row['Name'] = row['Name'].strip()
            row['Display ID'] = row['Display ID'].strip()

            for field in DATEFIELDS:
                try:
                    row[field] = datetime.strptime(row[field], from_format)
                except:
                    try:
                        row[field] = datetime.strptime(row[field], from_format_hours)
                    except:
                        continue

            # if row['Planned Start']:
            #     row['Planned Start'] = datetime.strptime(row['Planned Start'], from_format)
            # if row['Planned End']:
            #     row['Planned End'] = datetime.strptime(row['Planned End'], from_format)
            # if row['Actual Start']:
            #     row['Actual Start'] = datetime.strptime(row['Actual Start'], from_format)
            # if row['Actual End']:
            #     row['Actual End'] = datetime.strptime(row['Actual End'], from_format)
            row['Task Type'] = row['Task Type'].strip()


            tasks.append(row)

            #print(row['Planned Start'])
            #print(row['ActivityId'])


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
    indent = row['Task Nesting']
    task.DisplayId = row['Display ID']
    task.DisplayName = row['Name']

    for field,fattr in zip(DATEFIELDS, DATEATTRS):
        try:
        #if row[field]:
            setattr(task, fattr, row[field])
        except:
            continue
    # if row['Planned Start']:
    #     task.PlannedStartDate = row['Planned Start']
    # if row['Planned End']:
    #     task.PlannedEndDate = row['Planned End']
    # if row['Actual Start']:
    #     task.ActualStartDate = row['Actual Start']
    # if row['Actual End']:
    #     task.ActualEndDate = row['Actual End']
    task.SimulationTaskTypeName = row['Task Type']
    task.User1 = row['User 1']
    task.User2 = row['User 2']
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
        curr = int(row['Task Nesting'])
        task = create_task(row)
        parent, prev = filter_indent_lvl(parent, task, curr, prev)
        create_timeline(parent, task)

counter = itertools.count()
tasks = read_tasks(ffp)


parse_csv(tasks)






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
    # get task state
    #print(task.User2)
    if task.User2:
        if task.ActualEndDate:
            seen.Add(map_modelitems[task.User2])
        elif task.ActualStartDate:
            inwork.Add(map_modelitems[task.User2])
        else:
            hidden.Add(map_modelitems[task.User2])
    return


seen = ModelItemCollection()
hidden = ModelItemCollection()
inwork = ModelItemCollection()
map_modelitems = map_mitems_func()
print('so far so good')

recursive_parse(timeline.TasksRoot)

doc.Models.SetHidden(hidden, False)
doc.Models.OverridePermanentColor(seen, Color(0.2549, 0.4118, 0.8824))
doc.Models.OverridePermanentColor(hidden, Color(0.8275, 0.8275, 0.8275))
doc.Models.OverridePermanentTransparency(hidden, 0.5)
doc.Models.OverridePermanentTransparency(seen, 0.5)
doc.Models.OverridePermanentColor(inwork, Color(0.7059, 0.8627, 0.6667))
doc.Models.OverridePermanentTransparency(inwork, 0.1)

