from pytest import fixture, mark
from typing import Iterator
from xsdata_ech.e_ch_0155_5_0 import (
    ElectionDescriptionInformationType,
    TypeOfElectionType,
)
from xsdata_ech.e_ch_0252_2_0 import (
    CandidateType,
    CountOfVotersInformationType,
    Delivery,
    DomainOfInfluenceType,
    DomainOfInfluenceTypeType,
    ElectionGroupInfoType,
    ElectionType,
    EventElectionInformationDeliveryType,
    SexType
)
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import JsonParser, XmlParser
from xsdata.formats.dataclass.serializers import JsonSerializer, XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate


SubtotalInfo = CountOfVotersInformationType.SubtotalInfo
ElectionGroup = ElectionGroupInfoType.ElectionGroup
ElectionInformation = ElectionGroup.ElectionInformation
ElectionDescriptionInfo = \
    ElectionDescriptionInformationType.ElectionDescriptionInfo


@fixture()
def delivery() -> Iterator[Delivery]:
    description = ElectionDescriptionInformationType(
        election_description_info=[
            ElectionDescriptionInfo(
                language='de',
                election_description='Title de',
                election_description_short='Short Title de'
            ),
            ElectionDescriptionInfo(
                language='fr',
                election_description='Title fr',
                election_description_short='Short Title fr'
            ),
            ElectionDescriptionInfo(
                language='it',
                election_description='Title it',
                election_description_short='Short Title it'
            ),
            ElectionDescriptionInfo(
                language='rm',
                election_description='Title rm',
                election_description_short='Short Title rm'
            )
        ]
    )

    yield Delivery(
        election_information_delivery=EventElectionInformationDeliveryType(
            canton_id=1,
            polling_day=XmlDate(2023, 1, 1),
            number_of_entries=1,
            election_group_info=[
                ElectionGroupInfoType(
                    election_group=ElectionGroup(
                        domain_of_influence=DomainOfInfluenceType(
                            domain_of_influence_type=DomainOfInfluenceTypeType(
                                DomainOfInfluenceTypeType.CT
                            ),
                            domain_of_influence_identification='18',
                            domain_of_influence_name='Kanton Graubünden'
                        ),
                        election_information=[
                            ElectionInformation(
                                election=ElectionType(
                                    election_identification='election-id',
                                    type_of_election=(
                                        TypeOfElectionType.VALUE_2
                                    ),
                                    number_of_mandates=1,
                                    election_description=description
                                ),
                                candidate=[
                                    CandidateType(
                                        candidate_identification='10.10',
                                        family_name='Power',
                                        first_name='Peter',
                                        date_of_birth=XmlDate(1900, 1, 1),
                                        sex=SexType.VALUE_1
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        ),
    )


def test_ech_0252_majorz_election_information_xml(delivery: Delivery) -> None:
    # to xml
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    xml = serializer.render(delivery)

    # from xml
    parser = XmlParser(context=XmlContext())
    parsed: Delivery = parser.from_string(xml)
    assert delivery == parsed


@mark.skip('xsdata messes up class inference')
def test_ech_0252_majorz_election_information_json(delivery: Delivery) -> None:
    # to json
    config = SerializerConfig(pretty_print=True)
    serializer = JsonSerializer(config=config)
    json = serializer.render(delivery)
    print(json)

    # from json
    parser = JsonParser(context=XmlContext())
    parsed: Delivery = parser.from_string(json)
    assert delivery == parsed
