import os
import asyncio
import shutil
from dotenv import main
from anthropic import AsyncAnthropic
from system.prompts import MAP, SIMPLIFY, ANALYZE
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
    return context

# Function to move files to output directory
def move_files_to_output():
    output_dir = './output'
    files_to_move = ['complete_mermaid.mmd', 'complete_mermaid_graph.png', 
                     'simplified_mermaid.mmd', 'simplified_mermaid_graph.png']
    
    for file in files_to_move:
        if os.path.exists(file):
            shutil.move(file, os.path.join(output_dir, file))
        else:
            print(f"Warning: {file} not found")
    print(f"Moved files to {output_dir}📮📮")
            

# Create the context
folder_path = './docs'
solidity_context = read_solidity_files(folder_path)

# Set up the Anthropic client
anthropic_client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
prod_claude_llm = "claude-3-5-sonnet-20240620"
test_claude_llm_sonnet = "claude-3-sonnet-20240229"
test_claude_llm_opus= "claude-3-opus-20240229"


# Set up worker function
async def generate_mermaid(contracts):
    print("Generating Mermaid code 🧜‍♀️🧜‍♀️")
    response = await anthropic_client.messages.create(
                    max_tokens=2048,
                    model=test_claude_llm_opus,
                    system=MAP,
                    temperature=0.0,
                    messages=[
                        {"role": "user", "content": contracts}
                    ]
    )
    return response.content[0].text

async def analyze_contracts(contracts):
    print("Analyzing your files, sit tight 🔧🔧")     
    response = await anthropic_client.messages.create(
        max_tokens=2048,
        model=test_claude_llm_opus,
        system=ANALYZE,
        temperature=0.0,
        messages=[
            {"role": "user", "content": contracts}
        ]
    )
    return response.content[0].text

async def simplify_mermaid(mermaid_code):    
    response = await anthropic_client.messages.create(
                    max_tokens=2048,
                    model=test_claude_llm_opus,
                    system=SIMPLIFY,
                    temperature=0.0,
                    messages=[
                        {"role": "user", "content": mermaid_code}
                    ]
    )
    return response.content[0].text.strip()

async def generate_mermaid_image(mermaid_code, output_file):
    print("Generating graph 🗺️")
    cleaned_code = clean_mermaid_code(mermaid_code)
    
    # Add Mermaid configuration
    mermaid_code = f"""%%{{init: {{'theme': 'default'}}}}%%
{cleaned_code}"""
    
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
            # '-s', '2',
            '--backgroundColor', 'white',
        ], check=True, capture_output=True, text=True)
        print(f"High-resolution Mermaid graph image saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating Mermaid image: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        print("Problematic Mermaid code:")
    
    # Clean up the temporary file
    os.remove(temp_file)

async def save_mermaid_code(mermaid_code, filename):
    cleaned_code = clean_mermaid_code(mermaid_code)
    async with aiofiles.open(filename, mode='w') as f:
        await f.write(cleaned_code)
    print(f"Mermaid code saved to {filename}")

def clean_mermaid_code(mermaid_code):
    # Remove any leading/trailing whitespace and backticks
    cleaned_code = mermaid_code.strip().strip('`')
    
    # Ensure the code starts with 'graph TD'
    if not cleaned_code.startswith('graph TD'):
        cleaned_code = 'graph TD\n' + cleaned_code
    
    # Remove any lines that contain complex type definitions
    cleaned_lines = [line for line in cleaned_code.split('\n') if '[]' not in line]
    
    return '\n'.join(cleaned_lines)

async def main():
    # First call: Analyze contracts
    contract_analysis = await analyze_contracts(solidity_context)
    print("Done analyzing your files 🫡🫡")
    
    # Second call: Generate initial Mermaid graph
    initial_mermaid = await generate_mermaid(contract_analysis)
    
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
    
    # Move all generated files to the output directory
    move_files_to_output()

# Run the async main function
asyncio.run(main())
