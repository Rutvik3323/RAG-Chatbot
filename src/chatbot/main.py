#!/usr/bin/env python
import sys
import warnings
import json
from datetime import datetime
from pathlib import Path

from crew import RAGChatbot
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """

    Starts the RAG chatbot in interactive mode.

    Steps:
    1. Indexes documents into the vector store (Qdrant).
    2. Continuously takes user input as queries.
    3. Uses agents and tasks to retrieve relevant info and generate a response.
    4. Optionally evaluates the response quality.

    Design decision: Kept as a CLI for simplicity; avoids GUI complexity.
    Assumption: 'knowledge' folder exists with readable documents.
    Limitation: Doesn't support file upload or dynamic document addition.

    """
    chatbot = RAGChatbot()
    
    # First, ensure documents are indexed
    print("Indexing documents...")
    num_chunks = chatbot.index_documents()  # Changed from index_documents_task.execute
    print(f"Documents indexed successfully! Created {num_chunks} chunks.")
    
    print("\nRAG Chatbot initialized. Type 'exit' to quit.")
    
    while True:
        user_query = input("\nEnter your question: ")
        if user_query.lower() in ['exit', 'quit']:
            break
        
        print("\nProcessing your question...")
        result = chatbot.answer_question(user_query)
        
        print("\n" + "="*50)
        print("Response:")
        print(result['response'])
        print("\n" + "="*50)
        print(result['retrieved_context'])
        print("\n" + "="*50)
        if result['evaluation']:
            print("\nEvaluation Results:")
            print("-" * 30)
            for metric, data in result['evaluation'].items():
                if metric != "overall":
                    print(f"{metric.replace('_', ' ').title()}:")
                    print(f"  Score: {data['score']:.2f}")
                    print(f"  Passed: {'✓' if data['passed'] else '✗'}")
                    if data.get('suggestions'):
                        print("  Suggestions:")
                        for suggestion in data['suggestions']:
                            print(f"    - {suggestion}")
            
            print("\nOverall Assessment:")
            print(f"Score: {result['evaluation']['overall']['score']:.2f}")
            print("Strengths:", ", ".join(result['evaluation']['overall']['summary']['strengths']))
            if result['evaluation']['overall']['summary']['weaknesses']:
                print("Areas for Improvement:", ", ".join(result['evaluation']['overall']['summary']['weaknesses']))
        
        print("="*50)       

if __name__ == "__main__":
    run()