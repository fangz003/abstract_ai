
file_path = "../resource/input/abstract-LewyORPark-set.txt"


def split_file_into_batches(file_path, batch_size):
    with open(file_path, 'r') as file:
        abstracts = file.read().split('\n\n\n')  # Assuming each abstract is separated by double newlines
    return [abstracts[i:i + batch_size] for i in range(0, len(abstracts), batch_size)]


batches = split_file_into_batches(file_path, 100)


for batch_number, batch in enumerate(batches, start=1):
    print(f"Split into file {batch_number}...")
    output_file = f'../resource/input/input-100/input-{batch_number}.txt'

    with open(output_file, mode='w', newline='') as file:
        for i, abstract in enumerate(batch, start=1):
            file.write(abstract)
            file.write("\n\n\n")
