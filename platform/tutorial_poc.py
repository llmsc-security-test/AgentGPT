#!/usr/bin/env python3
"""
Tutorial PoC - HTTP API Test Client for Reworkd Platform

This script demonstrates how to use the Platform API endpoints.
It includes examples for:
- Health checks
- Agent task operations (start, analyze, execute, create, summarize, chat)
- Tool listing
- Model listing
"""

import requests
import json
import sys
from typing import Any, Dict, Optional


class PlatformAPIClient:
    """Client for interacting with the Reworkd Platform API."""

    def __init__(self, base_url: str = "http://localhost:11230"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _get_url(self, endpoint: str) -> str:
        """Get full URL for an endpoint."""
        return f"{self.base_url}{endpoint}"

    def health_check(self) -> Dict[str, Any]:
        """Check platform health."""
        response = self.session.get(self._get_url("/api/monitoring/health"))
        response.raise_for_status()
        return response.json() if response.content else {"status": "ok"}

    def get_models(self, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Get available models."""
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        response = self.session.get(
            self._get_url("/api/models"), headers=headers
        )
        response.raise_for_status()
        return response.json()

    def get_tools(self) -> Dict[str, Any]:
        """Get available tools."""
        response = self.session.get(self._get_url("/api/agent/tools"))
        response.raise_for_status()
        return response.json()

    def start_agent_task(
        self, goal: str, run_id: Optional[str] = None, api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Start a new agent task with a goal.

        Args:
            goal: The goal for the agent to accomplish
            run_id: Optional run identifier
            api_key: Optional API key for authentication

        Returns:
            Response containing new tasks
        """
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "goal": goal,
            "run_id": run_id or "default-run",
        }

        response = self.session.post(
            self._get_url("/api/agent/start"),
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def analyze_task(
        self,
        goal: str,
        task: str,
        tool_names: Optional[list] = None,
        api_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a task to determine what actions to take.

        Args:
            goal: The overall goal
            task: The specific task to analyze
            tool_names: Optional list of tool names to consider
            api_key: Optional API key

        Returns:
            Analysis results
        """
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "goal": goal,
            "task": task,
            "tool_names": tool_names or [],
        }

        response = self.session.post(
            self._get_url("/api/agent/analyze"),
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def execute_task(
        self,
        goal: str,
        task: str,
        analysis: str,
        api_key: Optional[str] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute a task.

        Args:
            goal: The overall goal
            task: The task to execute
            analysis: The analysis from analyze_task
            api_key: Optional API key
            stream: Whether to stream the response

        Returns:
            Execution results
        """
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "goal": goal,
            "task": task,
            "analysis": analysis,
        }

        response = self.session.post(
            self._get_url("/api/agent/execute"),
            json=payload,
            headers=headers,
            stream=stream,
        )
        response.raise_for_status()

        if stream:
            return {"status": "streaming", "content": "[Streaming response]"}
        return response.json()

    def create_tasks(
        self,
        goal: str,
        tasks: Optional[list] = None,
        last_task: Optional[str] = None,
        result: Optional[str] = None,
        completed_tasks: Optional[list] = None,
        run_id: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create new tasks based on results.

        Args:
            goal: The overall goal
            tasks: Existing tasks
            last_task: The last completed task
            result: Result from the last task
            completed_tasks: List of completed task IDs
            run_id: Run identifier
            api_key: Optional API key

        Returns:
            Response with new tasks
        """
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "goal": goal,
            "tasks": tasks or [],
            "last_task": last_task,
            "result": result,
            "completed_tasks": completed_tasks or [],
            "run_id": run_id or "default-run",
        }

        response = self.session.post(
            self._get_url("/api/agent/create"),
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def summarize_tasks(
        self,
        goal: str,
        results: list,
        api_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Summarize task results.

        Args:
            goal: The overall goal
            results: List of results to summarize
            api_key: Optional API key

        Returns:
            Summary results
        """
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "goal": goal,
            "results": results,
        }

        response = self.session.post(
            self._get_url("/api/agent/summarize"),
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def chat(
        self,
        message: str,
        results: Optional[list] = None,
        api_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Chat with the agent.

        Args:
            message: The message to send
            results: Optional results to provide context
            api_key: Optional API key

        Returns:
            Chat response
        """
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "message": message,
            "results": results or [],
        }

        response = self.session.post(
            self._get_url("/api/agent/chat"),
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


def demo_health_check(client: PlatformAPIClient) -> None:
    """Demo health check endpoint."""
    print("\n=== Health Check ===")
    try:
        result = client.health_check()
        print(f"Health status: {result}")
    except Exception as e:
        print(f"Health check failed: {e}")


def demo_models(client: PlatformAPIClient, api_key: Optional[str]) -> None:
    """Demo models endpoint."""
    print("\n=== Available Models ===")
    try:
        result = client.get_models(api_key)
        print(f"Models: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Failed to get models: {e}")


def demo_tools(client: PlatformAPIClient) -> None:
    """Demo tools endpoint."""
    print("\n=== Available Tools ===")
    try:
        result = client.get_tools()
        print(f"Tools: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Failed to get tools: {e}")


def demo_agent_workflow(client: PlatformAPIClient, api_key: Optional[str]) -> None:
    """
    Demo complete agent workflow.

    This demonstrates a complete workflow:
    1. Start a simple goal
    2. Analyze the first task
    3. Execute the task
    """
    print("\n=== Agent Workflow Demo ===")

    # Step 1: Start task
    goal = "Create a simple to-do list app"
    print(f"\n1. Starting agent with goal: '{goal}'")
    try:
        start_result = client.start_agent_task(goal, api_key=api_key)
        print(f"Start result: {json.dumps(start_result, indent=2)}")

        # Extract tasks from result
        if "newTasks" in start_result:
            tasks = start_result["newTasks"]
            print(f"Created {len(tasks)} tasks")
    except Exception as e:
        print(f"Failed to start agent: {e}")
        return

    # Step 2: Analyze a task
    if "newTasks" in start_result and start_result["newTasks"]:
        first_task = start_result["newTasks"][0]
        print(f"\n2. Analyzing task: '{first_task}'")
        try:
            analysis_result = client.analyze_task(
                goal=goal,
                task=first_task,
                api_key=api_key,
            )
            print(f"Analysis: {json.dumps(analysis_result, indent=2)}")
        except Exception as e:
            print(f"Failed to analyze: {e}")


def main():
    """Main function to run demos."""
    print("=" * 60)
    print("Reworkd Platform API Test Client")
    print("=" * 60)

    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:11230"
    api_key = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\nConnecting to: {base_url}")
    print(f"API Docs: {base_url}/api/docs")
    print(f"Redoc: {base_url}/api/redoc")

    client = PlatformAPIClient(base_url)

    # Run demos
    demo_health_check(client)
    demo_models(client, api_key)
    demo_tools(client)

    # Agent workflow demo (requires valid API key for some operations)
    demo_agent_workflow(client, api_key)

    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
