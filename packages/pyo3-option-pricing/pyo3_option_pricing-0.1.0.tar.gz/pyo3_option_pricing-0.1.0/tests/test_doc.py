def test_doc() -> None:
    import pyo3_option_pricing

    assert (
        pyo3_option_pricing.__doc__
        == "BlackScholes option pricing implemented in Rust and exposed to Python with PyO3."
    )
