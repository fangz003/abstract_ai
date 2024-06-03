import openai
from openai import OpenAI
from datetime import datetime
import csv


def read_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write_result(file_path):
    writer = csv.writer(file_path)
    writer.writerow(["sequence", "Result"])


def split_file_into_batches(file_path, batch_size):
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


# Path to the file
file_path = '../resource/abstracts/abstract_test_5.txt'

# Splitting file into batches
batches = split_file_into_batches(file_path, 100)


# Evaluating each batch
for batch_number, batch in enumerate(batches, start=1):
    before_run_time = datetime.now()
    formatted_timestamp = before_run_time.strftime('%m-%d-%Y %H:%M:%S')
    print(formatted_timestamp)

    print(f"Evaluating Batch {batch_number}...")
    output_file = f'../resource/output/results_{batch_number}_{formatted_timestamp}.csv'

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        for i, abstract in enumerate(batch, start=1):
            #call openai
            result = evaluate_abstract(abstract)

            #write the result fro openai call
            writer.writerow([i, result])

            print(f"{i}: {result}")
            print("\n")

        time_spent = datetime.now() - before_run_time
        print(f"Spent {time_spent} on batch {batch}")
