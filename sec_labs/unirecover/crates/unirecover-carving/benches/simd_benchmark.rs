use criterion::{criterion_group, criterion_main, Criterion};

fn benchmark_signature_scan(c: &mut Criterion) {
    let dummy_buffer = vec![0x00u8; 1024 * 1024]; // 1MB allocation block
    c.bench_function("scalar_scan_baseline", |b| b.iter(|| {
        let _count = dummy_buffer.iter().filter(|&&x| x == 0xFF).count();
    }));
}

criterion_group!(benches, benchmark_signature_scan);
criterion_main!(benches);
