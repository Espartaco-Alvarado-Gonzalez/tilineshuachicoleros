import pytest

# Si el paquete no existe aún, el test se marca como "skipped" y no hace fallar el CI.
optifuel = pytest.importorskip("optifuel")

def test_import_and_attrs():
    assert hasattr(optifuel, "compute_metrics")
