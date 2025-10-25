import numpy as np
import pandas as pd

def _build_df(data):
    df = pd.DataFrame(data)
    df["cap_efectiva"] = np.maximum(df["capacidad"], df["actual"])
    df["flag_cap"] = np.where(df["actual"] > df["capacidad"], "Actual>Capacidad", "OK")
    df["litros_dia"] = np.where(df["dias"] > 0, df["consumo"]/df["dias"], np.nan)
    mediana_reg = np.nanmedian(df.loc[df["producto"]=="Regular","litros_dia"])
    mask_imp = (df["producto"]=="Regular") & ~np.isfinite(df["litros_dia"])
    df.loc[mask_imp, "litros_dia"] = mediana_reg
    df["fuente_tasa"] = np.where(mask_imp, "imputado_mediana_regular",
                                 np.where(np.isfinite(df["litros_dia"]), "observado","sin_datos"))
    df["dias_agotar"] = df["actual"] / df["litros_dia"]
    df.loc[~np.isfinite(df["dias_agotar"]), "dias_agotar"] = np.nan
    return df

def compute_metrics(data, prices, lead_time, buffer, extra_days, cap_fill):
    df = _build_df(data).copy()
    df["precio_min"] = df["producto"].map(lambda p: prices[p]["min"])
    df["precio_max"] = df["producto"].map(lambda p: prices[p]["max"])
    rL = (1.0 + buffer) * lead_time * df["litros_dia"]
    objetivo = np.minimum(rL + extra_days * df["litros_dia"], cap_fill * df["cap_efectiva"])
    pedido = np.maximum(0.0, objetivo - df["actual"])
    df["r_L"] = rL
    df["objetivo_litros"] = objetivo
    df["pedido_recomendado_L"] = pedido
    df["gasto_diario_min"] = df["litros_dia"] * df["precio_min"]
    df["gasto_diario_max"] = df["litros_dia"] * df["precio_max"]
    df["costo_reabasto_min"] = pedido * df["precio_min"]
    df["costo_reabasto_max"] = pedido * df["precio_max"]
    def riesgo(d):
        if not np.isfinite(d): return "SIN DATOS"
        if d <= 0: return "URGENTE"
        if d < lead_time: return "ALTO"
        if d < 3*lead_time: return "MEDIO"
        return "BAJO"
    df["riesgo"] = [riesgo(x) for x in df["dias_agotar"]]
    return df

def objective_cost(df, rho=5.0):
    short = np.maximum(0.0, df["r_L"] - df["actual"])
    penalty = rho * (short**2 / (df["litros_dia"] + 1.0))
    order_cost = df["costo_reabasto_min"]
    return float((order_cost + penalty).sum())
