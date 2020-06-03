from collections import namedtuple

from ghostdb.db.models.client import Client
from ghostdb.db.models.pet import Pet, PetOwner
from ghostdb.db.models.corporation import Corporation
from ghostdb.db.models.business import Business
from ..data_dumper import GenericDataDumper, RelationDataDumper


class TestGenericDataDumper:

    def test_get_modified_keys(self):
        key1 = 'field1'
        key2 = 'field2'

        attrs = {key1, key2}
        unmodified = {key2}
        State = namedtuple('State', 'attrs, unmodified')
        StateAttrs = namedtuple('StateAttrs', 'key')

        state = State(
            attrs=[StateAttrs(key=key1), StateAttrs(key=key2)],
            unmodified=unmodified
        )

        test_modified_keys = GenericDataDumper.get_modified_keys(state)
        expected_keys = attrs ^ unmodified

        assert test_modified_keys == expected_keys

    def test_get_modified_data(self, dbsession):

        # create pet with name Nick and weight 1
        pet = Pet(name='Nick', weight=1)
        data_dump = GenericDataDumper(pet).get_modified_data()
        assert data_dump == {
            'name': 'Nick',
            'weight': 1
        }

        # commit pet to db
        # modified data will be empty
        dbsession.add(pet)
        dbsession.commit()
        data_dump = GenericDataDumper(pet).get_modified_data()
        assert data_dump == {}

        # change weight to 2
        pet.weight = 2
        data_dump = GenericDataDumper(pet).get_modified_data()
        assert data_dump == {
            'weight': 2
        }

    def test_get_pms_ids_data(self):
        # create object without pms_ids
        corporation = Corporation(name='VIS')
        assert not getattr(corporation, 'pms_ids', None)
        data_dump = GenericDataDumper(corporation).get_pms_ids_data()
        assert data_dump == {}

        # create object with pms_ids
        business = Business(name='Antlers and Hooves', pms_ids=1)
        data_dump = GenericDataDumper(business).get_pms_ids_data()
        assert getattr(business, 'pms_ids', None)
        assert data_dump == {
            'pms_ids': 1
        }

        # change object, anyway must get pms_ids
        business.country = 'USE'
        data_dump = GenericDataDumper(business).get_pms_ids_data()
        assert data_dump == {
            'pms_ids': 1
        }

    def test_get_data_dump(self, monkeypatch):
        modified_data = {'test1': 'test'}
        pms_ids_data = {'test2': 'test'}
        monkeypatch.setattr(GenericDataDumper, 'get_modified_data', lambda self: modified_data)
        monkeypatch.setattr(GenericDataDumper, 'get_pms_ids_data', lambda self: pms_ids_data)
        pet = Pet(name='Nick')
        data_dump = GenericDataDumper(pet).get_data_dump()
        modified_data.update(pms_ids_data)
        assert data_dump == modified_data


class TestRelationDataDumper:

    def test_dump_relation_one_to_one(self, dbsession):
        corporation = Corporation(name='FooBar Inc')
        business = Business(name='BarBaz', corporation=corporation, display_name='BarBaz')
        dbsession.add(corporation)
        dbsession.add(business)
        dbsession.commit()

        business.name = 'FooBaz'
        dump = RelationDataDumper(business, pk_fields=('corporation_id', )).get_data_dump()

        assert dump == {'name': 'FooBaz', 'corporation_id': corporation.id.hex}

    def test_dump_relation_many_to_many(self, dbsession):
        client1 = Client(first_name="A")
        client2 = Client(first_name="B")

        pet = Pet(name="Bobik")

        pet_owner_1 = PetOwner(pet=pet, client=client1)
        pet_owner_2 = PetOwner(pet=pet, client=client2)

        dbsession.add(client1)
        dbsession.add(client2)
        dbsession.add(pet)
        dbsession.add(pet_owner_1)
        dbsession.add(pet_owner_2)
        dbsession.commit()

        dump = RelationDataDumper(pet, pk_fields=('owners', )).get_data_dump()

        assert sorted(dump["owners"]) == sorted([client1.id.hex, client2.id.hex, ])
