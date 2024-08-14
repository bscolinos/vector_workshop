from fastapi import FastAPI, Query
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
import json
import asyncio
import singlestoredb
from dotenv import load_dotenv

load_dotenv()

# Define your connection parameters
config = {
    'user': os.getenv('SINGLESTORE_USER'),
    'password': os.getenv('SINGLESTORE_PASSWORD'),
    'port': 3306,
    'host': os.getenv('SINGLESTORE_HOST'),
    'database': 'vector_workshop'
}

# Establish the database connection
db_connection = singlestoredb.connect(**config)
cursor = db_connection.cursor()

app = FastAPI()

# Set up OpenAI client and models
OPENAI_API_KEY = os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = AsyncOpenAI()
EMBEDDING_MODEL = 'text-embedding-ada-002'
GPT_MODEL = 'gpt-3.5-turbo'

async def get_embedding(text, model=EMBEDDING_MODEL):
    if isinstance(text, str):
        response = await client.embeddings.create(input=[text], model=model)
        return json.dumps(response.data[0].embedding)

async def vector_search(query, limit=15):
    query_embedding_vec = await get_embedding(query)
    query_statement = '''
        SELECT content, v <*> %s :> vector(1536) AS similarity
        FROM embeddings
        ORDER BY similarity DESC
        LIMIT %s;
    '''
    cursor.execute(query_statement, (query_embedding_vec, limit))
    results = cursor.fetchall()
    return results

async def rag(query, limit=5, temp=0.1):
    results = await vector_search(query, limit)
    prompt = f'''Excerpt from the conversation history:
        {results}
        Question: {query}

        You are a research assistant. Based on the conversation history, try to provide the most accurate answer to the question.
        Consider the details mentioned in the conversation history to formulate a response that is as
        helpful and precise as possible. 
        '''
    response = await client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a research assistant who is answering questions about an article."},
            {"role": "user", "content": prompt}
        ],
        temperature=temp
    )
    response_message = response.choices[0].message.content
    return response_message

class QueryInput(BaseModel):
    query: str
    limit: int = Query(5, ge=1, le=15)
    temperature: float = Query(0.1, ge=0, le=1)

@app.post("/rag")
async def perform_rag(query_input: QueryInput):
    result = await rag(query_input.query, query_input.limit, query_input.temperature)
    return {"response": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
