use actix_web::{App, HttpServer};

mod routes;
mod middleware;

use routes::acquisition::start_acquisition;
use routes::carving::trigger_carve;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(start_acquisition)
            .service(trigger_carve)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
