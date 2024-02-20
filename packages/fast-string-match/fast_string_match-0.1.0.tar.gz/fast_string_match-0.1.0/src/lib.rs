use pyo3::prelude::*;

// Example function to find the closest match
fn find_closest_match<'a>(query: &str, options: &[&'a str]) -> Option<&'a str> {
    options.iter().min_by_key(|&option| levenshtein_distance(query, option)).cloned()
}

// Helper function to calculate Levenshtein distance
fn levenshtein_distance(s: &str, t: &str) -> usize {
    let mut dp = vec![vec![0; t.len() + 1]; s.len() + 1];
    for i in 0..=s.len() {
        dp[i][0] = i;
    }
    for j in 0..=t.len() {
        dp[0][j] = j;
    }
    for (i, sc) in s.chars().enumerate() {
        for (j, tc) in t.chars().enumerate() {
            let cost = if sc == tc { 0 } else { 1 };
            dp[i + 1][j + 1] = (dp[i][j + 1] + 1)
                .min(dp[i + 1][j] + 1)
                .min(dp[i][j] + cost);
        }
    }
    dp[s.len()][t.len()]
}

#[pyfunction]
fn closest_match_py<'a>(_py: Python, query: &str, options: Vec<&'a str>) -> Option<String> {
    find_closest_match(query, &options).map(|s| s.to_string())
}

#[pymodule]
fn fast_string_match(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(closest_match_py, m)?)?;
    Ok(())
}

