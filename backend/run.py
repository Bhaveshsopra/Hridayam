"""
Run the AI Smart Tourism MP server.

Usage:
    python run.py

The server starts at http://127.0.0.1:5000
"""

from app import app

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  🏛️  AI SMART TOURISM — MADHYA PRADESH")
    print("  🤖 Backend Server Starting...")
    print("=" * 55)
    print(f"\n  🌐 URL:  http://127.0.0.1:5000")
    print(f"  📋 API:  http://127.0.0.1:5000/health")
    print(f"  🗺️  Plan: POST http://127.0.0.1:5000/plan")
    print(f"  💬 Chat: POST http://127.0.0.1:5000/chatbot")
    print(f"  🆘 SOS:  POST http://127.0.0.1:5000/sos")
    print(f"\n  Press Ctrl+C to stop the server\n")
    print("=" * 55 + "\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )