use actix_web::{post, HttpResponse, Responder};

#[post("/api/v1/carve")]
pub async fn trigger_carve() -> impl Responder {
    HttpResponse::Ok().json("Carver active")
}
