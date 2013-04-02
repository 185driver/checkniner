from .models import AircraftType, Checkout


def get_aircrafttype_names(order="name"):
    """Populates a sorted list with the names of all known
    AircraftTypes"""
    aircrafttypes = AircraftType.objects.order_by(order)
    return [actype.name for actype in aircrafttypes]


def pilot_checkouts_grouped_by_airstrip(pilot):
    """Organizes the pilot's checkouts by airstrips.
    
    Returns a list (sorted by airstrip ident) in which
    every airstrip at which the given pilot is checked 
    out is a dictionary, with a key:value pair indicating
    whether the pilot is checked out or not in each
    AircraftType."""
    actypes = get_aircrafttype_names()

    pilot_checkouts = Checkout.objects.filter(pilot=pilot).select_related('airstrip', 'aircraft_type')
    pilot_checkouts = pilot_checkouts.order_by('airstrip__ident', 'aircraft_type__name')
    
    by_airstrip = []
    row_data = None
    for c in pilot_checkouts:
	if row_data == None or c.airstrip.ident != row_data['ident']:
	    # Don't save on the initial loop iteration
	    if row_data != None:
		by_airstrip.append(row_data)
	    
	    row_data = {
		'ident': c.airstrip.ident,
		'name': c.airstrip.name,
		'aircraft': [False,] * len(actypes),
	    }
	
	ac_index = actypes.index(c.aircraft_type.name)
	row_data['aircraft'][ac_index] = True
    
    # Saving the very last airstrip record is missed by 
    # the 'is this the same airstrip as before?' check,
    # so we'll manually save it to the list (if necessary)
    if row_data != None:
        by_airstrip.append(row_data)
    
    return by_airstrip