use pyo3::prelude::*;

#[pyfunction]
fn create_range_py(_py: Python, start: i32, end: i32) -> Vec<i32> {
    (start..end).collect()
}

#[pymodule]
#[pyo3(name = "rust_range")]
fn rust_range(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(create_range_py, m)?)?;
    Ok(())
}


