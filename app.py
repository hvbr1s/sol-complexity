import os
import asyncio
from dotenv import main
from anthropic import AsyncAnthropic
from system.prompts import PROMPT, SIMPLIFY
from groq import Groq
import aiofiles
import subprocess

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

async def simplify_mermaid(mermaid_code):    
    response = await anthropic_client.messages.create(
                    max_tokens=2048,
                    model="claude-3-sonnet-20240229",
                    system=SIMPLIFY,
                    temperature=0.0,
                    messages=[
                        {"role": "user", "content": mermaid_code}
                    ]
    )
    return response.content[0].text.strip()

async def generate_mermaid_image(mermaid_code, output_file):
    # Remove any leading/trailing whitespace and backticks
    mermaid_code = mermaid_code.strip().strip('`')
    
    # Add Mermaid configuration
    mermaid_code = f"""%%{{init: {{'theme': 'default'}}}}%%
{mermaid_code}"""
    
    # Save Mermaid code to a temporary file with .mmd extension
    temp_file = 'temp_mermaid.mmd'
    async with aiofiles.open(temp_file, mode='w') as f:
        await f.write(mermaid_code)
    
    try:
        subprocess.run([
            'mmdc',
            '-i', temp_file,
            '-o', output_file,
            '-w', '2048',
            '-H', '2048',
            '-s', '2',
            '--backgroundColor', 'white'
        ], check=True, capture_output=True, text=True)
        print(f"High-resolution Mermaid graph image saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating Mermaid image: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
    
    # Clean up the temporary file
    os.remove(temp_file)

async def save_mermaid_code(mermaid_code, filename):
    async with aiofiles.open(filename, mode='w') as f:
        await f.write(mermaid_code)
    print(f"Mermaid code saved to {filename}")

async def main():
    # Generate initial Mermaid code
    full_prompt = PROMPT + solidity_context
    initial_mermaid = await claude_research(contracts=solidity_context, prompt=full_prompt)
    
    if initial_mermaid:
        print("Initial Mermaid Code:")
        print(f"{initial_mermaid}\n\n")
        
        # Save and generate image for initial Mermaid code
        await save_mermaid_code(initial_mermaid, 'complete_mermaid.mmd')
        await generate_mermaid_image(initial_mermaid, 'complete_mermaid_graph.png')
        
        # Simplify the Mermaid code
        simplified_mermaid = await simplify_mermaid(initial_mermaid)
        
        if simplified_mermaid:
            print("Simplified Mermaid Code:")
            print(f"{simplified_mermaid}\n\n")
            
            # Save and generate image for simplified Mermaid code
            await save_mermaid_code(simplified_mermaid, 'simplified_mermaid.mmd')
            await generate_mermaid_image(simplified_mermaid, 'simplified_mermaid_graph.png')
        else:
            print("Failed to simplify the Mermaid code.")
    else:
        print("Failed to generate initial Mermaid code.")

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

