# 🚀 Setup Guide - Ewa Customer Support Automation

This guide will help you set up and deploy the Ewa customer support automation system.

## 📋 Prerequisites

Before you begin, ensure you have the following:

### Required Accounts
- **AWS Account** with appropriate permissions
- **Pinecone Account** for vector database
- **Cohere Account** for AI text generation

### Required Software
- **Python 3.8+** installed on your system
- **Git** for version control
- **AWS CLI** configured with credentials
- **Docker** (optional, for containerized deployment)

## 🔧 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ewa-customer-support-automation.git
cd ewa-customer-support-automation
```

### 2. Set Up Environment Variables

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your actual API keys
nano .env
```

Fill in your API keys:
```env
PINECONE_API_KEY=your_actual_pinecone_api_key
PINECONE_INDEX=your_actual_pinecone_index_name
COHERE_API_KEY=your_actual_cohere_api_key
```

### 3. Set Up Pinecone Vector Database

#### Create Pinecone Index

1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Create a new index with:
   - **Name**: `ewa-support-index`
   - **Dimensions**: `768` (for e5-base-v2 model)
   - **Metric**: `cosine`
   - **Cloud**: `AWS`
   - **Region**: `us-east-1`

#### Upload Knowledge Base

Create a script to upload your knowledge base:

```python
# upload_knowledge.py
import pinecone
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

# Initialize embedding model
embed_model = SentenceTransformer("intfloat/e5-base-v2")

# Your knowledge base data
knowledge_base = [
    {
        "text": "Ewa is an on-demand barbing service platform that connects customers with professional barbers in their area.",
        "metadata": {"category": "about", "service": "general"}
    },
    {
        "text": "To book a barber, download the Ewa app, create an account, select your location, choose a barber, and schedule your appointment.",
        "metadata": {"category": "booking", "service": "appointment"}
    },
    # Add more knowledge base entries...
]

# Upload to Pinecone
for i, item in enumerate(knowledge_base):
    embedding = embed_model.encode(item["text"]).tolist()
    index.upsert(vectors=[{
        "id": f"doc_{i}",
        "values": embedding,
        "metadata": item["metadata"]
    }])

print("Knowledge base uploaded successfully!")
```

### 4. Deploy AWS Lambda Function

#### Option A: Using AWS CLI

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Create deployment package
cd backend
zip -r lambda_deployment.zip .

# Deploy to AWS Lambda
aws lambda create-function \
  --function-name ewa-chatbot \
  --runtime python3.10 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_deployment.zip \
  --timeout 30 \
  --memory-size 512

# Or update existing function
aws lambda update-function-code \
  --function-name ewa-chatbot \
  --zip-file fileb://lambda_deployment.zip
```

#### Option B: Using Docker

```bash
# Build Docker image
docker build -t ewa-chatbot backend/

# Test locally
docker run -p 9000:8080 ewa-chatbot

# Deploy to AWS ECR
aws ecr create-repository --repository-name ewa-chatbot
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag ewa-chatbot:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ewa-chatbot:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ewa-chatbot:latest
```

### 5. Configure Lambda Function URL

```bash
# Create function URL
aws lambda create-function-url-config \
  --function-name ewa-chatbot \
  --auth-type NONE \
  --cors '{
    "AllowCredentials": false,
    "AllowHeaders": ["*"],
    "AllowMethods": ["POST", "OPTIONS"],
    "AllowOriginUrls": ["*"],
    "ExposeHeaders": ["*"],
    "MaxAge": 86400
  }'
```

### 6. Set Up API Gateway (Optional)

If you prefer using API Gateway instead of Lambda Function URLs:

```bash
# Create HTTP API
aws apigatewayv2 create-api \
  --name ewa-chatbot-api \
  --protocols HTTP

# Add route
aws apigatewayv2 create-route \
  --api-id YOUR_API_ID \
  --route-key "POST /chat" \
  --target "integrations/YOUR_INTEGRATION_ID"

# Deploy API
aws apigatewayv2 create-deployment \
  --api-id YOUR_API_ID
```

### 7. Test the Backend

```bash
# Test with curl
curl -X POST https://your-lambda-url.lambda-url.us-east-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I book a barber?"}'
```

### 8. Set Up Frontend

```bash
# Start local development server
python -m http.server 8000

# Or using Node.js
npx http-server -p 8000
```

### 9. Update Frontend Configuration

Edit `frontend/script.js` to point to your Lambda function URL:

```javascript
this.apiUrl = 'https://your-lambda-url.lambda-url.us-east-1.on.aws/';
```

## 🔍 Testing

### Test API Connection

1. Open `http://localhost:8000/test_connection.html`
2. Click "Test API" button
3. Verify response contains AI-generated answer

### Test Chatbot Interface

1. Open `http://localhost:8000`
2. Send test messages:
   - "How do I book a barber?"
   - "What services do you offer?"
   - "How much does a haircut cost?"

## 🚀 Production Deployment

### Frontend Deployment

#### Option A: Netlify
1. Connect your GitHub repository to Netlify
2. Set build command: `echo "No build required"`
3. Set publish directory: `.`
4. Deploy automatically

#### Option B: Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`

#### Option C: AWS S3 + CloudFront
```bash
# Create S3 bucket
aws s3 mb s3://ewa-chatbot-frontend

# Upload files
aws s3 sync frontend/ s3://ewa-chatbot-frontend --delete

# Create CloudFront distribution
aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json
```

### Backend Monitoring

Set up CloudWatch alarms:

```bash
# Create error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name ewa-chatbot-errors \
  --alarm-description "Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=FunctionName,Value=ewa-chatbot
```

## 🔧 Troubleshooting

### Common Issues

#### CORS Errors
- Ensure Lambda function returns proper CORS headers
- Check API Gateway CORS configuration
- Verify function URL CORS settings

#### API Key Errors
- Verify environment variables are set correctly
- Check API key permissions and quotas
- Ensure keys are valid and active

#### Lambda Timeout
- Increase timeout in Lambda configuration
- Optimize code for faster execution
- Consider using async operations

#### Memory Issues
- Increase Lambda memory allocation
- Optimize model loading
- Use smaller embedding models if needed

### Debug Logging

Enable detailed logging in Lambda:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check CloudWatch logs for debugging information.

## 📞 Support

For additional help:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review AWS Lambda and Pinecone documentation

---

**Happy coding! 🚀** 