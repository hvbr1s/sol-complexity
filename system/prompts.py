MAP = """

Create a Mermaid graph based on the provided contract analysis. Follow these steps:
1. Create a node for each unique contract, listing its public functions and their visibility.
2. Optionally, include the function modifiers (e.g., onlyOwner, requireSomething) in the node labels.
3. Create edges for function calls between contracts and from the user's wallet.
4. Focus only on the interactions between contracts, and skip internal contract function calls.
5. ALWAYS ignore interactions where the "from" and "to" contracts are the same.
6. Use the following Mermaid syntax:
    graph TD
        UserWallet[User Wallet]
        ContractA[ContractA<br>- function1#40;#41; : public<br>- function2#40;#41; : external]
        ContractB[ContractB<br>- functionA#40;#41; : public<br>- functionB#40;#41; : internal]
        UserWallet-->|"callFunction1#40;#41; -> Initiates action"|ContractA
        ContractA-->|"callFunctionA#40;#41; -> Performs task"|ContractB

Include all unique contracts, their public functions and visibility, and all possible interactions between them.
Provide ONLY the Mermaid code as your response, WITHOUT any additional explanation.
The code should start with 'graph TD' on its own line and NEVER include any ``` markers or additional explanations or comments.

IMPORTANT: 
1. Never use parenthesis in your response. Instead, use #40; to represent an opening parenthesis and #41; to represent a closing parenthesis.
2. Use <br> for line breaks within node labels to list functions and their visibility.
3. Edge labels should include the function name and a brief description preceded by a ->
4. Start with 'graph TD' on its own line.
5. Do not include any ``` markers or additional explanations.

Here is the analysis for each contract:
\n
#############
\n

"""

SIMPLIFY = '''

Simplify the following Mermaid graph code to create a user-centric transaction flow diagram for a specific user interaction. Follow these guidelines:

1. Focus on a single user interaction and the flow of that transaction through different contracts.
2. Include only the contracts and functions directly involved in the chosen user interaction.
3. Show how the user interacts with the system and how their transaction flows through the contracts.

Formatting rules:
1. Start with 'graph TD' on its own line.
2. Represent contracts as nodes with their functions listed inside.
3. Use #40; instead of ( and #41; instead of ).
4. Use <br> for line breaks within node labels to list functions and their visibility/modifiers.
5. Edge labels should include the function name followed by ' -> ' and a brief description.
6. Do not include any ``` markers or additional explanations.
7. Make sure every edge is represented in a unique color.

Node format:
ContractName[ContractName<br>- function1#40;#41; : public<br>- function2#40;#41; : external #40;onlyOwner#41;]

Edge format:
ContractA-->|"functionName#40;#41; -> Brief description"|ContractB

Example:
graph TD
    User[User]
    ContractA[ContractA<br>- deposit#40;#41; : public<br>- withdraw#40;#41; : external]
    ContractB[ContractB<br>- process#40;#41; : public]
    User-->|"deposit#40;#41; -> Adds funds"|ContractA
    ContractA-->|"process#40;#41; -> Handles transaction"|ContractB

Provide only the simplified Mermaid code as your response, adhering strictly to these guidelines.

Here is the analysis for the specific user interaction to focus on:
\n
#############
\n

'''


ANALYZE = """

Analyze the provided Solidity smart contracts and create a mapping of the transaction flow and contract interactions. Follow these steps:

1. Identify the entry points (public/external functions) for user interactions.
2. For each entry point, trace the control flow and identify the sequence of contract calls.
3. Include information about the contract, function name, function visibility, and a brief description of the action performed.
4. Represent the transaction flow and contract interactions as a JSON structure with the following format:

{
    "transactionFlow": [
        {
            "contract": "ContractName",
            "function": "functionName",
            "visibility": "public/external/internal",
            "modifiers": ["onlyOwner", "requireSomething"],
            "description": "Performs some action"
        },
        {
            "contract": "OtherContract",
            "function": "anotherFunction",
            "visibility": "public/external/internal",
            "modifiers": ["onlyAdmin"],
            "description": "Performs a supporting action"
        },
        {
            "contract": "HelperLibrary",
            "function": "helperFunction",
            "visibility": "public/external/internal",
            "description": "Provides utility functionality"
        }
    ],
    "contractInteractions": [
        {
            "from": "CallingContract",
            "to": "CalledContract",
            "via": "functionName"
        },
        {
            "from": "ContractA",
            "to": "ContractB",
            "via": "anotherFunctionName"
        }
    ],
}

Include only the essential contract interactions that are part of the main transaction flow. Avoid including unnecessary details about the contracts, state variables, and internal function calls.

Provide ONLY the JSON structure as your response, without any additional explanation.

Here are the Solidity smart contracts to analyze:
\n
#############
\n

"""
