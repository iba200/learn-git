from app import somme, est_pair, devision

def test_somme():
    assert somme(2, 3) == 5
    assert somme(-1, 1) == 0
    assert somme(10, 5) == 15

def test_est_pair():
    assert est_pair(2) is True
    assert est_pair(3) is False
    assert est_pair(0) is True

def test_devion_par_zero():
    assert devision(-1)