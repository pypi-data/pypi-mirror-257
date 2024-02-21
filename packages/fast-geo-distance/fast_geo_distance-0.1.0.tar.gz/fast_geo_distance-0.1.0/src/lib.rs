use geo::point;
use geo::prelude::*;
use pyo3::prelude::*;
use rayon::prelude::*;

#[pyfunction]
fn geodesic(latitude: f64, longitude: f64, points: Vec<(f64, f64)>) -> PyResult<Vec<f64>> {
    let p1 = point!(x: latitude, y: longitude);

    let distances: Vec<f64> = points.into_par_iter().map(|point| {
        let tmp_point = point!(x: point.0, y: point.1);

        let distance: f64 = p1.geodesic_distance(&tmp_point);

        return distance;
    })
    .collect();

    Ok(distances)
}

/// A Python module implemented in Rust.
#[pymodule]
fn fast_geo_distance(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(geodesic, m)?)?;
    Ok(())
}

// (40.7128, -74.006), (51.5074, -0.1278)
