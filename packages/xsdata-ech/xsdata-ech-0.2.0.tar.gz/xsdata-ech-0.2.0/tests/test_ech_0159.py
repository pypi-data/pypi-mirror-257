from pytest import fixture
from typing import Iterator
from xsdata_ech.e_ch_0058_5_0 import ActionType, SendingApplicationType
from xsdata_ech.e_ch_0155_5_0 import (
    DomainOfInfluenceType,
    DomainOfInfluenceTypeType,
    ElectronicBallotQuestionType,
    TieBreakQuestionType
)
from xsdata_ech.e_ch_0159_5_0 import (
    ContestType,
    Delivery,
    ElectronicBallotType,
    EventInitialDelivery,
    HeaderType,
    VoteType
)
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import JsonParser, XmlParser
from xsdata.formats.dataclass.serializers import JsonSerializer, XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate, XmlDateTime


VoteInformation = EventInitialDelivery.VoteInformation
StandardElectronicBallot = ElectronicBallotType.StandardElectronicBallot
VariantElectronicBallot = ElectronicBallotType.VariantElectronicBallot
ElectronicBallotQuestionInfo = \
    ElectronicBallotQuestionType.ElectronicBallotQuestionInfo
QuestionInformation = VariantElectronicBallot.QuestionInformation
TieBreakInformation = VariantElectronicBallot.TieBreakInformation
TieBreakQuestionInfo = TieBreakQuestionType.TieBreakQuestionInfo


@fixture()
def delivery() -> Iterator[Delivery]:
    standard_ballot = StandardElectronicBallot(
        question_identification='question-1-id',
        electronic_ballot_question=ElectronicBallotQuestionType(
            electronic_ballot_question_info=[
                ElectronicBallotQuestionInfo(
                    language='de',
                    electronic_ballot_question_title='Title 1 DE',
                    electronic_ballot_question='Question 1 DE',
                ),
                ElectronicBallotQuestionInfo(
                    language='fr',
                    electronic_ballot_question_title='Title 1 FR',
                    electronic_ballot_question='Question 1 FR',
                ),
                ElectronicBallotQuestionInfo(
                    language='it',
                    electronic_ballot_question_title='Title 1 IT',
                    electronic_ballot_question='Question 1 IT',
                ),
                ElectronicBallotQuestionInfo(
                    language='rm',
                    electronic_ballot_question_title='Title 1 RM',
                    electronic_ballot_question='Question 1 RM',
                ),
            ]
        ),
    )

    variant_ballot = VariantElectronicBallot(
        question_information=[
            QuestionInformation(
                question_identification='question-2-1-id',
                electronic_ballot_question=ElectronicBallotQuestionType(
                    electronic_ballot_question_info=[
                        ElectronicBallotQuestionInfo(
                            language='de',
                            electronic_ballot_question_title='Title 2-1 DE',
                            electronic_ballot_question='Question 2-1 DE',
                        ),
                        ElectronicBallotQuestionInfo(
                            language='fr',
                            electronic_ballot_question_title='Title 2-1 FR',
                            electronic_ballot_question='Question 2-1 FR',
                        ),
                        ElectronicBallotQuestionInfo(
                            language='it',
                            electronic_ballot_question_title='Title 2-1 IT',
                            electronic_ballot_question='Question 2-1 IT',
                        ),
                        ElectronicBallotQuestionInfo(
                            language='rm',
                            electronic_ballot_question_title='Title 2-1 RM',
                            electronic_ballot_question='Question 2-1 RM',
                        ),
                    ]
                ),
            ),
            QuestionInformation(
                question_identification='question-2-2-id',
                electronic_ballot_question=ElectronicBallotQuestionType(
                    electronic_ballot_question_info=[
                        ElectronicBallotQuestionInfo(
                            language='de',
                            electronic_ballot_question_title='Title 2-2 DE',
                            electronic_ballot_question='Question 2-2 DE',
                        ),
                        ElectronicBallotQuestionInfo(
                            language='fr',
                            electronic_ballot_question_title='Title 2-2 FR',
                            electronic_ballot_question='Question 2-2 FR',
                        ),
                        ElectronicBallotQuestionInfo(
                            language='it',
                            electronic_ballot_question_title='Title 2-2 IT',
                            electronic_ballot_question='Question 2-2 IT',
                        ),
                        ElectronicBallotQuestionInfo(
                            language='rm',
                            electronic_ballot_question_title='Title 2-2 RM',
                            electronic_ballot_question='Question 2-2 RM',
                        ),
                    ]
                ),
            ),
        ],
        tie_break_information=[
            TieBreakInformation(
                question_identification='question-2-3-id',
                tie_break_question=TieBreakQuestionType(
                    tie_break_question_info=[
                        TieBreakQuestionInfo(
                            language='de',
                            tie_break_question_title='Title 2-3 DE',
                            tie_break_question='Question 2-3 DE',
                        ),
                        TieBreakQuestionInfo(
                            language='fr',
                            tie_break_question_title='Title 2-3 FR',
                            tie_break_question='Question 2-3 FR',
                        ),
                        TieBreakQuestionInfo(
                            language='it',
                            tie_break_question_title='Title 2-3 IT',
                            tie_break_question='Question 2-3 IT',
                        ),
                        TieBreakQuestionInfo(
                            language='rm',
                            tie_break_question_title='Title 2-3 RM',
                            tie_break_question='Question 2-3 RM',
                        ),
                    ]
                )
            )
        ]
    )

    yield Delivery(
        delivery_header=HeaderType(
            sender_id='sender-id',
            message_id='62fdee70d9ea77646f6e8686a3f9332e',
            message_type='message-type',
            sending_application=SendingApplicationType(
                manufacturer='manufacturer',
                product='product',
                product_version='1.0'
            ),
            message_date=XmlDateTime(2023, 1, 1, 12, 0, 0),
            action=ActionType.VALUE_1,
            test_delivery_flag=True
        ),
        initial_delivery=EventInitialDelivery(
            contest=ContestType(
                contest_identification='contest-id',
                contest_date=XmlDate(2023, 6, 6),
            ),
            vote_information=[
                VoteInformation(
                    vote=VoteType(
                        vote_identification='vote-1',
                        domain_of_influence=DomainOfInfluenceType(
                            domain_of_influence_type=DomainOfInfluenceTypeType(
                                DomainOfInfluenceTypeType.CT
                            ),
                            domain_of_influence_identification='GR',
                            domain_of_influence_name='Kanton Graubünden'
                        ),
                    ),
                    electronic_ballot=[
                        ElectronicBallotType(
                            electronic_ballot_identification='ballot-1-id',
                            electronic_ballot_position=1,
                            standard_electronic_ballot=standard_ballot
                        )
                    ]
                ),
                VoteInformation(
                    vote=VoteType(
                        vote_identification='vote-2',
                        domain_of_influence=DomainOfInfluenceType(
                            domain_of_influence_type=DomainOfInfluenceTypeType(
                                DomainOfInfluenceTypeType.CT
                            ),
                            domain_of_influence_identification='GR',
                            domain_of_influence_name='Kanton Graubünden'
                        ),
                    ),
                    electronic_ballot=[
                        ElectronicBallotType(
                            electronic_ballot_identification='ballot-2-id',
                            electronic_ballot_position=1,
                            variant_electronic_ballot=variant_ballot,
                        )
                    ]
                )
            ]
        ),
    )


def test_ech_0159_xml(delivery: Delivery) -> None:
    # to xml
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    xml = serializer.render(delivery)

    # from xml
    parser = XmlParser(context=XmlContext())
    parsed: Delivery = parser.from_string(xml)
    assert delivery == parsed


def test_ech_0159_json(delivery: Delivery) -> None:
    # to json
    config = SerializerConfig(pretty_print=True)
    serializer = JsonSerializer(config=config)
    json = serializer.render(delivery)

    # from json
    parser = JsonParser(context=XmlContext())
    parsed: Delivery = parser.from_string(json)
    # FIXME: Some (inherited) classes seem to be sometimes parsed wrong
    # (Header instead of HeaderType, Contest instead of ContestType)
    parsed.delivery_header.__class__ = HeaderType
    assert parsed.initial_delivery is not None
    parsed.initial_delivery.contest.__class__ = ContestType
    assert delivery == parsed
