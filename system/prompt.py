PROMPT = f"""
Analyze the provided Solidity smart contracts and create a Mermaid graph showing how each contract interacts with others, which functions are called, and how a user's wallet would interact with the contracts. Follow these steps:

1. Identify all contracts in the provided files.
2. For each contract, identify public and external functions.
3. Analyze function bodies to detect calls to other contracts or functions.
4. Add a node representing a user's wallet.
5. Create a Mermaid graph where:
   - Nodes represent contracts and the user's wallet
   - Edges represent function calls between contracts, labeled with the function name
   - Edges from the user's wallet to contracts represent possible interactions (e.g., calling public functions)

Use the following Mermaid syntax:
graph TD
    UserWallet[User Wallet]
    ContractA-->|functionName#40;#41;|ContractB
    UserWallet-->|interactionName#40;#41;|ContractA

Include all possible user interactions with the contracts.
Provide only the Mermaid code as your response, without any additional explanation or comments.

IMPORTANT: Never use parenthesis in your response. Instead, use #40; to represent an opening parenthesis and #41; to represent a closing parenthesis.

Here are the Solidity files to analyze:
\n\n
#############
\n\n
"""
