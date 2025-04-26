import pytest

from api_project.pages.pet_store_api import PetStoreAPI


@pytest.fixture
def api():
    return PetStoreAPI()


@pytest.fixture
def sample_pet_data():
    return {
        "id": 1,
        "category": {
            "id": 1,
            "name": "dogs"
        },
        "name": "doggie",
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }


class TestPetStoreAPI:
    def test_create_pet_positive(self, api, sample_pet_data):
        response = api.create_pet(sample_pet_data)
        assert response.status_code == 200
        assert response.json()["id"] == sample_pet_data["id"]
        assert response.json()["name"] == sample_pet_data["name"]

    def test_create_pet_negative(self, api):
        invalid_data = {"invalid": "data"}
        response = api.create_pet(invalid_data)
        assert response.status_code == 500

    def test_get_pet_positive(self, api, sample_pet_data):
        # First create a pet
        api.create_pet(sample_pet_data)
        # Then get it
        response = api.get_pet(sample_pet_data["id"])
        assert response.status_code == 200
        assert response.json()["id"] == sample_pet_data["id"]

    def test_get_pet_negative(self, api):
        response = api.get_pet(999999)  # Non-existent ID
        assert response.status_code == 404

    def test_update_pet_positive(self, api, sample_pet_data):
        # First create a pet
        api.create_pet(sample_pet_data)
        # Then update it
        updated_data = sample_pet_data.copy()
        updated_data["name"] = "updated_doggie"
        response = api.update_pet(updated_data)
        assert response.status_code == 200
        assert response.json()["name"] == "updated_doggie"

    def test_update_pet_negative(self, api):
        invalid_data = {"invalid": "data"}
        response = api.update_pet(invalid_data)
        assert response.status_code == 500

    def test_delete_pet_positive(self, api, sample_pet_data):
        # First create a pet
        api.create_pet(sample_pet_data)
        # Then delete it
        response = api.delete_pet(sample_pet_data["id"])
        assert response.status_code == 200
        # Verify it's deleted
        get_response = api.get_pet(sample_pet_data["id"])
        assert get_response.status_code == 404

    def test_delete_pet_negative(self, api):
        response = api.delete_pet(999999)  # Non-existent ID
        assert response.status_code == 404

    def test_find_pets_by_status_positive(self, api):
        response = api.find_pets_by_status("available")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_find_pets_by_status_negative(self, api):
        response = api.find_pets_by_status("invalid_status")
        assert response.status_code == 400
