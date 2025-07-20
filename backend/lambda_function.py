"""
Ewa Customer Support Automation - Lambda Function
AI-powered chatbot backend using RAG (Retrieval-Augmented Generation)

Author: [Your Name]
Date: [Current Date]
"""

import os
import json
import logging
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import cohere

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize clients
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))
embed_model = SentenceTransformer("intfloat/e5-base-v2")
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def lambda_handler(event, context):
    """
    AWS Lambda handler function for Ewa customer support chatbot.
    
    Args:
        event (dict): AWS Lambda event object
        context (object): AWS Lambda context object
    
    Returns:
        dict: API Gateway response with CORS headers
    """
    logger.info("EVENT RECEIVED: %s", json.dumps(event))
    
    # Handle CORS preflight requests (OPTIONS)
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
        # Parse the incoming event
        data = None
        if 'body' in event:
            if isinstance(event['body'], str):
                try:
                    data = json.loads(event['body'])
                except json.JSONDecodeError as e:
                    logger.error("JSON decode error: %s", e)
                    data = {'body': event['body']}
            elif isinstance(event['body'], dict):
                data = event['body']
            else:
                data = {}
        elif isinstance(event, dict):
            data = event
        else:
            data = {}

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
                'body': json.dumps({
                    'error': 'Missing "question" or "message" in request.',
                    'received': data
                })
            }

        # Generate embeddings and search for relevant context
        logger.info("Processing question: %s", question)
        query_vector = embed_model.encode(question).tolist()
        result = index.query(vector=query_vector, top_k=5, include_metadata=True)
        contexts = [match["metadata"]["text"] for match in result["matches"]]

        # Create prompt for AI generation
        prompt = f"""You are a knowledgeable and friendly support assistant for Ewa, an on-demand barbing service platform that connects customers with professional barbers in their area.

Your role is to provide clear, helpful, and accurate responses to user inquiries based on the context provided below.

Context:
{chr(10).join(contexts)}

Question: {question}
Answer:"""

        # Generate AI response
        response = co.chat(
            model="command-r-plus-08-2024",
            prompt=prompt,
            max_tokens=300,
            temperature=0.3
        )

        logger.info("Generated response successfully")
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
        logger.error("Error processing request: %s", str(e))
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