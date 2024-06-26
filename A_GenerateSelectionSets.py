import os
import json

import math


class Point:
    def __init__(self, x, y, index=None, name=None):
        self.x = x
        self.y = y
        self.index = index
        self.newindex = None
        self.name = name

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)



class PointCluster:
    def __init__(self, points_list):
        self.points_list = points_list

    def __getitem__(self, s):
        return self.points_list[s]

    @property
    def x(self):
        return [point.x for point in self.points_list]

    @property
    def y(self):
        return [point.y for point in self.points_list]

    @property
    def index(self):
        return [point.index for point in self.points_list]

    def distance(self, other):
        return [point.distance(other) for point in self.points_list]

    def sort_by_distance(self, other):
        self.points_list = sorted(self.points_list, key=lambda point: point.distance(other), reverse=True)
        for i, point in enumerate(self.points_list):
            point.newindex = i +1
            self.newindex = [point.newindex for point in self.points_list]
        return self.points_list

    def to_dict(self):
        """
        Returns a dict that has:
        {oldindex: newindex}
        by old index, it is the first order index (order of appearence)
        by new index, it is the ordered index by distance to the reference point
        """
        return {point.index: point.newindex for point in self.points_list}

def save_references(_d):
    with open(os.path.join(os.getcwd(), 'references.json'), 'w') as f:
        json.dump(_d, f)


ordered_set = {
    '00 SLABS - SL1': {
        1: '66', 2: '65', 3: '64', 4: '69', 5: '68', 6: '67', 7: '72', 8: '71', 9: '70', 10: '75', 11: '74', 12: '73',
        13: '78', 14: '77', 15: '76', 16: '81', 17: '80', 18: '79', 19: '84', 20: '83', 21: '82', 22: '19', 23: '20',
        24: '21', 25: '22', 26: '23', 27: '24', 28: '25', 29: '26', 30: '27', 31: '28', 32: '29', 33: '30', 34: '31',
        35: '32', 36: '33', 37: '34', 38: '35', 39: '36', 40: '37', 41: '38', 42: '39', 43: '40', 44: '41', 45: '42',
        46: '43', 47: '44', 48: '45', 49: '46', 50: '47', 51: '48', 52: '49', 53: '50', 54: '51', 55: '52', 56: '53',
        57: '54', 58: '55', 59: '56', 60: '57', 61: '58', 62: '59', 63: '60', 64: '61', 65: '62', 66: '63', 67: '3',
        68: '1', 69: '2', 70: '6', 71: '4', 72: '5', 73: '9', 74: '7', 75: '8', 76: '12', 77: '10', 78: '11', 79: '15',
        80: '13', 81: '14', 82: '18', 83: '16', 84: '17',
    },

    '00 SLABS - SL2': {
        1: '22', 2: '23', 3: '24', 4: '25', 5: '26', 6: '27', 7: '28', 8: '7', 9: '8', 10: '9', 11: '10', 12: '11',
        13: '12', 14: '13', 15: '14', 16: '15', 17: '16', 18: '17', 19: '18', 20: '19', 21: '20', 22: '21', 23: '1',
        24: '2', 25: '3', 26: '4', 27: '5', 28: '6'
    },
    '00 SLABS - SL3': {
        1: '22', 2: '23', 3: '24', 4: '25', 5: '26', 6: '27', 7: '28', 8: '7', 9: '8', 10: '9', 11: '10', 12: '11',
        13: '12', 14: '13', 15: '14', 16: '15', 17: '16', 18: '17', 19: '18', 20: '19', 21: '20', 22: '21', 23: '1',
        24: '2', 25: '3', 26: '4', 27: '5', 28: '6'
    },
    '00 SLABS - SL4A': {1: '1', 2: '2'},
    '00 SLABS - SL4B': {1: '2', 2: '1'},
    '00 SLABS - SL5A': {1: '1', 2: '2'},
    '00 SLABS - SL5B': {1: '2', 2: '1'},
    '00 SLABS - SL6A': {1: '1', 2: '2'},
    '00 SLABS - SL6B': {1: '2', 2: '1'},
    '00 SLABS - SL7A': {1: '1', 2: '2'},
    '00 SLABS - SL7B': {1: '2', 2: '1'},
    '00 SLABS - SL8A': {1: '1', 2: '2'},
    '00 SLABS - SL8B': {1: '2', 2: '1'},
    '00 BEAMS PC1': {1: '31', 2: '30', 3: '29', 4: '28', 5: '27', 6: '26', 7: '25', 8: '24', 9: '1', 10: '2', 11: '3', 12: '4',
            13: '5', 14: '6', 15: '7', 16: '23', 17: '22', 18: '21', 19: '20', 20: '19', 21: '18', 22: '17', 23: '16',
            24: '15', 25: '14', 26: '13', 27: '12', 28: '11', 29: '10', 30: '9', 31: '8'},
    '00 BEAMS PC2': {1: '2', 2: '1'}}

# Map the name name of the model item ot the desired selection set
name_map = {'00 SLABS - SL1': 'SL1', '00 SLABS - SL2': 'SL2', '00 SLABS - SL3': 'SL3', '00 SLABS - SL4A': 'SL4A',
            '00 SLABS - SL4B': 'SL4B', '00 SLABS - SL5A': 'SL5A', '00 SLABS - SL5B': 'SL5B', '00 SLABS - SL6A': 'SL6A',
            '00 SLABS - SL6B': 'SL6B', '00 SLABS - SL7A': 'SL7A', '00 SLABS - SL7B': 'SL7B', '00 SLABS - SL8A': 'SL8A',
            '00 SLABS - SL8B': 'SL8B', '00 BEAMS PC1': 'PC1', '00 BEAMS PC2': 'PC2', '00 PILES': 'PILE',
            '00 METAL FORMWORK': 'FORMWORK','00 IN SITU CONCRETE - PILES': 'PLUG'}
chainages = {
    '12.00 P3 - BEACH RECLAMATION - FILL': {1: 'CH:+2300 to +2400', 2: 'CH:+2100 to +2300', 3: 'CH:+1900 to +2100',
                                            4: 'CH:+1700 to +1900', 5: 'CH:+1500 to +1700', 6: 'CH:+1300 to +1500',
                                            7: 'CH:+1100 to +1300', 8: 'CH:+900 to +1100', 9: 'CH:+700 to +900',
                                            10: 'CH:+500 to +700', 11: 'CH:+300 to +500', 12: 'CH:+000 to +300', },
    'BEACH SAND': {1: 'CH:+2300 to +2400', 2: 'CH:+2100 to +2300', 3: 'CH:+1900 to +2100', 4: 'CH:+1700 to +1900',
                   5: 'CH:+1500 to +1700', 6: 'CH:+1300 to +1500', 7: 'CH:+1100 to +1300', 9: 'CH:+700 to +900',
                   8: 'CH:+900 to +1100', 10: 'CH:+500 to +700', 11: 'CH:+300 to +500', 12: 'CH:+000 to +300', },
    '11.20 P3 - NORTH GROYNE AR': {
                                   1: 'CH: +000 to +020',
                                   2: 'CH: +020 to +040',
                                   3: 'CH: +040 to +060',
                                   4: 'CH: +060 to +080',
                                   5: 'CH: +080 to +100',
                                   6: 'CH: +100 to +120',
                                   8: 'CH: +120 to +140',
                                   7: 'CH: +140 to +150',
                                   },
    '11.10 P3 - NORTH GROYNE QR': {
                                   2: 'CH: +000 to +020',
                                   1: 'CH: +020 to +040',
                                   3: 'CH: +040 to +060',
                                   6: 'CH: +060 to +080',
                                   5: 'CH: +080 to +100',
                                   4: 'CH: +100 to +120',
                                   8: 'CH: +120 to +140',
                                   7: 'CH: +140 to +150',
                                   },
    '00 IN SITU CONCRETE - SLAB': {1 : '33%-67%', 2 : '67%-100%', 3 : '0-33%'}
}




doc.SelectionSets.Clear()



root = doc.Models[0].RootItem

container = {}
for c in root.Children:
    # Create a dictionary with
    # {key: value} = {Root.DisplayName: [ModelItems of Root Children]}
    container[c.DisplayName] = [modelItem for modelItem in c.Children]

def parse_point(point):
    return point.X, point.Y


def process_pile_points():
    """
    The piles have a different ordering from the client.
    This function will return the correct order.
    """
    pile_row1 = list(range(1, 34))
    pile_row2 = list(range(34, 67))[::-1]
    pile_row3 = list(range(67, 100))
    pile_order = []
    for r1, r2, r3 in zip(pile_row1, pile_row2, pile_row3):
        for r in [r1, r2, r3]:
            pile_order.append(r)
    return pile_order


pile_order = process_pile_points() #By ATM
indexed = dict(zip(range(1, len(pile_order)+1), pile_order))


def process_cluster(modelitems, ref_point = Point(0,0)):
    """
    Process model items from the container dict
    {key: value} = {Root.DisplayName: [ModelItems of Root Children]}
    and returns the Cluster of Points sorted by distance from a reference point.
    Defaults (0,0) as reference point.
    """
    points = []
    for i, mitem in enumerate(modelitems):
        point3d = mitem.Geometry.BoundingBox.Center
        x, y = parse_point(point3d)
        points.append(Point(x, y, i+1))
    cluster = PointCluster(points)
    cluster.sort_by_distance(ref_point)
    return cluster.to_dict()





piles = ['00 PILES', '00 METAL FORMWORK', '00 IN SITU CONCRETE - PILES']
references = {}  # Stores the key:val pairs where key = Selection.Id and val is Model.Id
for item in container.keys():
    if item in piles:
        print(item)
        sorted_mitems = process_cluster(container[item])
    for i, child in enumerate(container[item]):
        col = ModelItemCollection()
        col.Add(child)
        newsel = SelectionSet(col)

        if item in ordered_set.keys():
            name_ref = name_map[item] + '-' + ordered_set[item][i + 1]
            newsel.DisplayName = name_ref
            references[name_ref] = child.InstanceGuid.ToString()

        elif item in chainages.keys():
            name_ref =  item.split()[-1] + ' ' + chainages[item][i + 1]
            newsel.DisplayName = name_ref
            references[name_ref] = child.InstanceGuid.ToString()

        elif item in piles:

            name_ref = "(" + str(sorted_mitems[i + 1]) + ")" + name_map[item] + '-' +  str(indexed[sorted_mitems[i + 1]])
            newsel.DisplayName = name_ref
            references[name_ref] = child.InstanceGuid.ToString()
			#newsel.DisplayName = name_ref
            #references[name_ref] = child.InstanceGuid.ToString()
			#print(name_ref)
        else:
            name_convention = item + '-' + str(i + 1)
            newsel.DisplayName = name_convention
            references[name_convention] = child.InstanceGuid.ToString()


        doc.SelectionSets.InsertCopy(0, newsel)
save_references(references)

