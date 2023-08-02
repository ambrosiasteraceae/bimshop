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
            point.newindex = i + 1
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


def save_references(ref):
    import os
    import json
    with open(os.path.join(os.getcwd(), 'references.json'), 'w') as f:
        json.dump(ref, f)


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


slabs = ['00 SLABS - SL1', '00 SLABS - SL2', '00 SLABS - SL3', '00 SLABS - SL4A', '00 SLABS - SL4B', '00 SLABS - SL5A',
         '00 SLABS - SL5B', '00 SLABS - SL6A', '00 SLABS - SL6B', '00 SLABS - SL7A', '00 SLABS - SL7B',
         '00 SLABS - SL8A', '00 SLABS - SL8B', '00 BEAMS PC1', '00 BEAMS PC2']
piles = ['00 PILES', '00 METAL FORMWORK', '00 IN SITU CONCRETE - PILES']
rename_map = {'00 SLABS - SL1': 'SL1', '00 SLABS - SL2': 'SL2', '00 SLABS - SL3': 'SL3', '00 SLABS - SL4A': 'SL4A',
              '00 SLABS - SL4B': 'SL4B', '00 SLABS - SL5A': 'SL5A', '00 SLABS - SL5B': 'SL5B',
              '00 SLABS - SL6A': 'SL6A',
              '00 SLABS - SL6B': 'SL6B', '00 SLABS - SL7A': 'SL7A', '00 SLABS - SL7B': 'SL7B',
              '00 SLABS - SL8A': 'SL8A',
              '00 SLABS - SL8B': 'SL8B', '00 BEAMS PC1': 'PC1', '00 BEAMS PC2': 'PC2', '00 PILES': 'PILE',
              '00 METAL FORMWORK': 'FORMWORK', '00 IN SITU CONCRETE - PILES': 'PLUG'}
chainages = {
    '12.00 P3 - BEACH RECLAMATION - FILL': {1: 'CH:+2300 to +2400', 2: 'CH:+2100 to +2300', 3: 'CH:+1900 to +2100',
                                            4: 'CH:+1700 to +1900', 5: 'CH:+1500 to +1700', 6: 'CH:+1300 to +1500',
                                            7: 'CH:+1100 to +1300', 8: 'CH:+900 to +1100', 9: 'CH:+700 to +900',
                                            10: 'CH:+500 to +700', 11: 'CH:+300 to +500', 12: 'CH:+000 to +300', },
    'BEACH SAND': {1: 'CH:+2300 to +2400', 2: 'CH:+2100 to +2300', 3: 'CH:+1900 to +2100', 4: 'CH:+1700 to +1900',
                   5: 'CH:+1500 to +1700', 6: 'CH:+1300 to +1500', 7: 'CH:+1100 to +1300', 9: 'CH:+700 to +900',
                   8: 'CH:+900 to +1100', 10: 'CH:+500 to +700', 11: 'CH:+300 to +500', 12: 'CH:+000 to +300', },
    '11.20 P3 - NORTH GROYNE AR': {1: 'CH: +140 to +150', 2: 'CH: +000 to +020', 3: 'CH: +020 to +040',
                                   4: 'CH: +040 to +060', 5: 'CH: +060 to +080', 6: 'CH: +080 to +100',
                                   7: 'CH: +100 to +120', 8: 'CH: +120 to +140'},
    '11.10 P3 - NORTH GROYNE QR': {5: 'CH: +140 to +150', 2: 'CH: +000 to +020', 1: 'CH: +020 to +040',
                                   3: 'CH: +040 to +060', 4: 'CH: +060 to +080', 6: 'CH: +080 to +100',
                                   7: 'CH: +100 to +120', 8: 'CH: +120 to +140'},
    '00 IN SITU CONCRETE - SLAB': {1: '33%-67%', 2: '67%-100%', 3: '0-33%'}
}

doc.SelectionSets.Clear()
root = doc.Models[0].RootItem
container = {}

for c in root.Children:
    # Create a dictionary with
    # {key: value} = {Root.DisplayName: [ModelItems of Root Children]}
    container[c.DisplayName] = [modelItem for modelItem in c.Children]
# ppoints = []

NAMES = ['00 SLABS - SL1', '00 SLABS - SL2', '00 SLABS - SL3', '00 SLABS - SL4A', '00 SLABS - SL4B', '00 SLABS - SL5A',
         '00 SLABS - SL5B', '00 SLABS - SL6A', '00 SLABS - SL6B', '00 SLABS - SL7A', '00 SLABS - SL7B',
         '00 SLABS - SL8A', '00 SLABS - SL8B']
SLABS = []
SLABSDICT = {}
for k, v in container.items():
    if k in NAMES:
        for idx, item in enumerate(v):
            SLABS.append(item)
            key = item.InstanceGuid
            SLABSDICT[key.ToString()] = k + '-' + str(idx)


def process_cluster(modelitems, ref_point=Point(0, 0)):
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
        points.append(Point(x, y, i + 1))
    cluster = PointCluster(points)
    cluster.sort_by_distance(ref_point)
    return cluster.to_dict()


doc.SelectionSets.Clear()
sorted_items = process_cluster(SLABS)

for k, v in sorted_items.items():
    print(k, v)

for j, child in enumerate(SLABS):
    col = ModelItemCollection()
    col.Add(child)
    newsel = SelectionSet(col)
    # print(SLABSDICT[child.InstanceGuid.ToString()].split()[-1].split('-')[0])
    # print(str(sorted_items[j+1]))

    name_ref = "(" + str(sorted_items[j + 1]) + ")" + SLABSDICT[child.InstanceGuid.ToString()].split()[-1].split('-')[
        0] + '-' + SLABSDICT[child.InstanceGuid.ToString()].split()[-1].split('-')[1]
    print(name_ref)
    # newsel.DisplayName = name_ref
    # references[name_ref] = child.InstanceGuid.ToString()
    # doc.SelectionSets.InsertCopy(0, newsel)

