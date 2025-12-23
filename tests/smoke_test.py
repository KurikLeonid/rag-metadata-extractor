import os

from langchain_google_genai import ChatGoogleGenerativeAI

from rag_metadata_extractor.extractor import MetadataExtractor
from rag_metadata_extractor.taxonomy import Taxonomy


def main():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"],
        temperature=0,
    )

    extractor = MetadataExtractor(llm=llm)
    taxonomy = Taxonomy()

    doc = """
    Project Phoenix was completed on 2024-11-18. This doc summarizes outcomes,
    risks, and follow-up actions for the Barcelona team. Updated on 2024-12-02.
    Benefits policy: Spain employees have 25 vacation days.
    """

    meta = extractor.extract(doc)
    meta.topics = taxonomy.add_tags(meta.topics)

    print(meta.model_dump())


if __name__ == "__main__":
    main()