import aiohttp
import json
import logging
import sys
from pipelines import Pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Pipeline:
    @Pipeline.inlet()
    async def search_web(self, body):
        logger.info("Inlet triggered")
        sys.stdout.flush()
        
        messages = body.get('messages', [])
        if not messages:
            return body
        
        last_message = messages[-1].get('content', '').lower()
        if any(word in last_message for word in ['search', 'who is', 'what is', 'find']):
            logger.info(f"Search triggered for: {last_message}")
            sys.stdout.flush()

            # Extract clean query
            query = messages[-1]['content']
            if 'search' in last_message:
                query = query.split('search', 1)[1].strip()
            elif 'find' in last_message:
                query = query.split('find', 1)[1].strip()
            # For 'who is'/'what is', keep full as it's the query
            url = "http://searxng:8080/search"
            params = {
                "q": query,
                "format": "json",
                "categories": "general"
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params, timeout=30) as response:
                        if response.status == 200:
                            data = await response.json()
                            results = []
                            for result in data.get("results", [])[:5]:
                                results.append({
                                    "title": result.get("title", ""),
                                    "url": result.get("url", ""),
                                    "snippet": (result.get("content") or result.get("snippet") or "")[:300]
                                })
                            print(f"DEBUG: Sent {len(results)} results to model", flush=True)
                            search_result = json.dumps(results)
                        else:
                            search_result = json.dumps([{"title": "Error", "url": "", "snippet": f"HTTP {response.status}"}])
            except Exception as e:
                logger.error(f"Search error: {e}")
                sys.stdout.flush()
                search_result = json.dumps([{"title": "Error", "url": "", "snippet": str(e)}])

            logger.info(f"Messages length before: {len(messages)}")
            context_message = {
                "role": "assistant",
                "content": f"Search results (JSON array): {search_result}. Parse this JSON and use the information to answer the user's query, citing sources from the results."
            }
            body['messages'].insert(-1, context_message)
            logger.info(f"Messages length after: {len(body['messages'])}")
            logger.info("Search results added to messages")
            sys.stdout.flush()
        
        return body