import threading, asyncio, logging
from open_search_access import *

DOMAIN_INDEX_NAME = "domain1"
INSTRUCTION_INDEX_NAME = "instruction7"

async def _search_domain(user_query):
    """Asynchronously retrieve all available domain knowledge base data."""
    try:
        dom = await search_documents(user_query, DOMAIN_INDEX_NAME)

        return dom
    except Exception as e:
        logging.infp(f"Error in _display_domain_kb_data: {str(e)}")
        return []


async def _search_instructions(user_query):
    """Asynchronously retrieve all available domain knowledge base data."""
    try:
        ins = await search_instructions(user_query, INSTRUCTION_INDEX_NAME)
        return ins
    except Exception as e:
        logging.info(f"Error in _display_domain_kb_data: {str(e)}")
        return []


def get_instructions_domains(user_query: str) -> str:
    """Get instructions and domains for a given user query."""
    instructions = None
    domain = None
    logging.info("Started flow to get instructions and domains")

    def fetch_instructions():
        nonlocal instructions
        try:
            instructions = asyncio.run(_search_instructions(user_query))
            logging.info("Completed retrieving instructions")
        except Exception as e:
            logging.info(f"Error with instruction: {e}")

    def fetch_domain():
        nonlocal domain
        try:
            domain = asyncio.run(_search_domain(user_query))
            logging.info("Completed retrieving domain")
        except Exception as e:
            logging.info(f"Error with domain: {e}")

    thread1 = threading.Thread(target=fetch_instructions)
    thread2 = threading.Thread(target=fetch_domain)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    output = f"""
    Similar Instructions: {instructions}

    Similar Domain: {domain}
    """

    logging.info(output)
    return output