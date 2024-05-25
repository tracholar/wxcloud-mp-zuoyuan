from sparkai.llm.llm import ChatSparkLLM, BaseCallbackHandler, ChunkPrintHandler, GenerationChunk, ChatGenerationChunk
from sparkai.core.messages import ChatMessage
from typing import Optional, Union, Any
import os
import json
from wxcloudrun.dao import query_config

spark_ai_conf = json.loads(query_config('SPARKAI_CONF').value)

SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'
SPARKAI_APP_ID = spark_ai_conf['SPARKAI_APP_ID']
SPARKAI_API_SECRET = spark_ai_conf['SPARKAI_API_SECRET']
SPARKAI_API_KEY = spark_ai_conf['SPARKAI_API_KEY']
SPARKAI_DOMAIN = 'general'


class MyHandler(BaseCallbackHandler):
    def __init__(self, color: Optional[str] = None) -> None:
        self.color = color

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            **kwargs: Any,
    ) -> Any:
        print(token)

def chat(msg):
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content="请在150字以内回复我。" + msg
    )]
    handler = MyHandler()
    a = spark.generate([messages], callbacks=[handler])
    for g in a.generations:
        for gg in g:
            return gg.text.strip()
    return 'NOT FOUND'
