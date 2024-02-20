use std::path::Path;

use pyo3::prelude::*;
use wordcut_engine::Wordcut;
use wordcut_engine::load_cluster_rules;
use wordcut_engine::load_dict;

#[pyclass(subclass)]
struct Seema {
    wordcut: Wordcut,
}

#[pymethods]
impl Seema {
    #[new]
    fn new(dict_path_str: &str, cluster_rules_path_str: &str) -> Self {
	let dict_path = Path::new(dict_path_str);
	let cluster_rules_path = Path::new(cluster_rules_path_str);
        let dict = load_dict(&dict_path).unwrap();
        let cluster_re = load_cluster_rules(&cluster_rules_path).unwrap();
        let wordcut = Wordcut::new_with_cluster_re(dict, cluster_re);
        Seema {
            wordcut,
        }
    }

    /// word tokenize
    fn segment_into_strings(&self, text: &str) -> PyResult<Vec<String>> {
        Ok(self.wordcut.segment_into_strings(&text))
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn seema(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Seema>()?;
    Ok(())
}
