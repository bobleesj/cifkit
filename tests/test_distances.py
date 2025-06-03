from cifkit import Cif

def test_expected_shortest_distance(cif_CUMNON_sb: Cif):

    assert cif_CUMNON_sb.shortest_distance == 6.732
    assert cif_CUMNON_sb.connections_flattened[:6] == [(('Sb', 'Sb'), 6.732), (('Sb', 'Sb'), 7.033), (('Sb', 'Sb'), 7.182), (('Sb', 'Sb'), 7.544), (('Sb', 'Sb'), 7.813), (('Sb', 'Sb'), 7.88)]
    
