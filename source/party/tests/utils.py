from party.models import Party


def create_party(**kwargs) -> Party:
    members = kwargs.pop('members', [])
    party = Party.objects.create(**kwargs)
    if members:
        party.members.set(members)
    return party
