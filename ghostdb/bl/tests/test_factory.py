import pytest
from unittest.mock import Mock

from ghostdb.bl.factory import BLFactory
from ghostdb.bl.actions import (
    corporation as corp_act, business as business_act, provider as provider_act,
    client as client_act, pet as pet_act, order as order_act, code as code_act
)
from ghostdb.bl.selectors import (
    corporation as corp_selectors, business as business_selectors,
    provider as provider_selectors, client as client_selectors, pet as pet_selectors,
    order as order_selectors, code as code_selectors
)


@pytest.mark.parametrize(
    'model_path, action_class, selector_class',
    (
        ('ghostdb.db.models.corporation.Corporation', corp_act.CorporationAction, corp_selectors.CorporationSelector),
        ('ghostdb.db.models.business.Business', business_act.BusinessAction, business_selectors.BusinessSelector),
        ('ghostdb.db.models.provider.Provider', provider_act.ProviderAction, provider_selectors.ProviderSelector),
        (
            'ghostdb.db.models.provider.ProviderKind',
            provider_act.ProviderKindAction,
            provider_selectors.ProviderKindSelector
        ),
        ('ghostdb.db.models.client.Client', client_act.ClientAction, client_selectors.ClientSelector),
        ('ghostdb.db.models.pet.Pet', pet_act.PetAction, pet_selectors.PetSelector),
        ('ghostdb.db.models.pet.Breed', pet_act.BreedAction, pet_selectors.BreedSelector),
        ('ghostdb.db.models.pet.Color', pet_act.ColorAction, pet_selectors.ColorSelector),
        ('ghostdb.db.models.pet.Gender', pet_act.GenderAction, pet_selectors.GenderSelector),
        ('ghostdb.db.models.pet.Species', pet_act.SpeciesAction, pet_selectors.SpeciesSelector),
        ('ghostdb.db.models.pet.WeightUnit', pet_act.WeightUnitAction, pet_selectors.WeightUnitSelector),
        ('ghostdb.db.models.order.Order', order_act.OrderAction, order_selectors.OrderSelector),
        ('ghostdb.db.models.code.RevenueCenter', code_act.RevenueCenterAction, code_selectors.RevenueCenterSelector),
        ('ghostdb.db.models.code.Department', code_act.DepartmentAction, code_selectors.DepartmentSelector),
        ('ghostdb.db.models.code.Category', code_act.CategoryAction, code_selectors.CategorySelector),
        ('ghostdb.db.models.code.Class', code_act.ClassAction, code_selectors.ClassSelector),
        ('ghostdb.db.models.code.SubClass', code_act.SubClassAction, code_selectors.SubClassSelector),
        ('ghostdb.db.models.code.ServiceType', code_act.ServiceTypeAction, code_selectors.ServiceTypeSelector),
        ('ghostdb.db.models.code.Service', code_act.ServiceAction, code_selectors.ServiceSelector),
    )
)
def test_get_bl_classes_by_model(model_path, action_class, selector_class):
    bl = BLFactory(model_path)

    assert bl.get_action_class() == action_class
    assert bl.get_selector_class() == selector_class


def test_get_bl_instance_by_model():
    dbsession = Mock()
    customer = 'test-customer'
    event_bus = Mock()

    bl = BLFactory(
        'ghostdb.db.models.corporation.Corporation',
        dbsession=dbsession,
        customer=customer,
        event_bus=event_bus
    )

    action = bl.action
    assert action.db == dbsession
    assert action.event_bus == event_bus

    assert bl.selector.db == dbsession
