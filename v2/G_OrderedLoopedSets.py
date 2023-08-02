def save_references(_d):
    with open(os.path.join(os.getcwd(), 'references.json'), 'w') as f:
        json.dump(_d, f)


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
name_map = {'00 SLABS - SL1': 'SL1', '00 SLABS - SL2': 'SL2', '00 SLABS - SL3': 'SL3', '00 SLABS - SL4A': 'SL4A',
            '00 SLABS - SL4B': 'SL4B', '00 SLABS - SL5A': 'SL5A', '00 SLABS - SL5B': 'SL5B', '00 SLABS - SL6A': 'SL6A',
            '00 SLABS - SL6B': 'SL6B', '00 SLABS - SL7A': 'SL7A', '00 SLABS - SL7B': 'SL7B', '00 SLABS - SL8A': 'SL8A',
            '00 SLABS - SL8B': 'SL8B', '00 BEAMS PC1': 'PC1', '00 BEAMS PC2': 'PC2', '00 PILES': 'PILE',
            '00 METAL FORMWORK': 'FORMWORK', '00 IN SITU CONCRETE - PILES': 'PLUG'}

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

    # def __repr__(self):
    # return f"Point( {self.index} - {self.x}-{self.y})"


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
            point.newindex = i
            self.newindex = [point.newindex for point in self.points_list]
        return self.points_list

    def to_dict(self):
        return {point.index: point.newindex for point in self.points_list}


doc.SelectionSets.Clear()
root = doc.Models[0].RootItem
container = {}

for c in root.Children:
    # Create a dictionary with
    # {key: value} = {Root.DisplayName: [ModelItems of Root Children]}
    container[c.DisplayName] = [modelItem for modelItem in c.Children]
# ppoints = []


pile_order = process_pile_points()
indexed = dict(zip(range(len(pile_order)), pile_order))

for item in piles:
    PileModelItems = container[item]
    ppoints = []
    for i, mitem in enumerate(PileModelItems):
        point3d = mitem.Geometry.BoundingBox.Center
        x, y = parse_point(point3d)
        # name_shortcut = name_map[piles[0]]
        # print(Point(parse_point(point3d))
        ppoints.append(Point(x, y, i))
    zero = Point(0, 0)

    cluster = PointCluster(ppoints)
    cluster.sort_by_distance(zero)
    pile_sorted = cluster.to_dict()
    references = {}


    for j, child in enumerate(PileModelItems):
        col = ModelItemCollection()
        col.Add(child)
        newsel = SelectionSet(col)
        #print(j)

        name_ref = str(pile_sorted[j]) + "__" + name_map[item] + '-' + str(indexed[pile_sorted[j]])
        newsel.DisplayName = name_ref
        references[name_ref] = child.InstanceGuid.ToString()

        doc.SelectionSets.InsertCopy(0, newsel)

for item in slabs:
	print(item)
	SlabModelItems = container[item]
	#print(SlabModelItems)
	for i,mitem in enumerate(SlabModelItems):
		print(item,i, mitem)
		#point3d = mitem.Geometry.BoundingBox.Center



