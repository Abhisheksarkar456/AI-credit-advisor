import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

AGENT_ID = "YBZ6CQZ1T7"
AGENT_ALIAS_ID = "WGW5DFWZMZ"
AWS_REGION = "us-east-1"

bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

@app.route("/query", methods=["POST"])
def query_agent():
    data = request.get_json(force=True, silent=True)
    user_message = data.get("message", "")
    session_id = str(uuid.uuid4())
    try:
        response = bedrock_agent_runtime.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=user_message
        )
        text = "".join(event.get("chunk", {}).get("bytes", b"").decode("utf-8", "replace") for event in response.get("completion", []))
        return jsonify({"reply": text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)