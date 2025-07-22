# 🤖 Ewa Customer Support Automation

A modern, AI-powered customer support chatbot system for Ewa, an on-demand barbing service platform. Built with RAG (Retrieval-Augmented Generation) technology, this system provides intelligent, context-aware responses to customer inquiries.

## 🚀 Live Demo

Access the chatbot at: `http://localhost:8000` (after running the local server)

## ✨ Features

- **🤖 AI-Powered Responses** - Intelligent answers using RAG technology
- **💬 Real-time Chat Interface** - Modern, responsive chatbot UI
- **🔍 Semantic Search** - Vector-based knowledge retrieval
- **⚡ Serverless Architecture** - Scalable AWS Lambda backend
- **📱 Mobile Responsive** - Works seamlessly on all devices
- **🎨 Modern UI/UX** - Professional design with smooth animations

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Icon library

### Backend
- **Python** - Serverless Lambda function
- **AWS Lambda** - Serverless compute
- **AWS API Gateway** - HTTP API management

### AI/ML
- **Pinecone** - Vector database for semantic search
- **Cohere** - AI text generation (Command-R-Plus model)
- **Sentence Transformers** - Text embedding (intfloat/e5-base-v2)

### Infrastructure
- **AWS CloudWatch** - Monitoring and logging
- **AWS IAM** - Security and permissions

## 📁 Project Structure

```
ewa-customer-support-automation/
├── frontend/
│   ├── index.html          # Main chatbot interface
│   ├── styles.css          # Modern CSS styling
│   ├── script.js           # JavaScript functionality
│   └── test_connection.html # API testing utility
├── backend/
│   ├── lambda_function.py  # AWS Lambda function code
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Container configuration
├── docs/
│   ├── setup.md           # Detailed setup instructions
│   └── api.md             # API documentation
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS CLI configured
- Node.js (optional, for alternative server)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ewa-customer-support-automation.git
cd ewa-customer-support-automation
```

### 2. Set Up Environment Variables

Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your actual API keys:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=your_pinecone_index_name
COHERE_API_KEY=your_cohere_api_key
```

### 3. Deploy Backend

#### Option A: Using AWS CLI

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Deploy Lambda function
aws lambda update-function-code \
  --function-name your-lambda-function-name \
  --zip-file fileb://backend/lambda_function.py
```

#### Option B: Using Docker

```bash
# Build and deploy
docker build -t ewa-chatbot .
docker run -p 9000:8080 ewa-chatbot
```

### 4. Start Frontend Server

```bash
# Using Python
python -m http.server 8000

# Or using Node.js
npx http-server -p 8000
```

### 5. Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PINECONE_API_KEY` | Pinecone API key for vector database | Yes |
| `PINECONE_INDEX` | Pinecone index name | Yes |
| `COHERE_API_KEY` | Cohere API key for AI generation | Yes |

### API Endpoints

The system uses the following endpoints:

- **Lambda Function URL**: `https://your-lambda-url.lambda-url.us-east-1.on.aws/`
- **API Gateway**: `https://your-api-gateway.execute-api.us-east-1.amazonaws.com/prod/chat`

## 🧪 Testing

### Test API Connection

Use the included test file to verify API connectivity:

```bash
# Open in browser
http://localhost:8000/test_connection.html
```

### Manual Testing

1. Open the chatbot interface
2. Send test messages like:
   - "How do I book a barber?"
   - "What services do you offer?"
   - "How much does a haircut cost?"

## 📊 API Documentation

### Request Format

```json
{
  "question": "Your question here"
}
```

### Response Format

```json
{
  "answer": "AI-generated response based on knowledge base"
}
```

### Error Response

```json
{
  "error": "Error message description"
}
```

## 🔒 Security

- **CORS Configuration** - Properly configured for cross-origin requests
- **Environment Variables** - Sensitive data stored securely
- **Input Validation** - Sanitized user inputs
- **Error Handling** - Graceful error responses without exposing sensitive information

## 🚀 Deployment

### Production Deployment

1. **Frontend**: Deploy to static hosting (Netlify, Vercel, AWS S3)
2. **Backend**: Deploy Lambda function to AWS
3. **Domain**: Configure custom domain and SSL certificate
4. **Monitoring**: Set up CloudWatch alerts and logging

### Environment-Specific Configurations

- **Development**: Local server with debug logging
- **Staging**: AWS with test data
- **Production**: AWS with production data and monitoring



**Built with ❤️ for Ewa Barbing Platform** 
