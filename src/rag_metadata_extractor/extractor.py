from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class Metadata(BaseModel):
    doc_date: Optional[str] = Field(default=None, description="Document date in ISO format if possible (YYYY-MM-DD)")
    summary: str = Field(description="Short summary (1-3 sentences)")
    topics: List[str] = Field(default_factory=list, description="List of topics/tags")
    location: Optional[str] = Field(default=None, description="Location/country/region if applicable")
    confidence: float = Field(default=0.7, description="0..1 overall confidence")


class MetadataExtractor:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.parser = JsonOutputParser(pydantic_object=Metadata)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You extract structured metadata for RAG indexing. "
             "Return ONLY valid JSON matching the schema."),
            ("user",
             "Document:\n{doc}\n\n"
             "Schema:\n{schema}\n\n"
             "Rules:\n"
             "- topics: short, canonical, lowercase where possible\n"
             "- doc_date: prefer explicit doc date, not ingestion date\n"
             "- if unknown, set null/empty\n"),
        ])

    def extract(self, doc_text: str) -> Metadata:
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({
            "doc": doc_text,
            "schema": self.parser.get_format_instructions(),
        })
