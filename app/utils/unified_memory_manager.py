from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain_openai import ChatOpenAI
from app.core.config import settings


class UnifiedMemoryManager:
    def __init__(
        self, thread_id: str, max_messages: int = 4, summary_token_limit: int = 500
    ):
        self.session_id = f"user-{thread_id}"
        self.max_messages = max_messages
        self.summary_token_limit = summary_token_limit

        mongo_uri = settings.MONGO_URI
        database_name = settings.MONGO_DB_NAME
        collection_name = "chat_message_history"

        self.chat_history = MongoDBChatMessageHistory(
            connection_string=mongo_uri,
            database_name=database_name,
            collection_name=collection_name,
            session_id=self.session_id,
        )

        # ✅ Direct OpenAI model (LLMProvider removed)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            verbose=True,
        )

    def get_full_history(self):
        return self.chat_history.messages

    async def get_history_context(self, user_query: str):
        messages = self.chat_history.messages

        if len(messages) > self.max_messages:
            to_summarize = messages[:-self.max_messages]
            recent = messages[-self.max_messages:]
            summary = await self.summarize_messages(to_summarize)
            context = []

            if summary:
                context.append(
                    {
                        "role": "system",
                        "content": f"Summary of previous conversation: {summary}",
                    }
                )

            for msg in recent:
                if msg.type == "human":
                    context.append({"role": "user", "content": msg.content.strip()})
                elif msg.type == "ai":
                    context.append(
                        {"role": "assistant", "content": msg.content.strip()}
                    )
        else:
            context = []
            for msg in messages:
                if msg.type == "human":
                    context.append({"role": "user", "content": msg.content.strip()})
                elif msg.type == "ai":
                    context.append(
                        {"role": "assistant", "content": msg.content.strip()}
                    )

        return context

    async def summarize_messages(self, messages):
        conversation_text = []

        for msg in messages:
            if msg.type == "human":
                conversation_text.append(HumanMessage(content=msg.content.strip()))
            elif msg.type == "ai":
                conversation_text.append(AIMessage(content=msg.content.strip()))

        if not conversation_text:
            return ""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"Summarize the following conversation in under {self.summary_token_limit} tokens. "
                    "Focus on key facts, decisions, and context needed for future turns:\n\n{conversation}",
                )
            ]
        )

        chain = prompt | self.llm
        summary_response = await chain.ainvoke(
            {"conversation": conversation_text}
        )

        return summary_response.content.strip()

    def update_memory(
        self, user_query: str, ai_response: str, max_ai_chars: int = 2000
    ):
        self.chat_history.add_user_message(user_query)

        trimmed_response = (
            ai_response[:max_ai_chars] + "\n\n[...truncated]"
            if len(ai_response) > max_ai_chars
            else ai_response
        )

        self.chat_history.add_ai_message(trimmed_response)
