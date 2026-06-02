#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::*;

pub unsafe fn scan_chunk_avx2(data: &[u8], pattern: u8) -> Vec<usize> {
    let mut matches = Vec::new();
    if data.len() < 32 { return matches; }

    let pattern_vec = _mm256_set1_epi8(pattern as i8);
    
    for i in (0..data.len() - 32).step_by(32) {
        let chunk = _mm256_loadu_si256(data.as_ptr().add(i) as *const __m256i);
        let cmp = _mm256_cmpeq_epi8(chunk, pattern_vec);
        let mask = _mm256_movemask_epi8(cmp);
        
        if mask != 0 {
            for bit in 0..32 {
                if (mask & (1 << bit)) != 0 {
                    matches.push(i + bit);
                }
            }
        }
    }
    matches
}
