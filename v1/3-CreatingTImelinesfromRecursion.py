import clr
clr.AddReference("Autodesk.Navisworks.Timeliner")
from Autodesk.Navisworks.Api.Timeliner import TimelinerTask, TimelinerSelection

#@TODO ITERATE OVER A SEQUENCE OF SETS THAT DECREASES OR IS REMOVED ONCE IT IS READ
chainages = {
    '12.00 P3 - BEACH RECLAMATION - FILL':
        {
            1: 'FILL CH:+000 to +300', 2: 'FILL CH:+300 to +500', 3: 'FILL CH:+500 to +700', 4: 'FILL CH:+900 to +1100', 5: 'FILL CH:+700 to +900', 6: 'FILL CH:+1100 to +1300', 7: 'FILL CH:+1300 to +1500', 8: 'FILL CH:+1500 to +1700', 9: 'FILL CH:+1700 to +1900', 10: 'FILL CH:+1900 to +2100', 11: 'FILL CH:+2100 to +2300', 12: 'FILL CH:+2300 to +2400'
        },
    'BEACH SAND': {
        1: 'SAND CH:+000 to +300', 2: 'SAND CH:+300 to +500', 3: 'SAND CH:+500 to +700', 4: 'SAND CH:+900 to +1100', 5: 'SAND CH:+700 to +900', 6: 'SAND CH:+1100 to +1300', 7: 'SAND CH:+1300 to +1500', 8: 'SAND CH:+1500 to +1700', 9: 'SAND CH:+1700 to +1900', 10: 'SAND CH:+1900 to +2100', 11: 'SAND CH:+2100 to +2300', 12: 'SAND CH:+2300 to +2400',},

    '11.20 P3 - NORTH GROYNE AR': {1: 'AR CH: +000 to +020', 2: 'AR CH: +020 to +040',
                                   3: 'AR CH: +040 to +060', 4: 'AR CH: +060 to +080', 5: 'AR CH: +080 to +100',
                                   6: 'AR CH: +100 to +120', 7: 'AR CH: +120 to +140',8: 'AR CH: +140 to +150'},
    '11.10 P3 - NORTH GROYNE QR': {1: 'QR CH: +000 to +020', 2: 'QR CH: +020 to +040',
                                   3: 'QR CH: +040 to +060', 4: 'QR CH: +060 to +080', 5: 'QR CH: +080 to +100',
                                   6: 'QR CH: +100 to +120', 7: 'QR CH: +120 to +140', 8: 'QR CH: +140 to +150'},
    '00 IN SITU CONCRETE - SLAB': { 1: '0-33%', 2 : '33%-67%', 3: '67%-100%'}
}


def invert_vals(ch):
    _chainages = {}
    for key in ch:
        _chainages[key] = list(ch[key].values())
    return _chainages

tchainages = invert_vals(chainages)

bs_iter = iter(tchainages['BEACH SAND'])
fill_iter = iter(tchainages['12.00 P3 - BEACH RECLAMATION - FILL'])
mapping = {
'HPDA.CON..DM.10000' : '10.10 P3 - EXISTING SOUTH GROYNE - CUT',
'HPDA.CON.NG.10020': tchainages['11.10 P3 - NORTH GROYNE QR'],
'HPDA.CON.NG.10040': tchainages['11.20 P3 - NORTH GROYNE AR'],
'HPDA.CON.BW.NS.BP.10010': next(fill_iter),
'HPDA.CON.BW.NS.BP.10020': next(fill_iter),
'HPDA.CON.BW.NS.BP.10030': next(fill_iter),
'HPDA.CON.BW.NS.BP.10040': next(fill_iter),
'HPDA.CON.BW.NS.BP.10050': next(fill_iter),
'HPDA.CON.BW.NS.BP.10060': next(fill_iter),
'HPDA.CON.BW.NS.BP.10070': next(fill_iter),
'HPDA.CON.BW.NS.BP.10080': next(fill_iter),
'HPDA.CON.BW.NS.BP.10090': next(fill_iter),
'HPDA.CON.BW.NS.BP.10100': next(fill_iter),
'HPDA.CON.BW.NS.BP.10110': next(fill_iter),
'HPDA.CON.BW.NS.BP.10120': next(fill_iter),
'HPDA.CON.BW.NS.BS.10010': next(bs_iter),
'HPDA.CON.BW.NS.BS.10020': next(bs_iter),
'HPDA.CON.BW.NS.BS.10030': next(bs_iter),
'HPDA.CON.BW.NS.BS.10040': next(bs_iter),
'HPDA.CON.BW.NS.BS.10050': next(bs_iter),
'HPDA.CON.BW.NS.BS.10060': next(bs_iter),
'HPDA.CON.BW.NS.BS.10070': next(bs_iter),
'HPDA.CON.BW.NS.BS.10080': next(bs_iter),
'HPDA.CON.BW.NS.BS.10090': next(bs_iter),
'HPDA.CON.BW.NS.BS.10100': next(bs_iter),
'HPDA.CON.BW.NS.BS.10110': next(bs_iter),
'HPDA.CON.BW.NS.BS.10120': next(bs_iter),
'HPDA.CON.CP.10010': 'PILE',
'HPDA.CON.CP.10040': 'PC',
'HPDA.CON.CP.10020': 'FORMWORK',
'HPDA.CON.CP.10050': 'PLUG',
'HPDA.CON.CP.10080': ['SL1', 'SL2', 'SL3', 'SL4A', 'SL4B', 'SL5A', 'SL5B', 'SL6A', 'SL6B', 'SL7A', 'SL7B', 'SL8A', 'SL8B'],
'HPDA.CON.CP.10090': ['33%-67%', '67%-100%', '0-33%']
}








def load_references():
	import os
	import json
	with open(os.path.join(os.getcwd(), 'references.json')) as f:
		return json.load(f)

references = load_references()

timeline = doc.Timeliner

def create_task(s):
	task = TimelinerTask()
	task.DisplayName = s.DisplayName
	print(s.DisplayName)
	task.DisplayId = references[s.DisplayName] #instance guid
	task.SimulationTaskTypeName = 'Construct' 
	task.User1 = 'hidden'
	return task

sets = doc.SelectionSets.Value



def process_task(t):
	if t.DisplayName in mapping.keys():
		val = mapping[t.DisplayName]
		#
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
