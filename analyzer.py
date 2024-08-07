import os
import json
import asyncio
import statistics
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
openai_model_prod = "gpt-4o-2024-08-06"

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
        code_lines = str(file_info['code_lines'])

        response = await openai_client.chat.completions.create(
            temperature=0.0,
            model=openai_model_prod,
            messages=[
                {"role": "system", "content": await preprare_prompt(file_path, code_lines , file_info['comment_lines'], file_info['blank_lines'])},
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
            print (f'Program {file_path} got assigned a complexity score of {score}. {rationale}')
            return score, rationale, code_lines
        else:
            print(f"Couldn't generate complexity info for {file_path}")
            return None
    except Exception as e:
        print(f"Failed to generate complexity info for {file_path}: {e}")
        return None

# Function to analyze all Rust files
async def analyze_rust_programs():
    rust_files = await get_rust_files_info()
    results = []
    
    for file_path, file_info in rust_files.items():
        score, rationale, code_lines = await get_complexity_score(file_path, file_info)
        if score is not None:
            results.append({
                'file': file_path,
                'score': score,
                'rationale': rationale,
                'cloc': code_lines
            })
    
    return results

# Function to save results to a json file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        json_data = {"complexity_report": results}
        await f.write(json.dumps(json_data, indent=2))

# Function to calculate summary statistics
def calculate_summary(results):
    total_cloc = sum(int(result['cloc']) for result in results)
    complexity_scores = [float(result['score']) for result in results]
    avg_complexity = statistics.mean(complexity_scores)
    median_complexity = statistics.median(complexity_scores)
    return total_cloc, avg_complexity, median_complexity

# Function to save summary to a txt file
async def save_summary(total_cloc, avg_complexity, median_complexity, output_file):
    
    summary = f"""Project Summary:
Total CLOC: {total_cloc}
Average Complexity Score: {avg_complexity:.2f}
Median Complexity Score: {median_complexity:.2f}
"""
    async with aiofiles.open(output_file, 'w') as f:
        await f.write(summary)

async def main():
    complexity_report_file = './output/complexity_report.json'
    summary_file = './output/project_summary.txt'
    
    print("Analyzing Rust programs...")
    results = await analyze_rust_programs()
    
    print("Saving complexity report...")
    await save_results(results, complexity_report_file)
    
    print("Calculating summary statistics...")
    total_cloc, avg_complexity, median_complexity = calculate_summary(results)
    
    print("Saving project summary...")
    await save_summary(total_cloc, avg_complexity, median_complexity, summary_file)
    
    print(f"Analysis complete. Complexity report saved to {complexity_report_file}")
    print(f"Project summary saved to {summary_file}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())