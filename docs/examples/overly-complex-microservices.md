\# Case Study: Overly Complex Microservices Architecture



\## The Scenario

A startup built a microservices architecture for their e-commerce platform with:

\- 12 microservices

\- Each with its own database

\- Service mesh (Istio)

\- Multiple message queues (Kafka + RabbitMQ)

\- Redis for caching

\- Elasticsearch for logging



\## The Problem

The architecture was over-engineered for their scale (10,000 users/month). 

High operational cost, complex deployments, and slow development velocity.



\## Running Loom Audit



```bash

\# Save the pattern

cat > complex-ecommerce.json << 'EOF'

{

&nbsp; "name": "Complex E-commerce",

&nbsp; "components": \[

&nbsp;   "FastAPI", "PostgreSQL", "Redis", "Kafka", "RabbitMQ",

&nbsp;   "Elasticsearch", "Istio", "Docker", "Kubernetes"

&nbsp; ]

}

EOF



\# Audit it

loom audit complex-ecommerce.json

