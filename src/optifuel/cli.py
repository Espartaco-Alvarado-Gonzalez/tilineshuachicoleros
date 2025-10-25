import json, click
from .data import DATA, PRICES
from .metrics import compute_metrics, objective_cost
from .optimize import simulated_annealing
from .report import export_excel

@click.group()
def main(): pass

@main.command()
@click.option("--out", type=click.Path(writable=True), default="reporte.xlsx", help="Excel de salida.")
@click.option("--data", "data_path", type=click.Path(exists=True), default=None, help="JSON alterno de datos.")
@click.option("--iters", type=int, default=2000, help="Iteraciones de recocido simulado.")
def run(out, data_path, iters):
    data = json.load(open(data_path)) if data_path else DATA
    bounds = [(1.0,5.0),(0.0,0.5),(0.0,2.0),(0.8,0.98)]  # L, buffer, extra, cap_fill
    x0 = [2.0, 0.20, 1.0, 0.95]
    def eval_params(x):
        L, buf, extra, fill = x
        df = compute_metrics(data, PRICES, L, buf, extra, fill)
        return objective_cost(df, rho=5.0)
    x_best, f_best = simulated_annealing(eval_params, x0, bounds, iters=iters)
    params = dict(lead_time_dias=x_best[0], buffer=x_best[1], extra_dias=x_best[2], cap_fill=x_best[3])
    df_final = compute_metrics(data, PRICES, params["lead_time_dias"], params["buffer"], params["extra_dias"], params["cap_fill"])
    export_excel(df_final, PRICES, params, out)
    click.echo(f"OK | J*={f_best:.3f} params={params} -> {out}")
