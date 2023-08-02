def unhide():
	elem = doc.Models[0].RootItem
	collector = ModelItemCollection()
	for parent in elem.Children:
		for child in parent.Children:
			collector.Add(child)
	doc.Models.SetHidden(collector,False)
	return collector

collector = unhide()
doc.Models.OverridePermanentColor(collector, Color(0.8275, 0.8275, 0.8275))
doc.Models.OverridePermanentTransparency(collector, 0.5)

