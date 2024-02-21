use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;

use pyo3::types::{PyAny, PyDict};

use serde_pyobject::{from_pyobject, to_pyobject};

use option_pricing::black_scholes::{BlackScholes, Input};

#[pyclass]
pub struct WrapperBlackScholes {
    bs: BlackScholes,
}

#[pymethods]
impl WrapperBlackScholes {
    #[new]
    #[pyo3(signature = (input_params))]
    fn new(input_params: &PyDict) -> Result<Self, PyErr> {
        // println!("input_params: {:?}\n", input_params);

        let res: Result<Input, serde_pyobject::Error> = from_pyobject(input_params);

        match res {
            Ok(input) => Ok(WrapperBlackScholes {
                bs: BlackScholes::new(input),
            }),
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }

    fn get_price(slf: &PyCell<Self>) -> Result<&PyAny, PyErr> {
        let obj = slf.borrow();
        let out = &obj.bs.output;

        match out {
            Ok(output) => {
                let price = to_pyobject(slf.py(), &output).unwrap();
                Ok(price)
            }
            Err(e) => Err(PyErr::new::<PyTypeError, _>(format!("Error: {:?}", e))),
        }
    }

    fn __repr__(slf: &PyCell<Self>) -> Result<String, PyErr> {
        let class_name = slf.get_type().name()?;
        let obj = slf.borrow();

        let str_input = format!("{:?}", obj.bs.input);

        let str_output = format!("{:?}", obj.bs.output);

        Ok(format!(
            "{}:(input={:?}, n_output={:?})",
            class_name, str_input, str_output,
        ))
    }
}
