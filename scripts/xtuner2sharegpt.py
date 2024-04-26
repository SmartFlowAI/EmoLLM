import json

# Given JSON data in string format
# original_json_data = """
# [
#     {
#         "conversation": [
#             {"system": "system", "input": "input", "output": "output"},
#             {"input": "input", "output": "output"},
#             {"input": "input", "output": "output"}
#         ]
#     },
#     {
#         "conversation": [
#             {"system": "system", "input": "input", "output": "output"},
#             {"input": "input", "output": "output"},
#             {"input": "input", "output": "output"}
#         ]
#     }
# ]
# """

# Parse the original JSON data into Python objects
def convert_xtuner_to_sharegpt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Initialize a new list to hold transformed conversations
    transformed_conversations = []

    for conversation_group in data:
        system = conversation_group["conversation"][0]["system"]

        # Extract human and GPT inputs and outputs from each conversation pair
        transformed_pairs = []
        for pair in conversation_group["conversation"]:
            # if "system" in pair:
            #     continue  # Skip the initial system entry

            transformed_pairs.append({"from": "human", "value": pair["input"]})
            transformed_pairs.append({"from": "gpt", "value": pair["output"]})
        # print(transformed_pairs)
        # Add the transformed conversation group to the result list
        transformed_conversation = {
            "conversations": transformed_pairs,
            "system": system,
        }
        transformed_conversations.append(transformed_conversation)

    # Convert the transformed Python objects back into JSON format
    with open(output_path, "w", encoding='utf-8') as output_file:
        json.dump(transformed_conversations, output_file, ensure_ascii=False, indent=4)
        

if __name__ == "__main__":
    input_path = "../datasets/scientist.json"
    output_path = "../datasets/scientist_sharegpt.json"
    convert_xtuner_to_sharegpt(input_path, output_path)
    