import os
import asyncio
from dotenv import main
from anthropic import AsyncAnthropic
from system.prompt import PROMPT
from groq import Groq

# Load secrets
main.load_dotenv()

# Function to read all .sol files from the /doc folder
def read_solidity_files(folder_path):
    context = ""
    file_number = 1
    for filename in os.listdir(folder_path):
        if filename.endswith('.sol'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                context += f"Contract number {file_number}: {filename}\n\n"
                context += file.read()
                context += "\n"
                context += "###################\n\n"
                file_number += 1
    print(context)
    return context

# Create the context
folder_path = '/Users/danieljaheny/Documents/dev/contract-mapper/docs'
solidity_context = read_solidity_files(folder_path)

# Combine the prompt and context
full_prompt = PROMPT + solidity_context

##### CLAUDE RESEARCH

# Set up the Anthropic client
anthropic_client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Set up worker function
async def claude_research(contracts, prompt):

    response = await anthropic_client.messages.create(
                    max_tokens=2048,
                    model="claude-3-5-sonnet-20240620",
                    system=prompt,
                    temperature=0.0,
                    messages=[
                        {"role": "user", "content": contracts}
                    ]
    )
    claude_says =  response.content[0].text
    return claude_says

# Call function
async def main():
    # Assuming you have solidity_context and full_prompt defined earlier in your code
    claude_says = await claude_research(contracts=solidity_context, prompt=full_prompt)
    
    if claude_says:
        # Print Claude-generated graph
        print(f"{claude_says}\n\n")
    else:
        print("Failed to get a response from Claude.")

# Run the async main function
asyncio.run(main())

##### GROQ RESEARCH

# groq_client =  Groq(api_key=os.environ['GROQ_API_KEY'])
# response_groq = groq_client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",
#             "content": PROMPT
#         },
#         {
#             "role": "user",
#             "content": solidity_context
#         }
#     ],
#     model="llama3-70b-8192",
#     temperature = 0.0,
# )
# # Print Groq-generated graph
# groq_says = response_groq.choices[0].message.content
# print(f"{groq_says}\n\n")

