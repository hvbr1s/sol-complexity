import os
import re
import asyncio
import shutil
from dotenv import main
from openai import AsyncOpenAI
from system.prompts import MAP, SIMPLIFY, ANALYZE, FIND_BUGS
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
                content = file.read()
                context += f"Contract number {file_number}: {filename}\n\n"
                context += content.strip()  # Remove leading/trailing whitespace
                context += "\n"
                context += "###################\n\n"
                file_number += 1
    return context

# Function to move files to output directory
def move_files_to_output():
    output_dir = './output'
    files_to_move = ['complete_mermaid.mmd', 'complete_mermaid_graph.png']
    
    for file in files_to_move:
        if os.path.exists(file):
            shutil.move(file, os.path.join(output_dir, file))
        else:
            print(f"Warning: {file} not found")
    print(f"Moved files to {output_dir}📮📮")
            

# Create the context
folder_path = './docs'
solidity_context = read_solidity_files(folder_path)

# Initialize OpenAI client & Embedding model
openai_key = os.environ['OPENAI_API_KEY']
openai_client = AsyncOpenAI(api_key=openai_key)
openai_model_prod = "gpt-4-turbo"
openai_model_test = "gpt-4o"

async def analyze_contracts(solidity_context):
    print("Analyzing your files, sit tight 🔧🔧")
    try:     
        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_test,
            messages=[
            {"role": "system", "content":ANALYZE},
            {"role": "user", "content": solidity_context}
            ],
            timeout= 100,
            response_format={ "type": "json_object" }
        )
    except Exception as e:
        print(f"Failed to analyze the code: {e}")
        return("Snap! Something went wrong, please ask your question again!")
    
    return response.choices[0].message.content

async def generate_mermaid(contract_analysis):
    print("Generating Mermaid code 🧜‍♀️🧜‍♀️")
    try:
        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_test,
            messages=[
            {"role": "system", "content":MAP},
            {"role": "user", "content": contract_analysis}
            ],
            timeout= 60,
        )
    except Exception as e:
        print(f"Failed to generate Mermaid code: {e}")
        return("Snap! Something went wrong, please ask your question again!")
    return response.choices[0].message.content

async def simplify_mermaid(mermaid_code):
    try:    
        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_test,
            messages=[
            {"role": "system", "content":SIMPLIFY},
            {"role": "user", "content": mermaid_code}
            ],
            timeout= 30,
        )
    except Exception as e:
        print(f"Failed to simplify the mapping: {e}")
        return("Snap! Something went wrong, please ask your question again!")
    return response.choices[0].message.content

async def generate_mermaid_image(mermaid_code, output_file):
    print("Generating graph 🗺️")
    cleaned_code = await clean_mermaid_code(mermaid_code)
    
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
            '-s', '2',
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

async def save_mermaid_code(mermaid_code, filename):
    cleaned_code = await clean_mermaid_code(mermaid_code)
    with open(filename, 'w') as f:
        f.write(cleaned_code)
    print(f"Mermaid code saved to {filename}")

async def clean_mermaid_code(mermaid_code):
    # Remove any leading/trailing whitespace and backticks
    cleaned_code = mermaid_code.strip().strip('`')
    
    # Ensure the code starts with 'graph TD'
    if not cleaned_code.startswith('graph TD'):
        cleaned_code = 'graph TD\n' + cleaned_code
    
    # Remove any lines that contain complex type definitions
    cleaned_lines = [line for line in cleaned_code.split('\n') if '[]' not in line]
    
    return '\n'.join(cleaned_lines)

async def find_bugs(contract_analysis):
    print("Looking for bugs 🪲👀")
    try:
        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_test,
            messages=[
            {"role": "system", "content":FIND_BUGS},
            {"role": "user", "content": contract_analysis}
            ],
            timeout= 100,
        )
    except Exception as e:
        print(f"Failed to generate security report: {e}")
        return("Snap! ailed to generate security report!")
    return response.choices[0].message.content

async def main():
    # First call: Analyze contracts
    contract_analysis = await analyze_contracts(solidity_context)
    print("Done analyzing your files 🫡🫡")
    print(contract_analysis)
    
    # Second call: Generate initial Mermaid graph
    initial_mermaid = await generate_mermaid(contract_analysis)
    
    if initial_mermaid:
        print("Initial Mermaid Code:")
        print(f"{initial_mermaid}\n\n")
        
        # Save and generate image for initial Mermaid code
        await save_mermaid_code(initial_mermaid, 'complete_mermaid.mmd')
        await generate_mermaid_image(initial_mermaid, 'complete_mermaid_graph.png')
        
        # Provide code summary
        print('Writing an explanation 📜')
        summary = await simplify_mermaid(solidity_context)
        
        if summary:
            print("Simplified Mermaid Code:")
            print(f"{summary}\n\n")
            
                        
            # Define the full path for the file
            output_dir = "./output"
            filename_mermaid = os.path.join(output_dir, "summary.md")
            
            # Write the content to the file in Markdown format
            with open(filename_mermaid, 'w') as f:
                f.write(summary)
            
            print(f"Summary saved to {filename_mermaid}")
            
            bugs  = await find_bugs(solidity_context)
            filename_bug = os.path.join(output_dir, "bug_report.md")
            with open(filename_bug, 'w') as fil:
                fil.write(bugs)
            print(filename_bug)
            
        else:
            print("Failed to simplify the Mermaid code.")
    else:
        print("Failed to generate initial Mermaid code.")
    
    # Move all generated files to the output directory
    move_files_to_output()

# Run the async main function
asyncio.run(main())
