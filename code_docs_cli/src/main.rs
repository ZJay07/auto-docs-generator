use clap::Parser;
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the file to generate documentation for
    #[arg(short, long)]
    file_path: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct CodePayload {
    code: String,
}

#[derive(Deserialize, Debug)]
struct DocumentationResponse {
    documentation: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Parse CLI arguments
    let args = Args::parse();

    // Read the code from the provided file path
    let code = fs::read_to_string(&args.file_path)?;
    let payload = CodePayload { code };

    // Make an HTTP POST request to the Flask server
    let client = Client::new();
    let res = client
        .post("http://127.0.0.1:8000/generate-docs")
        .json(&payload)
        .send()
        .await?;

    if res.status().is_success() {
        let docs: DocumentationResponse = res.json().await?;
        println!("Generated Documentation:\n{}", docs.documentation);
    } else {
        eprintln!("Failed to generate documentation. Error: {:?}", res.text().await?);
    }

    Ok(())
}
