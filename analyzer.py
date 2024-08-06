import os
import re
import json
import asyncio
import aiofiles
import subprocess
from dotenv import load_dotenv
from openai import AsyncOpenAI
from system.prompts import preprare_prompt

# Load secrets
load_dotenv()

# Set up OpenAI
openai_key = os.environ['OPENAI_API_KEY']
openai_client = AsyncOpenAI(api_key=openai_key)
openai_model_prod = "gpt-4-turbo"
openai_model_test = "gpt-4o"

# Function to run CLOC on 'docs' directories and get Rust file information
def get_rust_files_info():
    result = subprocess.run(['cloc', './docs', '--json', '--include-lang=Rust', '--by-file'], capture_output=True, text=True)
    cloc_output = json.loads(result.stdout)
    print(cloc_output)
    
    rust_files = {}
    for file_path, file_info in cloc_output.items():
        if file_path != 'header' and file_path != 'SUM':
            rust_files[file_path] = {
                "file_name": file_path,
                "code_lines": file_info.get('code', 0),
                "comment_lines": file_info.get('comment', 0),
                "blank_lines": file_info.get('blank', 0)
            }
    
    return rust_files

# Function to run the bot on a file and get the complexity score
async def get_complexity_score(file_path, file_info):
    try:
        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_test,
            messages=[
                {"role": "system", "content": await preprare_prompt(file_path, file_info['code_lines'], file_info['comment_lines'], file_info['blank_lines'])},
                {"role": "user", "content": file_path}
            ],
            timeout=60,
        )
        content = response.choices[0].message.content
        print(content)
        
        # Extract the score using regex
        match = re.search(r'Complexity Score:\s*(\d+)', content)
        if match:
            score = int(match.group(1))
            print(f'Difficulty score for {file_path} is {score}')
            return score
        else:
            print(f"Couldn't extract complexity score for {file_path}")
            return None
    except Exception as e:
        print(f"Failed to generate complexity score for {file_path}: {e}")
        return None

# Function to analyze all Rust files
async def analyze_rust_programs():
    rust_files = get_rust_files_info()
    results = []
    
    for file_path, file_info in rust_files.items():
        score = await get_complexity_score(file_path, file_info)
        if score is not None:
            results.append({
                'file': file_path,
                'score': score
            })
    
    return results

# Function to save results to a text file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        await f.write("Complexity Report:\n\n")
        for result in results:
            await f.write(f"File: {result['file']}, Complexity Score: {result['score']}\n")

async def main():
    output_file = './output/complexity_report.txt'
    
    print("Analyzing Rust programs...")
    results = await analyze_rust_programs()
    
    print("Saving results...")
    await save_results(results, output_file)
    
    print(f"Analysis complete. Results saved to {output_file}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())