use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;

use pyo3::types::{PyAny, PyDict};

use serde_pyobject::{from_pyobject, to_pyobject};

use option_pricing::implied_vol::{ImpliedVol, Input, Method};

#[pyclass]
pub struct WrapperImpliedVol {
    iv: ImpliedVol,
}

#[pyclass]
#[derive(serde::Deserialize)]
pub struct WrapperInput {
    input: Input,
    method: Method,
}

#[pymethods]
impl WrapperImpliedVol {
    #[new]
    #[pyo3(signature = (input_params))]
    fn new(input_params: &PyDict) -> Result<Self, PyErr> {
        // println!("input_params: {:?}\n", input_params);

        let res: Result<WrapperInput, serde_pyobject::Error> = from_pyobject(input_params);

        match res {
            Ok(wi) => Ok(WrapperImpliedVol {
                iv: ImpliedVol::new(wi.input, wi.method),
            }),
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }

    fn get_vol(slf: &PyCell<Self>) -> Result<&PyAny, PyErr> {
        let obj = slf.borrow();
        let out = &obj.iv.output;

        match out {
            Ok(output) => {
                let out = to_pyobject(slf.py(), &output).unwrap();
                Ok(out)
            }
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }

    fn __repr__(slf: &PyCell<Self>) -> Result<String, PyErr> {
        let class_name = slf.get_type().name()?;
        let obj = slf.borrow();

        let str_input = format!("{:?}", obj.iv.input);

        let str_output = format!("{:?}", obj.iv.output);

        Ok(format!(
            "{}:(input={:?}, n_output={:?})",
            class_name, str_input, str_output,
        ))
    }
}
