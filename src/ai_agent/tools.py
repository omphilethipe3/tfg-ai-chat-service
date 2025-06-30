import httpx
from src.config.settings import settings

client = httpx.Client(timeout=5.0)

def get_person_address(person_id: str) -> dict:
    """
    Fetches the address for a given person from the Domain API.
    """
    url = f"{settings.domain_api_base_url}/persons/{person_id}/address"
    resp = httpx.get(url)
    resp.raise_for_status()
    return resp.json()

def check_credit_customer(person_id: str) -> bool:
    """
    Checks if a person is a credit customer.
    """
    url = f"{settings.domain_api_base_url}/customers/{person_id}/credit-status"
    resp = httpx.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("isCreditCustomer", False)