from pytest import fixture, mark
from typing import Iterator
from xsdata_ech.e_ch_0155_5_0 import (
    CandidatePositionInformationType,
    CandidateTextInformationType,
    ElectionDescriptionInformationType,
    ListDescriptionInformationType,
    ListRelationType,
    ListUnionDescriptionType,
    PartyAffiliationInformationType,
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
    ListType,
    ListUnionType,
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
PartyAffiliationInfo = PartyAffiliationInformationType.PartyAffiliationInfo
ListDescriptionInfo = ListDescriptionInformationType.ListDescriptionInfo
CandidateTextInfo = CandidateTextInformationType.CandidateTextInfo
ListUnionDescriptionInfo = ListUnionDescriptionType.ListUnionDescriptionInfo


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
    candidate = CandidateType(
        candidate_identification='candidate-id',
        family_name='Power',
        first_name='Peter',
        date_of_birth=XmlDate(1900, 1, 1),
        sex=SexType.VALUE_1,
        party_affiliation=PartyAffiliationInformationType(
            party_affiliation_info=[
                PartyAffiliationInfo(
                    language='de',
                    party_affiliation_short='Party de'
                ),
                PartyAffiliationInfo(
                    language='fr',
                    party_affiliation_short='Party fr'
                ),
                PartyAffiliationInfo(
                    language='it',
                    party_affiliation_short='Party it'
                ),
                PartyAffiliationInfo(
                    language='rm',
                    party_affiliation_short='Party rm'
                ),
            ]
        )
    )
    list_value = ListType(
        list_identification='list-id',
        list_indenture_number='10',
        list_description=ListDescriptionInformationType(
            list_description_info=[
                ListDescriptionInfo(
                    language='de',
                    list_description='List de'
                ),
                ListDescriptionInfo(
                    language='fr',
                    list_description='List fr'
                ),
                ListDescriptionInfo(
                    language='it',
                    list_description='List it'
                ),
                ListDescriptionInfo(
                    language='rm',
                    list_description='List rm'
                ),
            ]
        ),
        is_empty_list=False,
        candidate_position=[
            CandidatePositionInformationType(
                position_on_list=10,
                candidate_identification='candidate-id',
                candidate_reference_on_position='10.10',
                candidate_text_on_position=CandidateTextInformationType(
                    candidate_text_info=[
                        CandidateTextInfo(
                            language='de',
                            candidate_text='Peter Power de'
                        ),
                        CandidateTextInfo(
                            language='fr',
                            candidate_text='Peter Power fr'
                        ),
                        CandidateTextInfo(
                            language='it',
                            candidate_text='Peter Power it'
                        ),
                        CandidateTextInfo(
                            language='rm',
                            candidate_text='Peter Power rm'
                        ),
                    ]
                )
            )
        ]
    )
    list_union = ListUnionType(
        list_union_identification='list-union-id',
        list_union_description=ListUnionDescriptionType(
            list_union_description_info=[
                ListUnionDescriptionInfo(
                    language='de',
                    list_union_description='List Union de'
                ),
                ListUnionDescriptionInfo(
                    language='fr',
                    list_union_description='List Union fr'
                ),
                ListUnionDescriptionInfo(
                    language='it',
                    list_union_description='List Union it'
                ),
                ListUnionDescriptionInfo(
                    language='rm',
                    list_union_description='List Union rm'
                ),
            ]
        ),
        list_union_type=ListRelationType.VALUE_1,
        referenced_list=['list-id'],
        referenced_list_union=None
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
                                candidate=[candidate],
                                list_value=[list_value],
                                list_union=[list_union]
                            )
                        ]
                    )
                )
            ]
        ),
    )


def test_ech_0252_proporz_election_information_xml(
    delivery: Delivery
) -> None:
    # to xml
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    xml = serializer.render(delivery)

    # from xml
    parser = XmlParser(context=XmlContext())
    parsed: Delivery = parser.from_string(xml)
    assert delivery == parsed


@mark.skip('xsdata messes up class inference')
def test_ech_0252_proporz_election_information_json(
    delivery: Delivery
) -> None:
    # to json
    config = SerializerConfig(pretty_print=True)
    serializer = JsonSerializer(config=config)
    json = serializer.render(delivery)
    print(json)

    # from json
    parser = JsonParser(context=XmlContext())
    parsed: Delivery = parser.from_string(json)
    assert delivery == parsed
