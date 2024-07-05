PROMPT = f"""

Analyze the provided Solidity smart contracts and create a Mermaid graph showing how each contract interacts with others, which functions are called, and how a user's wallet would interact with the contracts. Follow these steps:

1. Identify all contracts in the provided files.
2. For each contract, identify public and external functions.
3. Analyze function bodies to detect calls to other contracts or functions.
4. Add a node representing a user's wallet.
5. Create a Mermaid graph where:
   - Each contract is represented as a box #40;node#41; containing a list of its functions
   - The user's wallet is represented as a separate box #40;node#41;
   - Edges represent function calls between contracts or from the user's wallet
   - Edge labels should include both the function name and a brief description of what calling the function does

Use the following Mermaid syntax:
graph TD
    UserWallet[User Wallet]
    ContractA[ContractA<br>- function1#40;#41;<br>- function2#40;#41;]
    ContractB[ContractB<br>- functionA#40;#41;<br>- functionB#40;#41;]
    UserWallet-->|"callFunction1#40;#41; #40;Initiates action#41;"|ContractA
    ContractA-->|"callFunctionA#40;#41; #40;Performs task#41;"|ContractB

Include all contracts, their functions, and all possible interactions.
Provide only the Mermaid code as your response, without any additional explanation.

IMPORTANT: 
1. Never use parenthesis in your response. Instead, use #40; to represent an opening parenthesis and #41; to represent a closing parenthesis.
2. Use <br> for line breaks within node labels to list functions.
3. Edge labels should include both the function name and a brief description of its action, separated by a space and enclosed in #40;#41;.

Here are the Solidity files to analyze:
\n\n
#############
\n\n

"""