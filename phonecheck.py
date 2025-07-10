import phonenumbers
import httpx

async def check_phone(number: str):
    try:
        parsed = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed):
            return {"valid": False, "reason": "Неверный номер"}

        country = phonenumbers.region_code_for_number(parsed)
        formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        # Проверка через Cleantalk
        url = f"https://cleantalk.org/blacklists/{formatted.replace(' ', '')}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            is_spammer = "listed in database" in resp.text

        return {
            "valid": True,
            "formatted": formatted,
            "country": country,
            "spammer": is_spammer
        }

    except Exception as e:
        return {"valid": False, "reason": str(e)}
