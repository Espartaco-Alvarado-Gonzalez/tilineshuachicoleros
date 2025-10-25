import math, random
def clamp(x, lo, hi): return max(lo, min(hi, x))
def simulated_annealing(eval_fn, x0, bounds, T0=1.0, Tf=1e-3, iters=4000, alpha=0.995, step=0.05):
    x, fx, T = x0[:], eval_fn(x0), T0
    best_x, best_fx = x[:], fx
    for _ in range(iters):
        i = random.randrange(len(x))
        span = bounds[i][1] - bounds[i][0]
        cand = x[:]
        cand[i] = clamp(x[i] + (random.random()*2-1)*step*span, bounds[i][0], bounds[i][1])
        fc = eval_fn(cand)
        if fc < fx or random.random() < math.exp(-(fc - fx)/max(T,1e-12)):
            x, fx = cand, fc
            if fc < best_fx: best_x, best_fx = cand[:], fc
        T = max(Tf, alpha*T)
    return best_x, best_fx
