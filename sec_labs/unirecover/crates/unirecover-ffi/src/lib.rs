pub mod python;

use pyo3::prelude::*;
use crate::python::engine::PyRecoveryEngine;

#[pymodule]
fn unirecover_backend(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyRecoveryEngine>()?;
    Ok(())
}
