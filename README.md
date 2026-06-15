# 🚀 ExcelGPT – AI-Powered Business Intelligence Assistant
🌐 Live Demo: https://excelgpt.streamlit.app/

ExcelGPT transforms Excel files into an intelligent analytics platform. Upload one or more datasets, ask questions in plain English, and receive SQL-powered insights, interactive visualizations, dashboards, and business explanations instantly.

Built with FastAPI, LangGraph, DuckDB, and LLMs, ExcelGPT acts as an AI Data Analyst capable of understanding relationships across datasets and generating actionable insights without requiring SQL knowledge.

---

## ✨ Features

### 🤖 Natural Language Analytics

Ask questions like:

> Which customer generated the highest revenue in South Region?

> Show category contribution in revenue as a pie chart

> Create an executive dashboard

ExcelGPT automatically generates SQL, executes queries, visualizes results, and explains findings.

---

### 📂 Multi-File Upload Support

Upload multiple Excel files simultaneously:

* Orders.xlsx
* Customers.xlsx
* Products.xlsx
* Regions.xlsx

The platform automatically discovers relationships and enables cross-dataset analysis.

---

### 🔗 Relationship Discovery Engine

Automatically detects:

* Primary / Foreign Key relationships
* Common business entities
* Cross-table joins

Example:

orders.Customer ID
→ customers.Customer ID

orders.Product Code
→ products.Product Code

orders.Region Code
→ regions.Region Code

---

### 🧠 AI Multi-Agent Workflow

Powered by LangGraph.

User Question
→ Intent Agent
→ SQL Agent
→ DuckDB Engine
→ Chart Agent
→ Explain Agent
→ Dashboard Agent

Agents collaborate to determine user intent, generate queries, create visualizations, and explain results.

---

### 📊 Smart Visualization Engine

Automatically selects the most suitable chart:

* Bar Charts
* Grouped Bar Charts
* Line Charts
* Pie Charts
* Scatter Plots
* Heatmaps
* Treemaps

Supports dynamic chart recommendations based on query results.

---

### 📈 Dashboard Generator

Generate complete dashboards using natural language:

> Create Executive Dashboard

Includes:

* Revenue KPIs
* Regional Performance
* Product Insights
* Revenue Trends
* Top Customers
* Category Analysis

---

### 🔍 AI Dataset Profiling

After upload, ExcelGPT automatically generates:

* Dataset Overview
* Data Quality Score
* Missing Value Analysis
* Duplicate Detection
* Numeric Statistics
* Categorical Statistics
* Suggested Business Questions

---

### 💡 Business Insight Generation

Automatically identifies:

* Top Products
* Best Performing Regions
* Most Ordered Products
* Revenue Trends
* Missing Data
* Outliers

---

## 🏗️ Architecture

│ User Question 
│
▼
│ Intent Agent 
│
▼
│ SQL Agent 
│
▼
│ DuckDB Engine 
│
▼
│ Chart Agent 
│
▼
│ Explain Agent 
│
▼
│ Dashboard Agent 

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Plotly

### Backend

* FastAPI
* LangGraph

### Database

* DuckDB

### Data Processing

* Pandas

### AI / LLM

* OpenRouter
* DeepSeek

### Visualization

* Plotly Express

---

## 📁 Project Structure

excelgpt/

├── frontend/

│ ├── app.py

│ └── utils/

├── backend/

│ ├── api/

│ ├── agents/

│ ├── graph/

│ ├── services/

│ ├── database/

│ └── llm/

├── uploads/

├── excelgpt.db

└── requirements.txt

---

## 🚀 Running Locally

### Backend

```bash
cd backend

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

streamlit run app.py
```

---

## Example Workflow

### Upload

* Orders.xlsx
* Customers.xlsx
* Products.xlsx

### Ask

```text
Which customer bought the most products?
```

### ExcelGPT

✅ Detects relationships

✅ Generates SQL joins

✅ Executes query

✅ Creates visualization

✅ Explains results in business language

---

## Future Enhancements

* Export Dashboard to PDF
* PowerPoint Report Generation
* Conversational Memory
* Automated KPI Monitoring
* Scheduled Insight Reports
* Role-Based Access Control
* Semantic Data Catalog
* Vector Search over Business Documents

---

## Why ExcelGPT?

Most BI tools require users to understand SQL, data modeling, and dashboard creation.

ExcelGPT enables anyone to upload spreadsheets and interact with data conversationally, making analytics accessible to business users, analysts, and decision-makers.

---

⭐ If you found this project interesting, consider giving it a star and sharing feedback.
