MAP = """

Create a Mermaid graph based on the provided contract analysis. Follow these steps:
1. Create a node for each contract, listing its functions.
2. If a user interaction is present, add a node representing the user.
3. Create edges for function calls between contracts and from the user's wallet.
4. Use the following Mermaid syntax:
    graph TD
        UserWallet[User Wallet]
        ContractA[ContractA<br>- function1#40;#41;<br>- function2#40;#41;]
        ContractB[ContractB<br>- functionA#40;#41;<br>- functionB#40;#41;]
        UserWallet-->|"callFunction1#40;#41; -> Initiates action"|ContractA
        ContractA-->|"callFunctionA#40;#41; -> Performs task"|ContractB

Include all contracts, their functions, and all possible interactions.
Provide ONLY the Mermaid code as your response, WITHOUT any additional explanation.
The code should start with 'graph TD' on its own line and NEVER include any ``` markers or additional explanations or comments.

IMPORTANT: 
1. Never use parenthesis in your response. Instead, use #40; to represent an opening parenthesis and #41; to represent a closing parenthesis.
2. Use <br> for line breaks within node labels to list functions.
3. Edge labels should include the function name and a brief description preceded by a ->
4. Start with 'graph TD' on its own line.
5. Do not include any ``` markers or additional explanations.

Here are the Solidity files to analyze:
\n\n
#############
\n\n

"""

SIMPLIFY = '''

Simplify the following Mermaid graph code to create a user-centric transaction flow diagram. Follow these guidelines:

1. Focus on user interactions and the journey of a transaction through different contracts.
2. Include only contracts and functions directly involved in user transactions.
3. Show how users interact with the system and how their transactions flow through the contracts.

Formatting rules:
1. Start with 'graph TD' on its own line.
2. Represent contracts as nodes with their functions listed inside.
3. Use #40; instead of ( and #41; instead of ).
4. Use <br> for line breaks within node labels to list functions.
5. Edge labels should include the function name followed by ' -> ' and a brief description.
6. Do not include any ``` markers or additional explanations.

Node format:
ContractName[ContractName<br>- function1#40;#41;<br>- function2#40;#41;]

Edge format:
ContractA-->|"functionName#40;#41; -> Brief description"|ContractB

Example:
graph TD
    User[User]
    ContractA[ContractA<br>- deposit#40;#41;<br>- withdraw#40;#41;]
    ContractB[ContractB<br>- process#40;#41;]
    User-->|"deposit#40;#41; -> Adds funds"|ContractA
    ContractA-->|"process#40;#41; -> Handles transaction"|ContractB

Provide only the simplified Mermaid code as your response, adhering strictly to these guidelines.

'''


ANALYZE = """

Analyze the provided Solidity smart contracts. Follow these steps:
1. Identify all contracts in the provided files.
2. For each contract, identify public and external functions.
3. Analyze function bodies to detect calls to other contracts or functions.
4. Identify inheritance relationships between contracts.
5. Detect state variables that reference other contracts.

Provide your response as a JSON structure with the following format:
{
    "contracts": [
        {
            "name": "ContractName",
            "inheritsFrom": ["ParentContract1", "ParentContract2"],
            "stateVariables": [
                {
                    "name": "variableName",
                    "type": "ContractType",
                    "visibility": "public/private/internal"
                }
            ],
            "functions": [
                {
                    "name": "functionName",
                    "visibility": "public/external",
                    "calls": [
                        {
                            "contract": "OtherContract",
                            "function": "someFunction"
                        }
                    ],
                    "modifies": [
                        {
                            "contract": "SomeContract",
                            "stateVariable": "variableName"
                        }
                    ]
                }
            ]
        }
    ],
    "relationships": [
        {
            "type": "inheritance",
            "from": "ChildContract",
            "to": "ParentContract"
        },
        {
            "type": "composition",
            "from": "ContainerContract",
            "to": "ContainedContract",
            "via": "stateVariableName"
        },
        {
            "type": "interaction",
            "from": "CallingContract",
            "to": "CalledContract",
            "via": "functionName"
        }
    ]
}

Include all contracts and their relevant functions, state variables, and relationships. Do not include any explanation, only the JSON structure.

Here are the Solidity smart contracts to analyze:
\n
#############
\n

"""
