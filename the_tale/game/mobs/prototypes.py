# -*- coding: utf-8 -*-
from game.heroes.habilities import AbilitiesPrototype

from game.balance import formulas as f
from game.game_info import ATTRIBUTES

class MobException(Exception): pass


class MobPrototype(object):

    def __init__(self, record=None, level=None, health=None, abilities=None):

        self.record = record
        self.level = level
        self.abilities = AbilitiesPrototype(abilities=record.abilities) if abilities is None else abilities

        self.initiative = self.abilities.modify_attribute(ATTRIBUTES.INITIATIVE, 1)
        self.health_cooficient = self.abilities.modify_attribute(ATTRIBUTES.HEALTH, 1)
        self.damage_cooficient = self.abilities.modify_attribute(ATTRIBUTES.DAMAGE, 1)

        self.max_health = f.mob_hp_to_lvl(level) * self.health_cooficient

        self.health = self.max_health if health is None else health


    @property
    def id(self): return self.record.id

    @property
    def name(self): return self.record.name

    @property
    def normalized_name(self): return (self.record.normalized_name, self.record.morph)

    @property
    def loot(self): return self.record.loot

    @property
    def artifacts(self): return self.record.artifacts

    @property
    def health_percents(self): return float(self.health) / self.max_health

    @property
    def exp_cooficient(self): return f.mob_difficulty(self.initiative, self.health_cooficient, self.damage_cooficient)

    @property
    def basic_damage(self): return f.expected_damage_to_hero_per_hit(self.level) * self.damage_cooficient

    def strike_by(self, percents):
        self.health = max(0, self.health - self.max_health * percents)

    def kill(self):
        pass

    def get_loot(self):
        from ..artifacts.storage import ArtifactsDatabase
        return ArtifactsDatabase.storage().generate_loot(self.artifacts, self.loot, artifact_level=self.level, loot_level=self.record.level)

    def serialize(self):
        return {'level': self.level,
                'id': self.id,
                'health': self.health,
                'abilities': self.abilities.serialize()}

    @classmethod
    def deserialize(cls, storage, data):
        return cls(record=storage.data[data['id']],
                   level=data['level'],
                   health=data['health'],
                   abilities=AbilitiesPrototype.deserialize(data['abilities']))

    def ui_info(self):
        return { 'name': self.name,
                 'health': self.health_percents }


    def __eq__(self, other):
        return (self.id == other.id and
                self.level == other.level and
                self.max_health == other.max_health and
                self.health == other.health and
                self.abilities == other.abilities)
