import pymatgen.core as pg

PETTIFOR_KEYS = tuple(range(1, 104))
# def pettifor_keys():
#     return tuple(range(1, 104))

def element_to_pettifor(elt):
    if isinstance(elt, str):
        elt = pg.Element(elt)
    assert isinstance(elt, pg.Element)
    return elt.mendeleev_no

def composition_to_pettifor_array(comp):
	"""
		Create an array representation of comp.
		Position i is normed quantity of the element with pettifor number i.
	"""
	if isinstance(comp, str):
		comp = pg.Composition(comp)

	# TODO magic number ick. Max petti number is 103 so need len 104 array. index 0 is unused.
	comp_array = [0]*104 
	for el in comp.elements:
		p_num = int(el.mendeleev_no)
		comp_array[p_num] = comp.get_atomic_fraction(el)

	return comp_array

def composition_to_pettifor_dict(comp):
	"""
		Create a dictionary representation of comp of the form {pettifor_number: quantity}
	"""
	if isinstance(comp, str):
		comp = pg.Composition(comp)

	comp_dict = {}
	for el in comp.elements:
		p_num = int(el.mendeleev_no)
		comp_dict[p_num] = comp.get_atomic_fraction(el)

	return comp_dict

def calculcate_emd(comp1, comp2) -> float:
	array1 = composition_to_pettifor_array(comp1)
	array2 = composition_to_pettifor_array(comp2)

	diffs = [0] * 104
	for i, val1 in enumerate(array1):
		if i == 0:
			continue
		val2 = array2[i]
		diffs[i] = abs(diffs[i-1] + val1 - val2)
	
	return sum(diffs)


def calculate_emd_dict(comp1, comp2) -> float:
	diffs = [0]*104
	for i in range(104):
		if i == 0:
			continue
		val1 = comp1.get(i, 0)
		val2 = comp2.get(i, 0)
		diffs[i] = abs(diffs[i-1] + val1 - val2)

	return sum(diffs)

def get_radii(sps, cn=None):
	radii = {}
	if cn is not None:
		for sp in sps.ungrouped_view():
			try:
				radii[str(sp)] = sp.get_shannon_radius(cn=cn, spin='High Spin', radius_type='crystal')
			except KeyError:
				pass
	else:
		radii = {str(sp): sp.ionic_radius for sp in sps.ungrouped_view()}
	return radii