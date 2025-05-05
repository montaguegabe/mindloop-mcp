import os
from typing import Any, Dict, List, Literal, Optional

import httpx
from mcp.server.fastmcp import Context, FastMCP

# TODO: Replace with actual backend API URL
DEV_MODE = False
BACKEND_API_URL = (
    "http://localhost:8000/api" if DEV_MODE else "https://app.mindloop.net/api"
)

# Initialize the MCP Server
mcp = FastMCP("MindLoop Spaced Repetition")


# --- Placeholder HTTP Client ---
# In a real scenario, you might want a more robust client setup,
# possibly shared via lifespan context.
async def call_backend(
    endpoint: str,
    method: str = "GET",
    json_data: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> Any:
    """Calls the backend REST API, handling authentication and errors."""
    api_key = os.environ.get("MINDLOOP_API_KEY", "FILL_ME_IN")
    if not api_key:
        # Handle missing API key - maybe raise an error or return a specific dict
        print("Error: MINDLOOP_API_KEY environment variable not set.")
        return {"error": "Server configuration error: Missing API key."}

    headers = {"Authorization": f"Token {api_key}"}  # Assuming Api-Key scheme

    url = f"{BACKEND_API_URL}/{endpoint}/"  # Add trailing slash typical for DRF routers

    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, params=params, headers=headers)
            elif method == "POST":
                response = await client.post(url, json=json_data, headers=headers)
            elif method == "PUT":
                response = await client.put(url, json=json_data, headers=headers)
            # Add other methods (PATCH, DELETE) as needed
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
    except httpx.RequestError as e:
        print(f"Error calling backend API at {url}: {e}")
        return {"error": f"Failed to connect to backend: {e}", "details": str(e)}
    except httpx.HTTPStatusError as e:
        print(
            f"HTTP error calling backend API at {url}: {e.response.status_code} - {e.response.text}"
        )
        # Try to return the error detail from the API response if possible
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = e.response.text
        return {
            "error": f"Backend API request failed with status {e.response.status_code}",
            "details": error_detail,
        }
    except Exception as e:
        print(f"An unexpected error occurred when calling {url}: {e}")
        return {"error": f"An unexpected error occurred: {e}", "details": str(e)}


# --- MCP Tools ---


@mcp.tool()
async def search_facts(search_term: str, ctx: Context) -> List[Dict]:
    """
    Search for facts-to-memorize related to a search term.
    Facts are statements given in markdown, potentially including images.
    """
    ctx.info(f"Searching facts for term: {search_term}")
    # Call the backend API
    search_params = {"search_term": search_term}
    result = await call_backend("facts", method="GET", params=search_params)
    # TODO: Potentially transform the result if the API format differs from MCP expectation
    return result


@mcp.tool()
async def get_fact_recall_performance(fact_id: str, ctx: Context) -> Dict:
    """
    See recall performance for a given fact (history of right/wrong recall + stats).
    """
    ctx.info(f"Getting recall performance for fact_id: {fact_id}")
    # Call the backend API for the specific fact's performance endpoint
    endpoint = f"facts/{fact_id}/performance"
    result = await call_backend(endpoint, method="GET")
    return result


@mcp.tool()
async def create_recall_event(fact_id: str, remembered: bool, ctx: Context) -> Dict:
    """
    Create a recall event: the fact was remembered or not remembered.
    Returns the created event, including its ID needed for setting ease later if remembered=True.
    """
    ctx.info(f"Creating recall event for fact_id: {fact_id}, remembered: {remembered}")
    # Call the backend API to create a recall event
    event_data = {"fact": fact_id, "remembered": remembered}
    result = await call_backend("recall-events", method="POST", json_data=event_data)
    # The API returns the created event object
    return result


# Define the valid ease levels using Literal for type safety
RecallEaseLevel = Literal["Again", "Hard", "Good", "Easy"]


@mcp.tool()
async def set_recall_ease(
    recall_event_id: str, ease: RecallEaseLevel, ctx: Context
) -> Dict:
    """
    Set the recall ease for a successful recall event (Again, Hard, Good, Easy).
    This should only be called for events where remembered was True.
    """
    ctx.info(f"Setting recall ease for event_id: {recall_event_id} to '{ease}'")
    # Call the backend API to set the ease for a specific recall event
    endpoint = f"recall-events/{recall_event_id}/ease"
    ease_data = {"ease": ease}
    result = await call_backend(endpoint, method="PUT", json_data=ease_data)
    return result


@mcp.tool()
async def get_facts_for_review(count: int, ctx: Context) -> List[Dict]:
    """
    Get the top N facts that need to be reviewed based on recall probability.
    """
    ctx.info(f"Getting top {count} facts for review")
    # Call the backend API to get facts for review
    review_params = {"count": count}
    result = await call_backend("facts/review", method="GET", params=review_params)
    # TODO: Potentially transform the result if the API format differs from MCP expectation
    return result


# --- Server Execution ---
if __name__ == "__main__":
    print("Starting MindLoop MCP Server...")
    # You can run this server using:
    # mcp dev server.py
    # or
    # python server.py
    mcp.run()
