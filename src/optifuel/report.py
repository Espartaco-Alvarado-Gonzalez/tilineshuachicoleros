import pandas as pd
def export_excel(df, prices, params, path):
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        cols = ["estacion","producto","capacidad","actual","cap_efectiva","flag_cap",
                "dias","consumo","litros_dia","fuente_tasa","dias_agotar",
                "precio_min","precio_max","gasto_diario_min","gasto_diario_max",
                "r_L","objetivo_litros","pedido_recomendado_L",
                "costo_reabasto_min","costo_reabasto_max","riesgo"]
        d = df.copy()
        for c in d.columns:
            if str(d[c].dtype)[:1] in "fc": d[c] = d[c].astype(float).round(2)
        d[cols].to_excel(writer, index=False, sheet_name="Metrica_y_Pedido")
        pd.DataFrame([
            {"producto":"Regular","precio_min":prices["Regular"]["min"],"precio_max":prices["Regular"]["max"]},
            {"producto":"Premium","precio_min":prices["Premium"]["min"],"precio_max":prices["Premium"]["max"]},
            {"producto":"Diesel","precio_min":prices["Diesel"]["min"],"precio_max":prices["Diesel"]["max"]},
        ]).to_excel(writer, index=False, sheet_name="Precios")
        pd.DataFrame({
            "parametro":["lead_time_dias","buffer","extra_dias","cap_fill"],
            "valor":[params["lead_time_dias"], params["buffer"], params["extra_dias"], params["cap_fill"]],
        }).to_excel(writer, index=False, sheet_name="Parametros")
