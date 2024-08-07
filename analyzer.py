import os
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
openai_model_test = "gpt-4o-2024-08-06"

# Function to run CLOC on 'docs' directories and get Rust file information
async def get_rust_files_info():
    result = subprocess.run(['cloc', './docs', '--json', '--include-lang=Rust', '--by-file'], capture_output=True, text=True)
    cloc_output = json.loads(result.stdout)
    
    rust_files = {}
    for file_path, file_info in cloc_output.items():
        if file_path != 'header' and file_path != 'SUM':
            
            # Read the file content
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")
                file_content = ""
            
            rust_files[file_path] = {
                "file_name": file_path,
                "code_lines": file_info.get('code', 0),
                "comment_lines": file_info.get('comment', 0),
                "blank_lines": file_info.get('blank', 0),
                "file_content": file_content
            }
    
    return rust_files

# Function to run the bot on a file and get the complexity score
async def get_complexity_score(file_path, file_info):
    try:
        rust_program = file_info['file_content']

        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_test,
            messages=[
                {"role": "system", "content": await preprare_prompt(file_path, file_info['code_lines'], file_info['comment_lines'], file_info['blank_lines'])},
                {"role": "user", "content": rust_program}
            ],
            response_format= { "type": "json_object" },
            timeout=60,
        )
        content = response.choices[0].message.content
        parsed_content = json.loads(content)
        score = parsed_content["complexity"]
        rationale = parsed_content["rationale"]
        
        if score and rationale:
            print (f'Program {file_path} got assigned a complexity scrore of {score} because: {rationale}')
            return score, rationale
        else:
            print(f"Couldn't extract complexity score for {file_path}")
            return None
    except Exception as e:
        print(f"Failed to generate complexity score for {file_path}: {e}")
        return None

# Function to analyze all Rust files
async def analyze_rust_programs():
    rust_files = await get_rust_files_info()
    results = []
    
    for file_path, file_info in rust_files.items():
        score, rationale = await get_complexity_score(file_path, file_info)
        if score is not None:
            results.append({
                'file': file_path,
                'score': score,
                'rationale': rationale
            })
    
    return results

# Function to save results to a json file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        json_data = {"complexity_report": results}
        await f.write(json.dumps(json_data, indent=2))

async def main():
    output_file = './output/complexity_report.json'
    
    print("Analyzing Rust programs...")
    results = await analyze_rust_programs()
    
    print("Saving results...")
    await save_results(results, output_file)
    
    print(f"Analysis complete. Results saved to {output_file}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
