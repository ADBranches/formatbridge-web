FROM clux/muslrust:1.75.0 AS builder
WORKDIR /volume
COPY . .
RUN cargo build --release --bin unirecover-server

FROM scratch
COPY --from=builder /volume/target/x86_64-unknown-linux-musl/release/unirecover-server /unirecover-server
ENTRYPOINT ["/unirecover-server"]
