# Vector Workshop

## Overview

Welcome to the Vector Workshop repository! This workshop is designed to help you build a production grade Retrieval-Augmented Generation (RAG) application.

## Objectives

- Understand the fundamentals of SingleStore and its applications in RAG solutions.
- Learn how to vectorize text data and store it in SingleStore.
- Explore querying techniques to retrieve relevant information from vectorized/text data.
- Implement a RAG solution.

## Prerequisites

- Basic knowledge of SingleStore, Python, and SQL.
- Access to SingleStore.
- Text data you want to use in a RAG application.
- Pre-built LOAD DATA NOTEBOOK
- Pre-built QUERY NOTEBOOK
- Pre-built RAG NOTEBOOK


## Workshop Structure

### 1. Introduction and Setup (30 minutes)

- **Initial Setup** (5 min)
  - One person sets up a new WSG and WS in the CO

- **Notebook Walkthrough** (15 min)
  - One person demonstrates a notebook that:
    - Branches the database
    - Chunks and embeds data
    - Reinserts data
    - Builds vector and full-text indexes

- **Q&A Session** (5 min)

- **Access Distribution** (5 min)
  - Provide querying notebook access to all participants (via GitHub repo)

### 2. Building a Generative AI Application (30 minutes)

- **Hands-on Exercise** (20 min)
  - Build a basic RAG app with participant data in SingleStore
    - Implement RAG in three functions
    - Write correct SQL queries
    - Integrate with pre-built React frontend

- **Q&A Session** (10 min)

### 3. Deep Dive and Q&A (30 minutes)

- **Vector Search**
  - Demo fast kNN search
  - Demo fast ANN search
  - Index usage and best practices
  - Vector range searches (for 8.7.x users)

- **Fulltext Search**
  - Exact search
  - Fuzzy search
  - Proximity search
  - BM25 and other techniques

- **Hybrid Search**
  - Benefits in AI applications
  - Implementation strategies

- **Open Q&A**
  - Address participant questions
