use pyo3::prelude::*;

mod black_scholes;
mod implied_vol;

/// BlackScholes option pricing implemented in Rust and exposed to Python with PyO3.
#[pymodule]
fn _rust(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    let mod_black_scholes = PyModule::new(py, "black_scholes")?;
    mod_black_scholes.add_class::<black_scholes::WrapperBlackScholes>()?;
    m.add_submodule(mod_black_scholes)?;

    let mod_implied_vol = PyModule::new(py, "implied_vol")?;
    mod_implied_vol.add_class::<implied_vol::WrapperImpliedVol>()?;
    m.add_submodule(mod_implied_vol)?;

    Ok(())
}
