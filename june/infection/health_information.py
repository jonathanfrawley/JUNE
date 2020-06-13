from june.infection.symptoms import SymptomTag

class HealthInformation:
    __slots__ = (
        "susceptibility",
        "susceptible",
        "infected",
        "infection",
        "recovered",
        "dead",
        "number_of_infected",
        "maximal_symptoms",
        "maximal_symptoms_time",
        "maximal_symptoms_tag",
        "time_of_infection",
        "time_of_symptoms_onset",
        "length_of_infection",
        "infecter",
    )

    def __init__(self):
        self.susceptibility = 1.0
        self.susceptible = True
        self.infected = False
        self.infection = None
        self.recovered = False
        self.dead = False
        self.number_of_infected = 0
        self.maximal_symptoms = 0
        self.maximal_symptoms_time = -1
        self.maximal_symptoms_tag = None
        self.time_of_infection = -1
        self.length_of_infection = -1
        self.infecter = None

    def set_infection(self, infection):
        self.infection = infection
        self.infected = True
        self.susceptible = False
        self.susceptibility = 0.0
        self.time_of_infection = infection.start_time
        if infection.symptoms.time_symptoms_onset():
            self.time_of_symptoms_onset = self.time_of_infection + infection.symptoms.time_symptoms_onset()

    @property
    def tag(self):
        if self.infection is not None:
            return self.infection.symptoms.tag
        return None

    @property
    def must_stay_at_home(self) -> bool:
        return self.tag in (SymptomTag.influenza, SymptomTag.pneumonia)

    @property
    def should_be_in_hospital(self) -> bool:
        return self.tag in (SymptomTag.hospitalised, SymptomTag.intensive_care)

    @property
    def infected_at_home(self) -> bool:
        return self.infected and not (self.dead or self.should_be_in_hospital)

    @property
    def is_dead(self) -> bool:
        return self.tag == SymptomTag.dead

    def update_health_status(self, time, delta_time):
         self.infection.update_at_time(time + delta_time)
         #if self.infection.symptoms.symtpoms_onset():
         #    self.symptoms_onset = symptoms_onset
         if self.infection.symptoms.is_recovered():
            self.recovered = True


    def set_recovered(self, time):
        self.recovered = True
        self.infected = False
        self.susceptible = False
        self.susceptibility = 0.0
        self.set_length_of_infection(time)
        self.infection = None

    def set_dead(self, time):
        self.dead = True
        self.infected = False
        self.susceptible = False
        self.susceptibility = 0.0
        self.set_length_of_infection(time)
        self.infection = None

    def get_symptoms_tag(self, symptoms):
        return self.infection.symptoms.tag

    def transmission_probability(self, time):
        if self.infection is not None:
            return 0.0
        return self.infection.transmission_probability(time)

    def symptom_severity(self, severity):
        if self.infection is None:
            return 0.0
        return self.infection.symptom_severity(severity)

    def update_symptoms(self, time):  # , symptoms, time):
        if self.infection.symptoms.severity > self.maximal_symptoms:
            self.maximal_symptoms = self.infection.symptoms.severity
            self.maximal_symptoms_tag = self.get_symptoms_tag(self.infection.symptoms)
            self.maximal_symptoms_time = time - self.time_of_infection

    def set_length_of_infection(self, time):
        self.length_of_infection = time - self.time_of_infection

