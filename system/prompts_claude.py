MAP = """

You are tasked with creating a Mermaid graph based on a provided contract analysis. This graph will visualize the relationships between contracts, their functions, and interactions.

<contract_analysis>
{{CONTRACT_ANALYSIS}}
</contract_analysis>

Follow these steps to create the Mermaid graph:

1. Identify all unique contracts mentioned in the analysis.
2. For each contract, create a node that lists ALL of its functions and their visibility.
3. Identify all function calls between contracts and from the user's wallet.
4. Create edges to represent these function calls.
5. Ignore any interactions where the "from" and "to" contracts are the same.

Use the following Mermaid syntax:

graph TD
    UserWallet[User Wallet]
    ContractA[ContractA<br>- function1#40;#41; : public<br>- function2#40;#41; : external]
    ContractB[ContractB<br>- functionA#40;#41; : public<br>- functionB#40;#41; : internal]
    UserWallet-->|"callFunction1#40;#41; -> Initiates action"|ContractA
    ContractA-->|"callFunctionA#40;#41; -> Performs task"|ContractB

Important rules to follow:
1. Never use parenthesis in your response. Instead, use #40; to represent an opening parenthesis and #41; to represent a closing parenthesis.
2. Use <br> for line breaks within node labels to list ALL the functions and their visibility.
3. Edge labels should include the function name and a brief description preceded by a ->
4. Start with 'graph TD' on its own line.
5. Include all unique contracts, their functions and visibility, and all possible interactions between them.

Provide ONLY the Mermaid code as your response, without any additional explanation or markdown formatting. Do not include any ``` markers or explanations outside of the Mermaid syntax.

"""

SIMPLIFY = '''

SYou are tasked with analyzing Mermaid code that represents the mapping of possible interactions and calls between multiple smart contracts. Your goal is to provide a written summary of what the contracts are doing and describe a common example of a user transaction while interacting with these contracts.

Here is the Mermaid code to analyze:

<mermaid_code>
{{MERMAID_CODE}}
</mermaid_code>

Please follow these steps:

1. Carefully examine the Mermaid code and identify all the smart contracts represented in the diagram.

2. Analyze the interactions and calls between the contracts, paying attention to the direction of arrows and any labels on the connections.

3. In your mind, create a clear picture of how these contracts work together and what their main purposes are.

4. Prepare a summary of what the contracts are doing. This should include:
   - The names of the main contracts
   - The primary function of each contract
   - How the contracts interact with each other
   - Any notable features or patterns in the contract ecosystem

5. Think of a common example of how a user might interact with this system of contracts. Consider:
   - What action might a user typically want to perform?
   - Which contract would they interact with first?
   - How would their action propagate through the system?
   - What would be the end result of their transaction?

6. Provide your analysis in the following format:

<contract_summary>
[Your summary of what the contracts are doing, based on your analysis of the Mermaid code]
</contract_summary>

<user_transaction_example>
[Your description of a common example of a user transaction interacting with the contracts]
</user_transaction_example>

Remember to be clear and concise in your explanations, avoiding technical jargon where possible. Your goal is to provide a comprehensible overview of the smart contract system and how it might be used in practice.

'''


ANALYZE = '''

You will be analyzing Solidity smart contracts to create a mapping of the transaction flow and contract interactions. Here are the Solidity smart contracts to analyze:

<solidity_contracts>
{{SOLIDITY_CONTRACTS}}
</solidity_contracts>

Your task is to follow these steps:

1. Identify the entry points (public/external functions) for user interactions.
2. For each entry point, trace the control flow and identify the sequence of contract calls.
3. Include information about the contract, function name, function visibility, and a brief description of the action performed.
4. Represent the transaction flow and contract interactions as a JSON structure.

Analyze the provided Solidity smart contracts carefully. Pay attention to function declarations, their visibility (public, external, internal), and any modifiers they may have. Also, look for interactions between contracts through function calls or imports.

Create a JSON structure with the following format to represent the transaction flow and contract interactions:

{
    "transactionFlow": [
        {
            "contract": "ContractName",
            "function": "functionName",
            "visibility": "public/external/internal",
            "modifiers": ["modifier1", "modifier2"],
            "description": "Brief description of the action performed"
        },
        // Add more entries as needed
    ],
    "contractInteractions": [
        {
            "from": "CallingContract",
            "to": "CalledContract",
            "via": "functionName"
        },
        // Add more entries as needed
    ]
}

Include only the essential contract interactions that are part of the main transaction flow. Avoid including unnecessary details about the contracts, state variables, and internal function calls.

Provide ONLY the JSON structure as your response, without any additional explanation. Ensure that your JSON is properly formatted and valid.

'''

