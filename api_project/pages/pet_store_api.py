import requests
from typing import Dict, Any


class PetStoreAPI:
    BASE_URL = "https://petstore.swagger.io/v2"
    
    def __init__(self):
        self.session = requests.Session()
    
    def create_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """Create a new pet"""
        return self.session.post(f"{self.BASE_URL}/pet", json=pet_data)
    
    def get_pet(self, pet_id: int) -> requests.Response:
        """Get pet by ID"""
        return self.session.get(f"{self.BASE_URL}/pet/{pet_id}")
    
    def update_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """Update an existing pet"""
        return self.session.put(f"{self.BASE_URL}/pet", json=pet_data)
    
    def delete_pet(self, pet_id: int) -> requests.Response:
        """Delete a pet"""
        return self.session.delete(f"{self.BASE_URL}/pet/{pet_id}")
    
    def find_pets_by_status(self, status: str) -> requests.Response:
        """Find pets by status"""
        return self.session.get(f"{self.BASE_URL}/pet/findByStatus", params={"status": status})
