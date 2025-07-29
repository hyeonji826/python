import os
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))
url = os.getenv("DB_URL")
dbconn = MongoClient(url)
database = dbconn['aiproject']
collection = database['ad']
class AdGenerator:
    def __init__(self, engine='gpt-4.1-nano-2025-04-14'):
        self.engine = engine
    def using_llm(self, prompt):
        system_instruction = 'assistant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라'
        messages = [{"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=self.engine,
            messages=messages
        )
        return response.choices[0].message.content
    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품 이름: {product_name}\n주요 내용: {details}\n 광고 문구의 스타일: {tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'
        result = self.using_llm(prompt=prompt)
        return result
app = FastAPI()
class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str
@app.post("/create_ad")
async def create_ad(product: Product):
    ad_generator = AdGenerator()
    ag = ad_generator.generate(product_name=product.product_name,
                               details=product.details,
                               tone_and_manner=product.tone_and_manner)
    data_insert = {'product_name': product.product_name,
                   'details': product.details,
                   'tone_and_manner': product.tone_and_manner, 'ad': ag}
    result = collection.insert_one(data_insert)
    result = collection.find({})
    datas = []
    for data in result:
        data.pop('_id', None)
        datas.append(data)
        
    return {'ad': ag, 'datas': datas}