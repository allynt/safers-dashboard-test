from enum import Enum


class ProfileDirection(str, Enum):

    LOCAL_TO_REMOTE = "local_to_remote"
    REMOTE_TO_LOCAL = "remote_to_local"


def reshape_profile_data(data: dict, direction: ProfileDirection | str) -> dict:
    """
    Reshapes the response from the gateway to something suitable for
    UserSerializer, and vice-versa.
    """
    if direction == ProfileDirection.REMOTE_TO_LOCAL:
        user_data = data["profile"]["user"]
        organization_data = data["profile"].get("organization")
        reshaped_data = {
            "auth_id":
                user_data["id"],
            "email":
                user_data["email"],
            "username":
                user_data["username"],
            "organization_name":
                organization_data["name"] if organization_data else None,
            "role_name":
                next(iter(user_data["roles"]), None),
            "profile": {
                "first_name": user_data["firstName"],
                "last_name": user_data["lastName"],
            }
        }

    elif direction == ProfileDirection.LOCAL_TO_REMOTE:
        role = data["role"]
        organization = data["organization"]
        # team = data["team"]
        reshaped_data = {
            "user": {
                "id": str(data["auth_id"]),
                "email": data["email"],
                "username": data["username"],
                "firstName": data["profile"]["first_name"],
                "lastName": data["profile"]["last_name"],
                "roles": [role.name if role else None],
            },
            "organizationId": organization.id if organization else None,
            # "teamId": team.id if team else None,
        }
    else:
        raise ValueError(f"Unknown ProfileDirection: '{direction}'.")

    return reshaped_data
