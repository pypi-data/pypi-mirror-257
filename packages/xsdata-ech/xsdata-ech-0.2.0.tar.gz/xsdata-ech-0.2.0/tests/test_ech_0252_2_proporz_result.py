from pytest import fixture
from typing import Iterator
from xsdata_ech.e_ch_0252_2_0 import (
    CandidateListResultType,
    CountingCircleResultType,
    CountOfVotersInformationType,
    Delivery,
    ElectionResultType,
    ElectedType,
    EventElectionResultDeliveryType,
    ListResultType,
    VoterTypeType
)
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import JsonParser, XmlParser
from xsdata.formats.dataclass.serializers import JsonSerializer, XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDate

SubtotalInfo = CountOfVotersInformationType.SubtotalInfo
ElectionGroupResult = EventElectionResultDeliveryType.ElectionGroupResult
ElectionResult = ElectionGroupResult.ElectionResult
ProportionalElectionResult = ElectionResultType.ProportionalElection
ProportionalElectionElected = ElectedType.ProportionalElection
ElectedCandidate = ProportionalElectionElected.ListType.ElectedCandidate
CandidateResults = ListResultType.CandidateResults
CandidateListResultsInfo = CandidateResults.CandidateListResultsInfo


@fixture()
def delivery() -> Iterator[Delivery]:
    candidate_list_results_info = CandidateListResultsInfo(
        candidate_list_results=[
            CandidateListResultType(
                list_identification='list-id',
                count_of_votes_from_changed_ballots=0
            )
        ],
        count_of_votes_from_ballots_without_list_designation=0,
    )
    proportional_election = ProportionalElectionResult(
        count_of_changed_ballots_without_list_designation=0,
        count_of_empty_votes_of_changed_ballots_without_list_designation=0,
        list_results=[
            ListResultType(
                list_identification='list-id',
                count_of_changed_ballots=0,
                count_of_unchanged_ballots=0,
                count_of_candidate_votes=0,
                count_of_additional_votes=0,
                candidate_results=[
                    CandidateResults(
                        candidate_identification='candidate-id',
                        count_of_votes_from_changed_ballots=0,
                        count_of_votes_from_unchanged_ballots=0,
                        candidate_list_results_info=candidate_list_results_info
                    )
                ]
            )
        ]
    )
    counting_circle_result = [
        CountingCircleResultType(
            counting_circle_id='3901',
            count_of_voters_information=(
                CountOfVotersInformationType(
                    count_of_voters_total=100,
                    subtotal_info=[
                        SubtotalInfo(
                            count_of_voters=100,
                            voter_type=(
                                VoterTypeType.VALUE_2
                            ),
                        )
                    ]
                )
            ),
            fully_counted_true=True,
            count_of_received_ballots=100,
            count_of_blank_ballots=1,
            count_of_invalid_ballots=2,
            count_of_valid_ballots=97,
            election_result=ElectionResultType(
                election_identification='election-id',
                proportional_election=proportional_election
            )
        )
    ]

    # todo:
    elected = ElectedType(
        proportional_election=ProportionalElectionElected(
            list_value=[
                ProportionalElectionElected.ListType(
                    list_identification='list-id',
                    count_of_seats_gained=1,
                    elected_candidate=[
                        ElectedCandidate(
                            candidate_identification="candidate-id",
                        )
                    ]
                )
            ]
        )
    )

    yield Delivery(
        election_result_delivery=EventElectionResultDeliveryType(
            canton_id=1,
            polling_day=XmlDate(2023, 1, 1),
            number_of_entries=1,
            election_group_result=[
                ElectionGroupResult(
                    election_group_identification='group-id',
                    election_result=[
                        ElectionResult(
                            election_identification='election-id',
                            counting_circle_result=counting_circle_result,
                            elected=elected
                        )
                    ]
                )
            ]

        )
    )


def test_ech_0252_proporz_election_result_xml(delivery: Delivery) -> None:
    # to xml
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    xml = serializer.render(delivery)

    # from xml
    parser = XmlParser(context=XmlContext())
    parsed: Delivery = parser.from_string(xml)
    assert delivery == parsed


def test_ech_0252_proporz_election_result_json(delivery: Delivery) -> None:
    # to json
    config = SerializerConfig(pretty_print=True)
    serializer = JsonSerializer(config=config)
    json = serializer.render(delivery)

    # from json
    parser = JsonParser(context=XmlContext())
    parsed: Delivery = parser.from_string(json)
    assert delivery == parsed
