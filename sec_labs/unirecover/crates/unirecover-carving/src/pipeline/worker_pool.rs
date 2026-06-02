use rayon::ThreadPoolBuilder;

pub struct ParallelWorkerOrchestrator;

impl ParallelWorkerOrchestrator {
    pub fn initialize_pool(thread_count: usize) -> Result<(), &'static str> {
        ThreadPoolBuilder::new()
            .num_threads(thread_count)
            .thread_name(|idx| format!("unirecover-carve-{}", idx))
            .build_global()
            .map_err(|_| "Failed to spawn framework worker pool thread topology")
    }
}
