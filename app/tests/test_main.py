import pytest
from httpx import AsyncClient, ASGITransport
from uuid import UUID, uuid4

from app.main import app, messages, TextModel


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Dailogy API"}


@pytest.mark.asyncio
async def test_transform_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/messages/", json={"original_text": "First message"})
        assert response.status_code == 200
        data = response.json()
        assert data["original_text"] == "First message"
        assert UUID(data["id"])  # Check if id is a valid UUID
        assert isinstance(data["original_text"], str)
        assert isinstance(data["prompt"], str)
        assert isinstance(data["transformed_text"], str)


@pytest.mark.asyncio
async def test_get_messages():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/messages/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1 # the message from test_transform_message
        assert data[0]["original_text"] == "First message"
        assert UUID(data[0]["id"])  # Check if id is a valid UUID
        assert isinstance(data[0]["original_text"], str)
        assert isinstance(data[0]["prompt"], str)
        assert isinstance(data[0]["transformed_text"], str)


@pytest.mark.asyncio
async def test_transform_message_add_2nd_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/messages/", json={"original_text": "Second message"})
        assert response.status_code == 200
        data = response.json()
        assert data["original_text"] == "Second message"
        assert UUID(data["id"])  # Check if id is a valid UUID
        assert isinstance(data["original_text"], str)
        assert isinstance(data["prompt"], str)
        assert isinstance(data["transformed_text"], str)


@pytest.mark.asyncio
async def test_get_messages_2messages():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/messages/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2 # the message from "test_transform_message" and "test_transform_message_add_2nd_message"
        # First message
        assert data[0]["original_text"] == "First message"
        assert UUID(data[0]["id"])  # Check if id is a valid UUID
        assert isinstance(data[0]["original_text"], str)
        assert isinstance(data[0]["prompt"], str)
        assert isinstance(data[0]["transformed_text"], str)
        # Second message
        assert data[1]["original_text"] == "Second message"
        assert UUID(data[1]["id"])  # Check if id is a valid UUID
        assert isinstance(data[1]["original_text"], str)
        assert isinstance(data[1]["prompt"], str)
        assert isinstance(data[1]["transformed_text"], str)


@pytest.mark.asyncio
async def test_add_multiple_messages():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First message
        response1 = await ac.post("/api/messages/", json={"original_text": "Third message"})
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["original_text"] == "Third message"
        assert UUID(data1["id"])
        assert isinstance(data1["original_text"], str)
        assert isinstance(data1["prompt"], str)

        # Second message
        response2 = await ac.post("/api/messages/", json={"original_text": "Fourth message"})
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["original_text"] == "Fourth message"
        assert UUID(data2["id"])
        assert isinstance(data2["original_text"], str)
        assert isinstance(data2["prompt"], str)

        # Check if both messages are in the database
        response = await ac.get("/api/messages/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4  # Including the message added in "test_get_messages" and "test_transform_message_add_2nd_message"
        texts = [msg["original_text"] for msg in data]
        assert "First message" in texts
        assert "Second message" in texts
        assert "Third message" in texts
        assert "Fourth message" in texts


@pytest.mark.asyncio
async def test_update_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Add a message to the in-memory database for testing
        message_id = str(uuid4())
        message = TextModel(id=message_id, original_text="message to update")
        messages.append(message) 
    
        # Define the updated message
        updated_message = {
            "id": message_id,
            "original_text": "updated message",
        }

        # Make a PUT request to update the message
        response = await ac.put(f"/api/messages/{message_id}", json=updated_message)
        print("Response status code:", response.status_code)
        print("Response content:", response.content)
        assert response.status_code == 200

        # Verify of the messages are updated
        response = await ac.get("/api/messages/")
        assert response.status_code == 200
        data = response.json()        
        texts = [msg["original_text"] for msg in data]
        assert "updated message" in texts
        assert "message to update" not in texts


@pytest.mark.asyncio
async def test_update_non_existing_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Generate a random UUID that is not in messages
        non_existing_message_id = str(uuid4())

        # Define the updated message
        updated_message = {
            "id": non_existing_message_id,
            "original_text": "updated non existing message",
        }

        # Make a PUT request to delete the message that does not extst
        response = await ac.put(f"/api/messages/{non_existing_message_id}", json=updated_message)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Add a message to the in-memory database for testing
        message_id = str(uuid4())
        message = TextModel(id=message_id, original_text="message to delete")
        messages.append(message)

        # Make a DELETE request to delete the message
        response = await ac.delete(f"/api/messages/{message_id}")
        assert response.status_code == 200

        # Verify of the messages are updated
        response = await ac.get("/api/messages/")
        assert response.status_code == 200
        data = response.json()        
        texts = [msg["original_text"] for msg in data]
        assert "message to delete" not in texts


@pytest.mark.asyncio
async def test_deletes_non_existing_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Generate a random UUID that is not in messages
        non_existing_message_id = str(uuid4())

        # Make a DELETE request to delete the message that does not extst
        response = await ac.delete(f"/api/messages/{non_existing_message_id}")
        assert response.status_code == 404
