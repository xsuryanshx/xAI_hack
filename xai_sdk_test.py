import os
import socket
import time

# Fix for gRPC DNS resolution issue: Force gRPC to use system DNS resolver instead of c-ares
# This must be set BEFORE importing grpc or xai_sdk
os.environ['GRPC_DNS_RESOLVER'] = 'native'  # Use system DNS resolver instead of c-ares

from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.tools import web_search, x_search, code_execution
import dotenv
dotenv.load_dotenv()

# Check API key
api_key = os.getenv("XAI_API_KEY")
if not api_key:
    raise ValueError("XAI_API_KEY environment variable is not set. Please set it before running this code.")

# Check network connectivity
def check_dns_resolution(hostname):
    """Check if DNS resolution works for a hostname"""
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False

print("Checking network connectivity...")
if not check_dns_resolution("api.x.ai"):
    print("Warning: DNS resolution for api.x.ai failed. This might be a network issue.")
    print("Please check:")
    print("1. Your internet connection")
    print("2. DNS server settings")
    print("3. Firewall/proxy settings")
    print("4. VPN connection (if using)")
    print("\nAttempting to continue anyway...")

# Create client with error handling
try:
    client = Client(api_key=api_key)
    print("Client created successfully.")
except Exception as e:
    print(f"Error creating client: {e}")
    raise

# Create chat with retry logic
max_retries = 3
retry_delay = 2

for attempt in range(max_retries):
    try:
        chat = client.chat.create(
            model="grok-4-1-fast",  # reasoning model
            # All server-side tools active
            tools=[
                web_search(),
                x_search(),
                code_execution(),
            ],
        )
        print("Chat session created successfully.")
        break
    except Exception as e:
        if attempt < max_retries - 1:
            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Failed after {max_retries} attempts: {e}")
            raise

# Feel free to change the query here to a question of your liking
chat.append(user("What are the latest updates from xAI?"))

is_thinking = True
response = None

try:
    for response, chunk in chat.stream():
        # View the server-side tool calls as they are being made in real-time
        for tool_call in chunk.tool_calls:
            print(f"\nCalling tool: {tool_call.function.name} with arguments: {tool_call.function.arguments}")
        if response.usage.reasoning_tokens and is_thinking:
            print(f"\rThinking... ({response.usage.reasoning_tokens} tokens)", end="", flush=True)
        if chunk.content and is_thinking:
            print("\n\nFinal Response:")
            is_thinking = False
        if chunk.content and not is_thinking:
            print(chunk.content, end="", flush=True)
except Exception as e:
    print(f"\n\nError during streaming: {e}")
    print("\nThis might be due to:")
    print("1. Network connectivity issues")
    print("2. DNS resolution problems")
    print("3. API endpoint unavailability")
    print("4. Invalid API key")
    raise

if response:
    print("\n\nCitations:")
    print(response.citations)
    print("\n\nUsage:")
    print(response.usage)
    print(response.server_side_tool_usage)
    print("\n\nServer Side Tool Calls:")
    print(response.tool_calls)