//! This module provides functionality for parsing VCF files and generating SBS data.
//!
//! The main function in this module is `parse_vcf_files`, which takes a list of VCF files,
//! a reference genome, and a context size as input. It reads the VCF files, collects the data,
//! reshapes it into a 2D array, and returns it as a numpy array.
//!
//! The module also provides helper functions for reading and processing the VCF files and
//! the associated byte files.
use numpy::PyArray;
use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3::Python;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader, Read, Seek, SeekFrom};

/// Parses VCF files and generates a NumPy array containing the parsed data.
///
/// # Arguments
///
/// * `py` - A Python interpreter session.
/// * `vcf_files` - A list of paths to VCF files.
/// * `ref_genome` - A string indicating the reference genome.
/// * `context` - An integer specifying the context size.
///
/// # Returns
///
/// A NumPy array containing the parsed data.
///
/// # Errors
///
/// Returns a Python error if there is an issue reading or parsing the VCF files.
#[pyfunction]
fn parse_vcf_files(
    py: Python,
    vcf_files: &PyList,
    ref_genome: &str,
    context: usize,
) -> PyResult<PyObject> {
    // All the collected data from the VCF files
    let all_data = read_and_collect_vcf_data(vcf_files, ref_genome, context)?;
    // Reshape the data into a 2D array
    let s = all_data.len();
    let t = if !all_data.is_empty() {
        all_data[0].len()
    } else {
        0
    };
    let py_objects: Vec<PyObject> = all_data
        .into_iter()
        .flatten()
        .map(|x| x.to_object(py))
        .collect();
    // Convert it to a numpy array
    let np_array = PyArray::from_iter(py, py_objects.iter().map(|x| x.to_object(py)))
        .reshape([s, t])
        .unwrap();
    Ok(np_array.to_object(py))
}

/// Reads the contents of VCF files and collects the relevant data.
///
/// # Arguments
///
/// * `vcf_files` - A list of paths to VCF files.
/// * `ref_genome` - A string indicating the reference genome.
/// * `context` - An integer specifying the context size.
///
/// # Returns
///
/// A vector containing the collected data.
///
/// # Errors
///
/// Returns an I/O error if there is an issue reading the VCF files.
fn read_and_collect_vcf_data(
    vcf_files: &PyList,
    ref_genome: &str,
    context: usize,
) -> Result<Vec<Vec<String>>, PyErr> {
    let mut all_data = Vec::new();

    for vcf_file in vcf_files {
        let vcf_file_path: String = vcf_file.extract()?;
        let data = read_vcf_file_contents(&vcf_file_path, &ref_genome, &context)?;
        all_data.extend(data);
    }

    Ok(all_data)
}

/// Reads the contents of a single VCF file and processes the data.
///
/// # Arguments
///
/// * `vcf_file` - Path to the VCF file.
/// * `ref_genome` - A string indicating the reference genome.
/// * `context` - An integer specifying the context size.
///
/// # Returns
///
/// A vector containing the processed data.
///
/// # Errors
///
/// Returns an I/O error if there is an issue reading the VCF file.
fn read_vcf_file_contents(
    vcf_file: &str,
    ref_genome: &str,
    context: &usize,
) -> Result<Vec<Vec<String>>, std::io::Error> {
    let nucleotides = vec!["A", "C", "G", "T"];
    let translate_purine_to_pyrimidine: HashMap<char, char> =
        [('A', 'T'), ('G', 'C')].iter().cloned().collect();
    let translate_nucleotide: HashMap<char, char> =
        [('A', 'T'), ('C', 'G'), ('G', 'C'), ('T', 'A')]
            .iter()
            .cloned()
            .collect();
    let mut data = Vec::new();

    let file = File::open(vcf_file)
        .map_err(|_| pyo3::exceptions::PyIOError::new_err("Failed to open the VCF file"))?;

    for line in BufReader::new(file).lines() {
        let line = line.map_err(|_| {
            pyo3::exceptions::PyIOError::new_err("Error reading line from the VCF file")
        })?;
        let fields: Vec<&str> = line.split('\t').collect();

        if fields.len() >= 10 {
            let reference_genome = fields[3];
            let mutation_type = fields[4];
            let reference_allele = fields[8];
            let alternate_allele = fields[9];

            let translated_alternate: String = if (reference_allele == "A"
                || reference_allele == "G")
                && nucleotides.contains(&alternate_allele)
            {
                alternate_allele
                    .chars()
                    .map(|c| *translate_nucleotide.get(&c).unwrap_or(&c))
                    .collect()
            } else {
                alternate_allele.to_string()
            };
            let translated_reference: String = reference_allele
                .chars()
                .map(|c| *translate_purine_to_pyrimidine.get(&c).unwrap_or(&c))
                .collect();

            if (reference_genome == "GRCh37" || reference_genome == "GRCh38")
                && (mutation_type == "SNP" || mutation_type == "SNV")
                && nucleotides.contains(&alternate_allele)
                && (translated_reference != translated_alternate)
            {
                let position = fields[6].parse::<usize>().unwrap() - 1;
                let start = position.saturating_sub(*context / 2);
                let end = position + *context / 2 + 1;
                let total_path = format!("{}/{}/{}.txt", ref_genome, reference_genome, fields[5]);
                let (left, right) = read_bytes_file_contents(&total_path, start, end)?;
                let sample = format!("{}::{}", fields[0], fields[1]);
                let new_mutation_type = format!(
                    "{}[{}>{}]{}",
                    left, translated_reference, translated_alternate, right
                );
                data.push(vec![sample, new_mutation_type]);
            }
        }
    }

    Ok(data)
}

/// Reads a portion of a binary file and translates the bytes into characters based on a mapping.
///
/// # Arguments
///
/// * `file_path` - Path to the binary file.
/// * `start` - The starting position to read from.
/// * `end` - The ending position to read to.
///
/// # Returns
///
/// A tuple containing left and right strings.
///
/// # Errors
///
/// Returns an I/O error if there is an issue reading the file
fn read_bytes_file_contents(
    file_path: &str,
    start: usize,
    end: usize,
) -> Result<(String, String), std::io::Error> {
    let mut file = File::open(file_path)
        .map_err(|_| pyo3::exceptions::PyIOError::new_err("Failed to open the bytes file"))?;
    file.seek(SeekFrom::Start(start as u64)).map_err(|_| {
        pyo3::exceptions::PyIOError::new_err("Error seeking to the specified position")
    })?;
    let bytes_to_read = end - start;
    let mut buffer = vec![0; bytes_to_read];
    file.read_exact(&mut buffer)
        .map_err(|_| pyo3::exceptions::PyIOError::new_err("Error reading data from the file"))?;

    let translation_mapping: HashMap<u8, char> = [
        (0, 'A'),
        (1, 'C'),
        (2, 'G'),
        (3, 'T'),
        (4, 'A'),
        (5, 'C'),
        (6, 'G'),
        (7, 'T'),
        (8, 'A'),
        (9, 'C'),
        (10, 'G'),
        (11, 'T'),
        (12, 'A'),
        (13, 'C'),
        (14, 'G'),
        (15, 'T'),
        (16, 'N'),
        (17, 'N'),
        (18, 'N'),
        (19, 'N'),
    ]
    .iter()
    .cloned()
    .collect();
    let middle_index = bytes_to_read / 2;
    let result: String = buffer
        .iter()
        .map(|&byte| translation_mapping.get(&byte).unwrap_or(&' ').to_owned())
        .collect();
    let result_chars: Vec<char> = result.chars().collect();
    let left = result_chars[..middle_index].iter().collect::<String>();
    let right = result_chars[middle_index + 1..].iter().collect::<String>();

    Ok((left, right))
}

/// A Python module implemented in Rust.
///
/// Exposes the `parse_vcf_files` function to Python.
#[pymodule]
fn sbsgenerator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(parse_vcf_files, m)?)?;
    Ok(())
}
