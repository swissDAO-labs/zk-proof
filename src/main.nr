use dep::std::hash::sha256;

// This circuit proves that the user knows the input of the provided hash of the prompt
// In the contract, if we would like to tie the 
fn main(prompt_bytes: [u8; 256], hash: pub [u8; 32]) {
    // Generate sha256 hash of input
    let compare_hash = sha256(prompt_bytes);
    assert(hash == compare_hash);
}

#[test]
fn test_main() {
    let prompt_str = "Renaissance-style portrait of an astronaut in space, detailed starry background, reflective helmet.";
    let mut prompt_bytes = prompt_str.as_bytes();

    let mut padded_input: [u8; 256] = [0; 256];

    for i in 0..prompt_bytes.len() {
        padded_input[i] = prompt_bytes[i];
    }

    let prompt_hash: [u8; 32] = sha256(padded_input);
    println(padded_input);
    println(prompt_hash);

    main(padded_input, prompt_hash);
}
