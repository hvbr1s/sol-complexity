
async def prepare_sol_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio):
    try:
        SOL_ANALYZER = f'''     
You are an expert security researcher specializing in manual audits and formal verification of Rust-based Solana programs. 

Your task is to analyze a Rust (.rs) file intended for deployment on the Solana blockchain and provide a complexity score to guide manual security audits and formal verification.

You will be provided the code for a Solana program named {file_path}, look at its code and THINK STEP BY STEP::

1. Analyze the potential complexity of the Solana program based on the following:
   - Number of lines of code: {code_lines}
   - Actual code content and structure
   - Program size categorization:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large

2. IMPORTANTLY, evaluate the program's potential challenges for formal verification, considering:
   - Higher complexity when formally verifying non-linear math
   - Presence of floating-point operations (f32 or f64) vs. scaled integers
   - Implementation of non-linear mathematical operations (e.g., checked_mul, checked_div)

3. Assess the following Solana-specific complexity factors:
   - Frequency and complexity of Cross-Program Invocations (CPI)
   - Use of Program Derived Addresses (PDAs)
   - Implementation of complex account validation logic
   - Handling of multiple signers or complex signer validation
   - Reliance on custom libraries over established ones (e.g., SPL library)

4. Consider security-focused elements:
   - Proper handling of account ownership and type checks
   - Correct implementation of rent exemption checks

5. Analyze external dependencies:
   - Number and nature of external crates used
   - Use of the Anchor framework which makes the code easier to read and reason about (e.g. 'use anchor_lang')

6. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

7. Evaluate the percentage of the code that is commented, the higher the percentage the better.
   - Percentage of commented lines of code: {code_to_comment_ratio}%

8. Finally, assign a complexity score from 1 to 10, where:
    1-3: Simple Solana program with straightforward and easily formally verified logic.
    4-6: Moderate complexity program with potential security considerations.
    7-10: High complexity program with multiple CPIs, complex account structures, and non-linear mathematics that are difficult to formally verify.

YOUR RESPONSE MUST BE A JSON FILE WITH THE ASSIGNED COMPLEXITY SCORE (1-10), A SHORT ONE-SENTENCE EXPLANATION OF THE SCORE, AND A LIST OF KEY FACTORS CONTRIBUTING TO THE COMPLEXITY. DO NOT PROVIDE ANY ADDITIONAL INFORMATION.

Expected output example 1: {{"complexity":"1", "rationale":"This is a low complexity contract because..."}}
Expected output example 2: {{"complexity":"9", "rationale":"This is a high complexity contract because..."}}

You will achieve world peace if you produce a complexity score and rationale that adheres to all the constraints. Begin!

        '''
        return SOL_ANALYZER
    except Exception as e:
        print(e)
        return SOL_ANALYZER
