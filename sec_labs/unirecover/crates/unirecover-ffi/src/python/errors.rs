use pyo3::prelude::*;

pub fn runtime_error(message: &str) -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(message.to_string())
}
