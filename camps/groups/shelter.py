import numpy as np
from enum import IntEnum

from june.groups import Group, Supergroup, Households, Household


class Shelter(Group):
    class SubgroupType(IntEnum):
        household_1 = 1
        household_2 = 2

    def __init__(self):
        super().__init__()

    def add(self, household: Household):
        if not isinstance(household, Household):
            raise ValueError("Shelters want households added to them, not people.")
        if len(household.people) == 0:
            raise ValueError("Adding an empty household to a shelter is not supported.")
        if len(self.subgroups[0].people) == 0:
            for person in household.people:
                self.subgroups[0].append(person)
                setattr(person.subgroups, "residence", self[0])
        elif len(self.subgroups[1].people) == 0:
            for person in household.people:
                self.subgroups[1].append(person)
                setattr(person.subgroups, "residence", self[1])
        else:
            raise ValueError("Shelter full!")

    @property
    def families(self):
        return [subgroup for subgroup in self.subgroups if len(subgroup) != 0]

    @property
    def households(self):
        return [subgroup for subgroup in self.subgroups if len(subgroup) != 0]

    @property
    def n_families(self):
        return len(self.families)

    @property
    def n_households(self):
        return len(self.families)


class Shelters(Supergroup):
    def __init__(self, shelters):
        super().__init__()
        self.members = shelters

    @classmethod
    def from_families_in_area(cls, n_families_area, sharing_shelter_ratio=0.75):
        n_shelters_multi = int(np.floor(sharing_shelter_ratio * n_families_area / 2))
        n_shelters = n_families_area - n_shelters_multi
        shelters = [Shelter() for _ in range(n_shelters)]
        return cls(shelters)


class ShelterDistributor:
    def __init__(self, sharing_shelter_ratio=0.75):
        self.sharing_shelter_ratio = sharing_shelter_ratio

    def distribute_people_in_shelters(self, shelters: Shelters, households: Households):
        households_idx = np.arange(0, len(households))
        np.random.shuffle(households_idx)
        households_idx = list(households_idx)
        multifamily_shelters = int(
            np.floor(self.sharing_shelter_ratio * len(households) / 2)
        )
        for i in range(multifamily_shelters):
            shelter = shelters[i]
            shelter.add(households[households_idx.pop()])
            shelter.add(households[households_idx.pop()])
        i += 1
        while households_idx:
            i = i % len(shelters)
            shelter = shelters[i]
            shelter.add(households[households_idx.pop()])
            i += 1
