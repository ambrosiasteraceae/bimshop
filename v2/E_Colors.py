timeline = doc.Timeliner


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
    print(task.User2)
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