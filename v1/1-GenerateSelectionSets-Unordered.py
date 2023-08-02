

doc.SelectionSets.Clear()

mapping = {1: '99', 2: '34', 3: '33', 4: '98', 5: '35', 6: '32', 7: '97', 8: '36', 9: '31', 10: '96', 11: '37', 12: '30', 13: '95', 14: '38', 15: '29', 16: '94', 17: '39', 18: '28', 19: '93', 20: '40', 21: '27', 22: '92', 23: '41', 24: '26', 25: '91', 26: '42', 27: '25', 28: '8', 29: '59', 30: '74', 31: '1', 32: '66', 33: '67', 34: '2', 35: '65', 36: '68', 37: '3', 38: '64', 39: '69', 40: '4', 41: '63', 42: '70', 43: '5', 44: '62', 45: '71', 46: '6', 47: '61', 48: '72', 49: '7', 50: '60', 51: '73', 52: '90', 53: '43', 54: '24', 55: '89', 56: '44', 57: '23', 58: '88', 59: '45', 60: '22', 61: '87', 62: '46', 63: '21', 64: '86', 65: '47', 66: '20', 67: '85', 68: '48', 69: '19', 70: '84', 71: '49', 72: '18', 73: '83', 74: '50', 75: '17', 76: '82', 77: '51', 78: '16', 79: '81', 80: '52', 81: '15', 82: '80', 83: '53', 84: '14', 85: '79', 86: '54', 87: '13', 88: '78', 89: '55', 90: '12', 91: '77', 92: '56', 93: '11', 94: '76', 95: '57', 96: '10', 97: '75', 98: '58', 99: '9'}
references = {}
def save_references(_d):
	import os
	import json
	with open (os.path.join(os.getcwd(), 'references.json'), 'w') as f:
		json.dump(_d,f)
		

root = doc.Models[0].RootItem

container = {}
for c in root.Children:
	#Create a dictionary with
	# {key: value} = {Root.DisplayName: [ModelItems of Root Children]}
	container[c.DisplayName] = [modelItem for modelItem in c.Children]


		
references = {} #Stores the key:val pairs where key = Selection.Id and val is Model.Id
x= 0
for item in container.keys():
	for i,child in enumerate(container[item]):
		col = ModelItemCollection()
		col.Add(child)
		newsel = SelectionSet(col)
		if item in ['00 PILES', '00 METAL FORMWORK', '00 IN SITU CONCRETE - PILES', '00 IN SITU CONCRETE - BEAMS']:
			name_convention = item + '-' + mapping[i+1]
			newsel.DisplayName = name_convention
			references[name_convention] = child.InstanceGuid.ToString()
		elif item in ['10.10 P3 - EXISTING SOUTH GROYNE - CUT', '11.10 P3 - NORTH GROYNE QR', '11.20 P3 - NORTH GROYNE AR', '13.00 P3 - BEACH QUALITY SAND']:
			newsel.DisplayName = item
			references[item] = child.InstanceGuid.ToString()
		elif item in ['12.00 P3 - BEACH RECLAMATION - FILL']:
			name_convention = item + '-' + chr(65+x)
			x+=1
			newsel.DisplayName = name_convention
			references[name_convention] = child.InstanceGuid.ToString()
			
		
		else:
			name_convention = item + '-' + str(i+1)
			newsel.DisplayName = name_convention
			references[name_convention] = child.InstanceGuid.ToString()
		#print(item + str(i+1), child.InstanceGuid.ToString())
		
		doc.SelectionSets.InsertCopy(0, newsel)
save_references(references)

