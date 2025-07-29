from fastapi import FastAPI
import asyncio
import httpx

app = FastAPI()

# 뉴스 URL 목록
NEWS_URLS: list[str] = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3"
]

# 요약 결과와 오류 타입을 dict로 타입힌트
async def fetch_and_summarize(url: str) -> dict[str, str]:
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url)
            data = await response.json()
            return {
                "url": url,
                "title": data.get("title", "No Title"),
                "summary": data.get("body", "")[:50] + "..."
            }
        except Exception as e:
            return {
                "url": url,
                "error": str(e)
            }

@app.get("/summaries")
async def get_summaries() -> dict[str, list[dict[str, str]]]:
    tasks = [fetch_and_summarize(url) for url in NEWS_URLS]
    results = await asyncio.gather(*tasks)
    return {"results": results}