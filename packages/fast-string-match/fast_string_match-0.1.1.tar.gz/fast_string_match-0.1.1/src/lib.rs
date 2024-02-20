use pyo3::prelude::*;
    use closestmatch::ClosestMatch;

// Example function to find the closest match
fn find_closest_match<'a>(query: &str, options: &[&'a str]) -> Option<&'a str> {
    options.iter().min_by_key(|&option| levenshtein_distance(query, option)).cloned()
}

// Helper function to calculate Levenshtein distance
fn levenshtein_distance(s: &str, t: &str) -> usize {
    let s_chars: Vec<char> = s.chars().collect();
    let t_chars: Vec<char> = t.chars().collect();
    let s_len = s_chars.len();
    let t_len = t_chars.len();

    let mut dp = vec![vec![0; t_len + 1]; s_len + 1];

    for i in 0..=s_len {
        dp[i][0] = i;
    }
    for j in 0..=t_len {
        dp[0][j] = j;
    }

    for i in 1..=s_len {
        for j in 1..=t_len {
            let cost = if s_chars[i - 1] == t_chars[j - 1] { 0 } else { 1 };
            dp[i][j] = (dp[i - 1][j] + 1)
                .min(dp[i][j - 1] + 1)
                .min(dp[i - 1][j - 1] + cost);
        }
    }

    dp[s_len][t_len]
}

#[pyfunction]
fn closest_match(target: String, candidates: Vec<String>) -> Option<String> {
    let cm = ClosestMatch::new(candidates, [2, 3].to_vec());
    cm.get_closest(target)
}

#[pyfunction]
fn closest_match_distance<'a>(_py: Python, query: &str, options: Vec<&'a str>) -> Option<String> {
    find_closest_match(query, &options).map(|s| s.to_string())
}

#[pymodule]
fn fast_string_match(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(closest_match_distance, m)?)?;
    m.add_function(wrap_pyfunction!(closest_match, m)?)?;
    Ok(())
}

