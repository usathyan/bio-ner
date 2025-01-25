import sys
import json
import argparse
import os
import importlib.util

import scispacy
import spacy
from spacy import displacy
from markitdown import MarkItDown

def convert_to_markdown(file_path):
    md = MarkItDown()
    return md.convert(file_path).text_content

def process_text(text, nlp, model_name):
    doc = nlp(text)
    entities = []
    sentences = []
    for ent in doc.ents:
        entities.append({
            "name": ent.text,
            "type": ent.label_,
        })
    for sent in doc.sents:
        sentences.append(str(sent))
    return {
        "model": model_name,
        "entities": entities,
        "sentences": sentences
    }

def save_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Process a document using bio-NER", add_help=False)
    parser.add_argument("input_file", help="Path to the input document", nargs='?')
    parser.add_argument("output_file", help="Path to save the JSON output (optional)", nargs='?', default='entities.txt')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    args = parser.parse_args()

    if not args.input_file:
        print("Error: input_file is required.")
        parser.print_help()
        sys.exit(1)

    print("Converting {args.input_file} to markdown...")
    markdown_text = convert_to_markdown(args.input_file)
    print(f"Markdown text: {markdown_text}")

    # See more details here - https://allenai.github.io/scispacy/
    # Each model can pull in a different set of entities
    # models = [
    #     "en_core_sci_sm", "en_core_sci_md", "en_core_sci_lg",
    #     "en_ner_craft_md", "en_ner_jnlpba_md",
    #     "en_ner_bc5cdr_md", "en_ner_bionlp13cg_md"
    # ]
    
    models = [
        "en_ner_bionlp13cg_md",
        "en_ner_bc5cdr_md",
        "en_ner_jnlpba_md",
        "en_ner_craft_md",
    ]

    results = []

    for model_name in models:
        print(f"Loading model {model_name}...")
        try:
            if not spacy.util.is_package(model_name):
                print(f"Downloading model {model_name}...")
                spacy.cli.download(model_name)
            nlp = spacy.load(model_name)
            print(f"Model {model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            continue

        print(f"Processing text with {model_name}...")
        model_results = process_text(markdown_text, nlp, model_name)
        results.append(model_results)

    print("Saving results...")
    save_json(results, args.output_file)

    print("Entities by model:")
    for model_result in results:
        print(f"\nModel: {model_result['model']}")
        for entity in model_result["entities"]:
            print(f"  {entity['name']} ({entity['type']})")

        print(f"Number of sentences: {len(model_result['sentences'])}")

    print(f"Results saved to {args.output_file}")
    print("Script completed")

if __name__ == "__main__":
    main()
