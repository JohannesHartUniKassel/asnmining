use bgpkit_parser::BgpkitParser;
use pyo3::prelude::*;
use pyo3::IntoPyObjectExt;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::BTreeMap;
use std::fs::File;
use csv::ReaderBuilder;


#[derive(IntoPyObject)]
struct Result {
    country_map: HashMap<String, i32>,
    map: HashMap<String, (String, String)>
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn asn_mining(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(bgp, m)?)?;
    m.add_function(wrap_pyfunction!(asns, m)?)?;
    m.add_function(wrap_pyfunction!(asns_nro, m)?)?;
    Ok(())
}

#[pyfunction]
fn bgp(path: String) -> PyResult<BTreeMap<String, HashSet<String>>> {
    let parser = BgpkitParser::new(path.as_str()).unwrap();
    let mut asns: HashSet<String> = HashSet::new();
    let mut originates: HashSet<String> = HashSet::new();
    for elem in parser {
        match elem.origin_asns {
            Some(origins) => {
                for asn in origins {
                    originates.insert(asn.to_string());
                }
            }
            None => {}
        }
        match elem.as_path {
            Some(path) => {
                for el in path {
                    for asn in el {
                        asns.insert(asn.to_string());
                    }
                }
            }
            None => {}
        }
    }
    let mut result: BTreeMap<String, HashSet<String>> = BTreeMap::new();
    result.insert("all_asns".to_string(), asns);
    result.insert("origins".to_string(), originates);
    Ok(result)
}

#[pyfunction]
fn asns_nro(py: Python, path: String) -> PyResult<PyObject> {
    // Datei öffnen
    let file = File::open(path);

    let mut map = HashMap::<String, i32>::new();
    let mut set: HashMap<String, (String, String)> = HashMap::new();

    // CSV-Reader ohne Header-Erkennung
    let mut rdr = ReaderBuilder::new()
        .has_headers(false) // Verhindert automatische Header-Erkennung
        .delimiter(b'|') // Setzt den Separator
        .flexible(true)  // Ermöglicht flexiblere Fehlerbehandlung
        .from_reader(file.unwrap());

    // Die CSV-Zeilen durchgehen
    for result in rdr.records() {
        let record = result.unwrap();
        if record.len() == 9 {
            if record[2] == *"asn" {
                if record[6] == *"assigned" || true {
                    set.insert(record[3].to_string(), (record[1].to_string(), record[0].to_string()));
                    if map.contains_key(&record[1]) {
                        map.insert(record[1].to_string(), map.get(&record[1].to_string()).unwrap()+1);
                    } else {
                        map.insert(record[1].to_string(), 1);
                    }
                }
            }
        }
    }
    let r: Result = Result {
        country_map: map,
        map: set
    };
    r.into_py_any(py)
}

#[pyfunction]
fn asns(py: Python, path: String) -> PyResult<PyObject> {
    // Datei öffnen
    let file = File::open(path);

    let mut map = HashMap::<String, i32>::new();
    let mut set: HashMap<String, (String, String)> = HashMap::new();

    // CSV-Reader ohne Header-Erkennung
    let mut rdr = ReaderBuilder::new()
        .has_headers(false) // Verhindert automatische Header-Erkennung
        .delimiter(b'|') // Setzt den Separator
        .flexible(true)  // Ermöglicht flexiblere Fehlerbehandlung
        .from_reader(file.unwrap());

    // Die CSV-Zeilen durchgehen
    for result in rdr.records() {
        let record = result.unwrap();
        if record.len() == 8 {
            if record[2] == *"asn" {
                if record[6] == *"assigned" || true {
                    set.insert(record[3].to_string(), (record[1].to_string(), record[0].to_string()));
                    if map.contains_key(&record[1]) {
                        map.insert(record[1].to_string(), map.get(&record[1].to_string()).unwrap()+1);
                    } else {
                        map.insert(record[1].to_string(), 1);
                    }
                }
            }
        }
    }
    let r = Result {
        country_map: map,
        map: set
    };
    r.into_py_any(py)
}