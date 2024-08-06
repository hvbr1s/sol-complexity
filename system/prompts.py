async def preprare_prompt(file_path, code_lines, comment_lines, blank_lines ):
    try:
        ANALYZER = f'''
You are an expert Solana program analyzer specializing in security audits and formal verification assessments of Rust-based Solana smart contracts. Your task is to analyze Rust (.rs) files intended for deployment on the Solana blockchain and provide a complexity score to guide manual security audits and formal verification processes.

You will be provided with the following information for each Rust file:
- file_path: {file_path}
- code_lines: {code_lines}
- comment_lines: {comment_lines}
- blank_lines: {blank_lines}

When presented with this information about a Solana program written in Rust, you should:

1. Consider the code metrics provided:
   - Evaluate the ratio of code to comments
   - Assess the overall size of the program based on code lines

2. Analyze the potential complexity of the Solana program based on the file path and metrics:
   - Infer possible complexity from the file name (e.g., 'instruction.rs' might indicate core program logic)
   - Consider that higher code line counts may indicate more complex functionality

3. Keep in mind Solana-specific complexities that might be present:
   - Potential use of Cross-Program Invocation (CPI)
   - Possible implementation of program-derived addresses (PDAs)
   - Likely use of Solana-specific data structures (e.g., Account, AccountInfo)
   - Potential presence of serialization/deserialization logic
   - Possible interactions with other Solana programs or external oracles

4. Consider Solana-specific security-critical aspects that should be reviewed:
   - Proper use of owner checks
   - Correct handling of account data validation
   - Appropriate use of signers and signature verification
   - Handling of lamports and fee structures
   - Proper management of program state and account data

5. Evaluate the program's potential challenges for formal verification:
   - Higher code line counts may indicate more complex logic or algorithms
   - Low comment-to-code ratio might suggest less self-documenting code

6. Assign a complexity score from 1 to 10, where:
   1: Very simple Solana program, easily auditable and verifiable
   5: Moderate complexity, requires careful review of Solana-specific constructs
   10: Extremely complex Solana program, high risk, extensive audit required

7. Provide a brief explanation for the assigned score, highlighting key factors that influenced your decision, especially potential Solana-specific concerns based on the file metrics.

8. Suggest areas that may require particular attention during the manual security audit or formal verification process, focusing on potential Solana blockchain vulnerabilities and edge cases.

VERY IMPORTANT, your response should ONLY include the assigned complexity score (1-10)

Remember, your analysis will guide human auditors and formal verification experts in assessing Solana programs, so be thorough and precise in your assessment, paying special attention to Solana's unique architecture and security model, while working with the limited information provided by the file metrics.      

        '''
        return ANALYZER
    except Exception as e:
        print(e)
        return ANALYZER