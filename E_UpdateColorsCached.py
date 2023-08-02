#WILL ONLY UPDATE THE COLORS BUT NOT THE TIMELINER
#SINCE TIMELINER.TASKs ARE READ ONLY PROPERTY
#IT IS A FAST WAY TO UPDATE THE SEEN/WORKING/HIDDEN COLORS

HIDDEN = ['651e2f2f-8619-5ea7-a731-7583b6c05827',
'8f29c750-49c9-54eb-9208-e6d944224900',
'62f9029e-ea59-5e2a-87dc-4949ed7a5f52',
'807c0e93-3d7a-512b-9e91-ce6cb0ed97af',
'07e7279b-0296-5e76-b5d6-68f45817936e']



import os
import clr
import csv
import itertools


clr.AddReference("Autodesk.Navisworks.Timeliner")
from Autodesk.Navisworks.Api.Timeliner import TimelinerTask, TimelinerSelection
from datetime import datetime



ffp = os.path.join(os.getcwd(), 'FinalSchedule.csv')
DATEFIELDS = ['Planned Start', 'Planned End', 'Actual Start', 'Actual End']
DATEATTRS= ['PlannedStartDate', 'PlannedEndDate', 'ActualStartDate', 'ActualEndDate']

def read_tasks(ffp):
    tasks = []
    from_format = "%d/%m/%Y"

    with open(ffp) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        my_dict = {}
        for row in reader:
            row['Task Nesting'] = str(row['Task Nesting'])
            row['Name'] = row['Name'].strip()
            row['Display ID'] = row['Display ID'].strip()

            for field in DATEFIELDS:
                try:
                    row[field] = datetime.strptime(row[field], from_format)
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

            my_dict[row['User 2']] = row
            #tasks.append(row)

            #print(row['Planned Start'])
            #print(row['ActivityId'])


    return my_dict







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
    """
    Checks if the actual date and start exist in the csv file
    If it does, it also changes the timeline.task & adds to the working/seen/hidden list as mitems
    """
    taskref = timeline_csv[task.User2] #Returns the dictionary of tasks from teh csv file based on the reference id
    if task.User2:
        if taskref['Actual End']:
            #task.ActualEndDate = taskref['Actual End']
            seen.Add(map_modelitems[task.User2])
        elif timeline_csv[task.User2]['Actual Start']:
            #task.ActualStartDate = taskref['Actual Start']
            inwork.Add(map_modelitems[task.User2])
        else:
            hidden.Add(map_modelitems[task.User2])

    if task.User2 in HIDDEN:
        notshown.Add(map_modelitems[task.User2])
    return


seen = ModelItemCollection()
hidden = ModelItemCollection()
inwork = ModelItemCollection()
notshown = ModelItemCollection()
map_modelitems = map_mitems_func()
timeline_csv = read_tasks(ffp)
timeline = doc.Timeliner

recursive_parse(timeline.TasksRoot)

doc.Models.SetHidden(notshown, True)
doc.Models.OverridePermanentColor(seen, Color(0.2549, 0.4118, 0.8824))
doc.Models.OverridePermanentColor(hidden, Color(0.8275, 0.8275, 0.8275))
doc.Models.OverridePermanentTransparency(hidden, 0.5)
doc.Models.OverridePermanentTransparency(seen, 0.5)
doc.Models.OverridePermanentColor(inwork, Color(0.7059, 0.8627, 0.6667))
doc.Models.OverridePermanentTransparency(inwork, 0.1)
