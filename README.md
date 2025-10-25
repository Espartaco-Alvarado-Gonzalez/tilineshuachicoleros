# OptiFuel Starter

Genera un Excel con métricas (litros/día, días para agotar, gasto diario min/máx, r(L), pedido recomendado)
y ajusta parámetros globales por recocido simulado (SA).

USO:
    python -m venv .venv && source .venv/bin/activate
    pip install -e .
    optifuel run --out reporte.xlsx
