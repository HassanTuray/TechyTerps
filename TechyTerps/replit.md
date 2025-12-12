# Overview

This is a GroupMe bot application that detects scam messages using machine learning. The bot is deployed on Replit and integrates with GroupMe's webhook API to receive and respond to messages. When messages are received, they are analyzed using a Naive Bayes classifier to determine if they are scam attempts.

# System Architecture

## Application Framework
**Decision:** Flask web framework for HTTP server
**Rationale:** Lightweight framework suitable for webhook-based integrations. Provides simple routing for both health checks (GET/HEAD) and webhook callbacks (POST).
**Trade-offs:** Flask is production-ready but requires additional configuration for high-scale deployments. Chosen for simplicity and fast development on Replit.

## Machine Learning Integration
**Decision:** Scikit-learn Naive Bayes classifier loaded via joblib
**Rationale:** Pre-trained model for text classification, loaded once at startup for performance. Naive Bayes is computationally efficient and well-suited for text spam/scam detection.
**Implementation:** Model stored at `TechyTerps/model/models/naive_bayes_pipeline.pkl` and loaded globally to avoid repeated disk I/O.
**Error Handling:** Graceful degradation - if model fails to load, scam detection is disabled but bot remains functional.

## Bot Response Logic
**Decision:** Scam detection
**Rationale:** 
- ML-based scam detection for security monitoring
**Alternatives Considered:** Could use other models based on current notebooks

## Deployment Architecture
**Decision:** Replit hosting with Flask development server
**Rationale:** Replit provides always-on hosting with automatic HTTPS endpoint. Flask runs on host 0.0.0.0:8080 to accept external connections.
**Health Check:** GET/HEAD endpoint at "/" returns 200 OK for uptime monitoring and GroupMe webhook verification.

## Message Flow
1. GroupMe sends webhook POST to Replit URL
2. Flask receives JSON payload with message data
3. Message text is extracted and processed
4. Scam detection model analyzes text (if loaded)
5. Bot responds via GroupMe POST API if conditions are met

# External Dependencies

## GroupMe API
**Integration:** Webhook-based message reception and bot posting API
**Authentication:** Bot ID (`BOT_ID`) used for posting messages
**Endpoints:**
- Incoming webhooks: POST to Replit URL
- Outgoing messages: POST to `https://api.groupme.com/v3/bots/post`
**Configuration:** Bot created via GroupMe Developer Portal at dev.groupme.com/bots

## Python Libraries
- **Flask:** Web framework for HTTP server and routing
- **requests:** HTTP client for sending messages to GroupMe API
- **joblib:** Model serialization/deserialization for ML pipeline
- **scikit-learn (implicit):** Required by the loaded Naive Bayes model pipeline

## File System Dependencies
- Bot code: `TechyTerps/bot/bot.py`
- Model file at relative path: `TechyTerps/model/models/naive_bayes_pipeline.pkl`
- No database currently used - stateless operation
- All data processing happens in-memory during request handling

## Bot Message Filtering
- Bot ignores messages from other bots (sender_type == 'bot') to prevent infinite loops
- Only user messages are processed for scam detection and keyword responses

## Callback URL Configuration
- GroupMe callback URL must include port: `https://<replit-url>:8080`

## Hosting Platform
**Platform:** Replit
**Requirements:**
- Python runtime environment
- Public HTTPS endpoint for webhooks
- Port 8080 accessibility
- Persistent storage for model file