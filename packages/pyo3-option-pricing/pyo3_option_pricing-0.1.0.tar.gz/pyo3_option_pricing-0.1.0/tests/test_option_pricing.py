from pyo3_option_pricing import BlackScholes, ImpliedVol


def is_close(a, b, tol=1e-3):
    """"""
    for k, v in a.items():
        if isinstance(v, float):
            assert abs(v - b[k]) < tol
        else:
            assert v == b[k]
    return True


def test_price_call():
    """"""
    input_call = {
        "is_call": True,
        "spot": 105.0,
        "strike": 100.0,
        "mat": 3.0,
        "vol": 0.15,
        "rate": 0.03,
        "div": 0.01,
    }
    output_call = {
        "is_call": True,
        "d1": 0.5486,
        "d2": 0.2888,
        "cdf_d1": 0.7084,
        "cdf_d2": 0.6136,
        "pdf_d1": 0.3432,
        "pdf_d2": 0.3826,
        "pv": 0.9139,
        "pv_k": 91.3931,
        "w": 0.9704,
        "price": 16.098,
        "delta": 0.6874,
        "gamma": 0.0122,
        "vega": 60.5716,
        "theta": -2.4750,
        "rho": 168.2485,
        "voma": 63.9890,
        "payoff": 5.0,
        "pv_payoff": 4.569,
    }

    bs = BlackScholes(input_call)
    price = bs.get_price()
    assert is_close(price, output_call)


def test_price_put():
    """"""
    input_put = {
        "is_call": False,
        "spot": 90.0,
        "strike": 100.0,
        "mat": 3.0,
        "vol": 0.15,
        "rate": 0.03,
        "div": 0.01,
    }
    output_put = {
        "is_call": False,
        "d1": -0.0447,
        "d2": -0.3045,
        "cdf_d1": 0.5178,
        "cdf_d2": 0.6196,
        "pdf_d1": 0.3985,
        "pdf_d2": 0.3809,
        "pv": 0.9139,
        "pv_k": 91.3931,
        "w": 0.9704,
        "price": 11.402,
        "delta": -0.5025,
        "gamma": 0.0165,
        "vega": 60.2908,
        "theta": -0.2607,
        "rho": -169.8884,
        "voma": 5.4694,
        "payoff": 10.0,
        "pv_payoff": 9.1393,
    }

    bs = BlackScholes(input_put)
    price = bs.get_price()
    assert is_close(price, output_put)


def test_put_call_parity():
    """"""
    input_call = {
        "is_call": True,
        "spot": 135.6,
        "strike": 100.0,
        "mat": 3.2,
        "vol": 0.25,
        "rate": 0.03,
        "div": 0.01,
    }
    bs = BlackScholes(input_call)
    price = bs.get_price()

    input_iv = {
        "price": price["price"],
        "spot": input_call["spot"],
        "strike": input_call["strike"],
        "mat": input_call["mat"],
        "rate": input_call["rate"],
        "div": input_call["div"],
        "iter": 10,
        "prec": 1e-6,
    }

    iv = ImpliedVol({"input": input_iv, "method": "Halley"})
    ivol = iv.get_vol()
    assert abs(ivol["vol"] - input_call["vol"]) < input_iv["prec"]
