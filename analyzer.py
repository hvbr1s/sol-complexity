import os
import asyncio
import aiofiles
import subprocess
from dotenv import load_dotenv
from openai import AsyncOpenAI
from system.prompts import preprare_prompt

# Load secrets
load_dotenv()

# Set up OpenAI
# Initialize OpenAI client & Embedding model
openai_key = os.environ['OPENAI_API_KEY']
openai_client = AsyncOpenAI(api_key=openai_key)
openai_model_prod = "gpt-4-turbo"
openai_model_test = "gpt-4o"

    # Function to run CLOC on a single Rust file and calculate complexity score
async def complexity_score(file_path):
    try:
        # Run CLOC on the file
        result = subprocess.run(['cloc', file_path, '--json'], capture_output=True, text=True)
        cloc_output = result.stdout

        # Parse the JSON output to get the number of lines
        import json
        cloc_data = json.loads(cloc_output)
        rust_data = cloc_data.get('Rust', {})
        
        # Calculate a simple complexity score (you can adjust this formula)
        code_lines = rust_data.get('code', 0)
        comment_lines = rust_data.get('comment', 0)
        blank_lines = rust_data.get('blank', 0)
        
        try:
            response = await openai_client.chat.completions.create(
                temperature=0.0,
                model=openai_model_test,
                messages=[
                {"role": "system", "content": await preprare_prompt(file_path, code_lines, comment_lines, blank_lines)},
                {"role": "user", "content": file_path}
                ],
                timeout= 60,
            )
            score = int(response.choices[0].message.content)
            print(f'Difficty score for {file_path} is {score}')
        except Exception as e:
            print(f"Failed to generate Mermaid code: {e}")
            return("Snap! Something went wrong, please ask your question again!")
        
        
        
        return {
            'file': os.path.basename(file_path),
            'score': round(score, 2),
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to analyze all Rust files in a folder
async def analyze_rust_programs(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.rs'):
            file_path = os.path.join(folder_path, filename)
            score = await complexity_score(file_path)
            if score:
                results.append(score)
    return results

# Function to save results to a text file
async def save_results(results, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        await f.write("Analyzed Rust Programs:\n\n")
        for result in results:
            await f.write(f"File: {result['file']}\n")
            await f.write(f"Complexity Score: {result['score']}\n")
            await f.write(f"Code Lines: {result['code_lines']}\n")
            await f.write(f"Comment Lines: {result['comment_lines']}\n")
            await f.write(f"Blank Lines: {result['blank_lines']}\n")
            await f.write("\n")

async def main():
    folder_path = './docs'  # Adjust this to your Rust files directory
    output_file = './output/analysis_results.txt'
    
    print("Analyzing Rust programs...")
    results = await analyze_rust_programs(folder_path)
    
    print("Saving results...")
    await save_results(results, output_file)
    
    print(f"Analysis complete. Results saved to {output_file}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
    
