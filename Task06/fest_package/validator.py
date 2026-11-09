from dataclasses import dataclass

@dataclass
class Registration:
    register: str
    name: str
    department: str
    email: str
    events: set

class InvalidRegistration(ValueError):
    pass

def valid_email(value):
    """Simple validation using string methods (as required by the task)."""
    value = value.strip()
    if not value or any(ch.isspace() for ch in value):
        return False
    if value.count("@") != 1:
        return False
    local, domain = value.split("@")
    if not local or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    return True

def parse_registration(line, source_department):
    # Format: register|name|department|email|event1;event2
    fields = [part.strip() for part in line.split("|")]
    if len(fields) != 5:
        raise InvalidRegistration(f"expected 5 pipe-separated fields, found {len(fields)}")
    register, name, department, email, event_text = fields
    if not register or not name or not department:
        raise InvalidRegistration("register, name and department are required")
    if department.lower() != source_department.lower():
        raise InvalidRegistration(
            f"department field {department!r} does not match source {source_department!r}"
        )
    if not valid_email(email):
        raise InvalidRegistration(f"invalid email address {email!r}")
    events = {event.strip() for event in event_text.split(";") if event.strip()}
    if not events:
        raise InvalidRegistration("at least one event is required")
    return Registration(register, name, department, email.lower(), events)
