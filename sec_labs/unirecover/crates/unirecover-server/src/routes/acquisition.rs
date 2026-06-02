use actix_web::{post, HttpResponse, Responder};

#[post("/api/v1/acquisition/start")]
pub async fn start_acquisition() -> impl Responder {
    HttpResponse::Accepted().json("Acquisition pipeline successfully spawned")
}
