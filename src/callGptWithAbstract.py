import openai
from openai import OpenAI
from datetime import datetime
from pathlib import Path
import csv


def read_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write_result(file_path):
    writer = csv.writer(file_path)
    writer.writerow(["sequence", "Result"])


def split_content_into_batches(file_path, batch_size):
    with open(file_path, 'r') as file:
        abstracts = file.read().split('\n\n\n')  # Assuming each abstract is separated by double newlines
    return [abstracts[i:i + batch_size] for i in range(0, len(abstracts), batch_size)]

client = OpenAI()

def evaluate_abstract(abstract):
    prompt = read_prompt("../resource/prompts/abstract_prompt")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": "You are a research assistant that evaluates abstracts based on specific criteria."},
            {"role": "user",
             "content": f"Evaluate the following abstract:\n\n{abstract}\n\n with {prompt}. Print Y for inclusion and N for exclusion"}
        ],
        model="gpt-4",
    )
    return chat_completion.choices[0].message.content

#Read all input files from the folder
#Change the path if a different input path contains the input file
path_str = "../resource/input/input-1/"
# Path to the file
file_path = Path(path_str)
all_files = sorted([f for f in file_path.iterdir() if f.is_file()])

#Iterate all input files
for batch_number, input_file in enumerate(all_files, start=1):
    # Splitting abstracts in each input file
    abstracts = split_content_into_batches(path_str + input_file.name, 1)
    before_run_time = datetime.now()
    formatted_timestamp = before_run_time.strftime('%m-%d-%Y %H:%M:%S')

    print(f"Evaluating Batch {batch_number}...")
    output_file = f'../resource/output/results_{batch_number}_{formatted_timestamp}.csv'

    with open(output_file, mode='w', newline='') as output_file:
        writer = csv.writer(output_file)

    # Evaluating each batch
        for i, abstract in enumerate(abstracts, start=1):
            print(formatted_timestamp)

            #call openai
            result = evaluate_abstract(abstract)
            #result = "test"
            #write the result fro openai call
            writer.writerow([(batch_number - 1) * 100 + i, result])

            print(f"{i}: {result}")
            print("\n")

        time_spent = datetime.now() - before_run_time
        print(f"Spent {time_spent} on batch {batch_number}")
