import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import cohere
import json

# Load environment variables
load_dotenv()

# Initialize clients
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))
embed_model = SentenceTransformer("intfloat/e5-base-v2")
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def lambda_handler(event, context):
    print("EVENT RECEIVED:", json.dumps(event))  # Debug log
    
    # Handle CORS preflight requests (OPTIONS) for Lambda Function URLs
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }

    try:
        # Determine the payload source
        if 'body' in event:
            data = json.loads(event['body'])
        else:
            data = event  # For direct Lambda invocation via CLI

        # Extract question or message
        question = data.get('question') or data.get('message')

        if not question:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Missing "question" or "message" in request.'})
            }

        # Embed the question
        query_vector = embed_model.encode(question).tolist()
        result = index.query(vector=query_vector, top_k=5, include_metadata=True)
        contexts = [match["metadata"]["text"] for match in result["matches"]]

        prompt = f"""You are a knowledgeable and friendly support assistant for Ewa, an on-demand barbing service platform that connects customers with professional barbers in their area.

Your role is to provide clear, helpful, and accurate responses to user inquiries based on the context provided below.

Context:
{chr(10).join(contexts)}

Question: {question}
Answer:"""

        response = co.chat(
            model="command-r-plus-08-2024",
            prompt=prompt,  # Fixed: use 'prompt' not 'message'
            max_tokens=300,
            temperature=0.3
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'answer': response.text.strip()})
        }

    except Exception as e:
        print("ERROR:", str(e))  # Debug log
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        } 