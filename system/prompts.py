async def preprare_prompt(file_path, code_lines, comment_lines, blank_lines ):
    try:
        ANALYZER = f'''     
You are an expert Solana program analyzer specializing in security audits and formal verification assessments of Rust-based Solana programs. Your task is to analyze Rust (.rs) files intended for deployment on the Solana blockchain and provide a complexity score to guide manual security audits and formal verification processes.

The full content of the Solana program to analyze will be provided.

When provided with the Solana program to analyze, consider the following:

1. Code metrics:
   - file_name: {file_path}
   - code_lines: {code_lines}
   - comment_lines: {comment_lines}
   - blank_lines: {blank_lines}

2. Analyze the potential complexity of the Solana program based on:
   - Number of lines of code
   - Actual code content and structure
   - Program size categorization:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large

3. IMPORTANTLY, evaluate the program's potential challenges for formal verification, considering:
   - Specific code structures and logic
   - Higher complexity when formally verifying non-linear math
   - Presence of floating-point operations (f32 or f64) vs. scaled integers

4. Assess the following Solana-specific complexity factors:
   - Frequency and complexity of Cross-Program Invocations (CPI)
   - Use of Program Derived Addresses (PDAs)
   - Implementation of complex account validation logic
   - Handling of multiple signers or complex signer validation
   - NOT using the Anchor framework (look for macros like #[program], #[derive(Accounts)], #[account])
   - Reliance on custom libraries over established ones (e.g., SPL library)
   - Implementation of non-linear mathematical operations (e.g., checked_mul, checked_div)

5. Consider security-focused elements:
   - Proper handling of account ownership and type checks
   - Correct implementation of rent exemption checks

6. Analyze external dependencies:
   - Number and nature of external crates used

7. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

8. Evaluate the ratio of comments to code

9. Assign a complexity score from 1 to 10, where:
    1-3: Simple programs with straightforward logic and minimal Solana-specific constructs
    4-6: Moderate complexity with some Solana-specific features and potential security considerations
    7-10: High complexity programs with multiple CPIs, complex account structures, and advanced Solana features

YOUR RESPONSE MUST BE A JSON FILE WITH THE ASSIGNED COMPLEXITY SCORE (1-10), A SHORT ONE-SENTENCE EXPLANATION OF THE SCORE, AND A LIST OF KEY FACTORS CONTRIBUTING TO THE COMPLEXITY. DO NOT PROVIDE ANY ADDITIONAL INFORMATION.

Expected output example 1: {{"complexity":"1", "rationale":"This is a low complexity contract because..."}}
Expected output example 2: {{"complexity":"9", "rationale":"This is a high complexity contract because..."}}

        '''
        return ANALYZER
    except Exception as e:
        print(e)
        return ANALYZER