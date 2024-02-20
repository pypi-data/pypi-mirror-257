from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from xsdata_ech.e_ch_0044_4_1 import SexType as SexType
from xsdata_ech.e_ch_0058_5_0 import HeaderType as HeaderType
from xsdata_ech.e_ch_0155_5_0 import (
    CandidateType as ECh015550CandidateType,
    DomainOfInfluenceType as DomainOfInfluenceType,
    DomainOfInfluenceTypeType as DomainOfInfluenceTypeType,
    ElectionType as ElectionType,
    ExtensionType as ExtensionType,
    ListType as ListType,
    ListUnionType as ListUnionType,
    VoterTypeType as VoterTypeType,
)

__NAMESPACE__ = "http://www.ech.ch/xmlns/eCH-0252/2"


@dataclass
class CandidateListResultType:
    class Meta:
        name = "candidateListResultType"

    list_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "listIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    count_of_votes_from_changed_ballots: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotesFromChangedBallots",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )


class DecisiveMajorityType(Enum):
    VALUE_1 = 1  # Mehrheit der Stimmen
    VALUE_2 = 2  # Mehrheit der Gemeinden
    VALUE_3 = 3  # Alle Gemeinden / einstimmig
    VALUE_4 = 4  # Mehrheit der Stimmen und der Gemeinden
    VALUE_5 = 5  # Volks- und Ständemehr


@dataclass
class ElectionAssociationType:
    class Meta:
        name = "electionAssociationType"

    election_association_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "electionAssociationId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    election_association_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "electionAssociationName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    quorum: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": Decimal("0.00"),
            "max_inclusive": Decimal("100.00"),
            "total_digits": 5,
            "fraction_digits": 2,
        },
    )


@dataclass
class NamedElementType:
    class Meta:
        name = "namedElementType"

    element_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "elementName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 100,
        },
    )
    count_of: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOf",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    percent: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": Decimal("0.00"),
            "max_inclusive": Decimal("100.00"),
            "total_digits": 5,
            "fraction_digits": 2,
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 500,
        },
    )


@dataclass
class NamedIdType:
    class Meta:
        name = "namedIdType"

    id_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "idName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 20,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )


class VoteSubTypeType(Enum):
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6


@dataclass
class VoteTitleInformationType:
    class Meta:
        name = "voteTitleInformationType"

    language: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "length": 2,
        },
    )
    vote_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "voteTitle",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 700,
        },
    )
    vote_title_short: Optional[str] = field(
        default=None,
        metadata={
            "name": "voteTitleShort",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 300,
        },
    )


@dataclass
class VotingCardInformationType:
    class Meta:
        name = "votingCardInformationType"

    count_of_voting_cards_received_in_ballotbox: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedInBallotbox",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_voting_cards_received_prematurely_in_ballotbox: Optional[
        int
    ] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedPrematurelyInBallotbox",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_voting_cards_received_by_mail: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedByMail",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_invalid_voting_cards_received_by_mail: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfInvalidVotingCardsReceivedByMail",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_voting_cards_received_by_evoting: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotingCardsReceivedByEvoting",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )


@dataclass
class CandidateResultType:
    class Meta:
        name = "candidateResultType"

    candidate_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "candidateIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    count_of_votes_total: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotesTotal",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    candidate_list_results_info: Optional[
        "CandidateResultType.CandidateListResultsInfo"
    ] = field(
        default=None,
        metadata={
            "name": "candidateListResultsInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )

    @dataclass
    class CandidateListResultsInfo:
        candidate_list_results: List[CandidateListResultType] = field(
            default_factory=list,
            metadata={
                "name": "candidateListResults",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )
        count_of_votes_from_ballots_without_list_designation: Optional[
            int
        ] = field(
            default=None,
            metadata={
                "name": "countOfVotesFromBallotsWithoutListDesignation",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )


@dataclass
class CandidateType(ECh015550CandidateType):
    class Meta:
        name = "candidateType"

    political_family_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "politicalFamilyName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 100,
        },
    )
    political_first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "politicalFirstName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 100,
        },
    )


@dataclass
class CountOfVotersInformationType:
    class Meta:
        name = "countOfVotersInformationType"

    count_of_voters_total: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotersTotal",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    subtotal_info: List["CountOfVotersInformationType.SubtotalInfo"] = field(
        default_factory=list,
        metadata={
            "name": "subtotalInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )

    @dataclass
    class SubtotalInfo:
        count_of_voters: Optional[int] = field(
            default=None,
            metadata={
                "name": "countOfVoters",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        voter_type: Optional[VoterTypeType] = field(
            default=None,
            metadata={
                "name": "voterType",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )
        sex: Optional[SexType] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )


@dataclass
class CountingCircleType:
    class Meta:
        name = "countingCircleType"

    counting_circle_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "countingCircleId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 50,
        },
    )
    counting_circle_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "countingCircleName",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 100,
        },
    )
    domain_of_influence_type: Optional[DomainOfInfluenceTypeType] = field(
        default=None,
        metadata={
            "name": "domainOfInfluenceType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )


@dataclass
class ElectedType:
    class Meta:
        name = "electedType"

    majoral_election: Optional["ElectedType.MajoralElection"] = field(
        default=None,
        metadata={
            "name": "majoralElection",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    proportional_election: Optional[
        "ElectedType.ProportionalElection"
    ] = field(
        default=None,
        metadata={
            "name": "proportionalElection",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )

    @dataclass
    class MajoralElection:
        absolute_majority: Optional[int] = field(
            default=None,
            metadata={
                "name": "absoluteMajority",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        elected_candidate: List[
            "ElectedType.MajoralElection.ElectedCandidate"
        ] = field(
            default_factory=list,
            metadata={
                "name": "electedCandidate",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )

        @dataclass
        class ElectedCandidate:
            candidate_identification: Optional[str] = field(
                default=None,
                metadata={
                    "name": "candidateIdentification",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "required": True,
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            elected_by_draw: Optional[bool] = field(
                default=None,
                metadata={
                    "name": "electedByDraw",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            named_element: List[NamedElementType] = field(
                default_factory=list,
                metadata={
                    "name": "namedElement",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )

    @dataclass
    class ProportionalElection:
        list_value: List["ElectedType.ProportionalElection.ListType"] = field(
            default_factory=list,
            metadata={
                "name": "list",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_occurs": 1,
            },
        )

        @dataclass
        class ListType:
            list_identification: Optional[str] = field(
                default=None,
                metadata={
                    "name": "listIdentification",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "required": True,
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            elected_candidate: List[
                "ElectedType.ProportionalElection.ListType.ElectedCandidate"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "electedCandidate",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            count_of_seats_gained: Optional[int] = field(
                default=None,
                metadata={
                    "name": "countOfSeatsGained",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "required": True,
                    "min_inclusive": 0,
                    "max_inclusive": 9999999,
                },
            )
            named_element: List[NamedElementType] = field(
                default_factory=list,
                metadata={
                    "name": "namedElement",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )

            @dataclass
            class ElectedCandidate:
                candidate_identification: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "candidateIdentification",
                        "type": "Element",
                        "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                        "required": True,
                        "min_length": 1,
                        "max_length": 50,
                    },
                )
                elected_by_draw: Optional[bool] = field(
                    default=None,
                    metadata={
                        "name": "electedByDraw",
                        "type": "Element",
                        "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    },
                )
                named_element: List[NamedElementType] = field(
                    default_factory=list,
                    metadata={
                        "name": "namedElement",
                        "type": "Element",
                        "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    },
                )


@dataclass
class ListResultType:
    class Meta:
        name = "listResultType"

    list_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "listIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    count_of_changed_ballots: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfChangedBallots",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_unchanged_ballots: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfUnchangedBallots",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_candidate_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfCandidateVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_additional_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfAdditionalVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    candidate_results: List["ListResultType.CandidateResults"] = field(
        default_factory=list,
        metadata={
            "name": "candidateResults",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_occurs": 1,
        },
    )
    named_element: List[NamedElementType] = field(
        default_factory=list,
        metadata={
            "name": "namedElement",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )

    @dataclass
    class CandidateResults:
        candidate_identification: Optional[str] = field(
            default=None,
            metadata={
                "name": "candidateIdentification",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_length": 1,
                "max_length": 50,
            },
        )
        count_of_votes_from_changed_ballots: Optional[int] = field(
            default=None,
            metadata={
                "name": "countOfVotesFromChangedBallots",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        count_of_votes_from_unchanged_ballots: Optional[int] = field(
            default=None,
            metadata={
                "name": "countOfVotesFromUnchangedBallots",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        candidate_list_results_info: Optional[
            "ListResultType.CandidateResults.CandidateListResultsInfo"
        ] = field(
            default=None,
            metadata={
                "name": "candidateListResultsInfo",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )
        named_element: List[NamedElementType] = field(
            default_factory=list,
            metadata={
                "name": "namedElement",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )

        @dataclass
        class CandidateListResultsInfo:
            candidate_list_results: List[CandidateListResultType] = field(
                default_factory=list,
                metadata={
                    "name": "candidateListResults",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            count_of_votes_from_ballots_without_list_designation: Optional[
                int
            ] = field(
                default=None,
                metadata={
                    "name": "countOfVotesFromBallotsWithoutListDesignation",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "min_inclusive": 0,
                    "max_inclusive": 9999999,
                },
            )
            named_element: List[NamedElementType] = field(
                default_factory=list,
                metadata={
                    "name": "namedElement",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )


@dataclass
class VoteType:
    class Meta:
        name = "voteType"

    vote_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "voteIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    main_vote_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "mainVoteIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 50,
        },
    )
    other_identification: List[NamedIdType] = field(
        default_factory=list,
        metadata={
            "name": "otherIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    domain_of_influence: Optional[DomainOfInfluenceType] = field(
        default=None,
        metadata={
            "name": "domainOfInfluence",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    superior_authority: Optional[DomainOfInfluenceType] = field(
        default=None,
        metadata={
            "name": "superiorAuthority",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    polling_day: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "pollingDay",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    vote_title_information: List[VoteTitleInformationType] = field(
        default_factory=list,
        metadata={
            "name": "voteTitleInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_occurs": 1,
        },
    )
    decisive_majority: Optional[DecisiveMajorityType] = field(
        default=None,
        metadata={
            "name": "decisiveMajority",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    vote_sub_type: Optional[VoteSubTypeType] = field(
        default=None,
        metadata={
            "name": "voteSubType",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    sequence: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 1,
            "max_inclusive": 999,
        },
    )
    grouping: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_length": 1,
            "max_length": 50,
        },
    )


@dataclass
class ElectionGroupInfoType:
    class Meta:
        name = "electionGroupInfoType"

    election_group: Optional["ElectionGroupInfoType.ElectionGroup"] = field(
        default=None,
        metadata={
            "name": "electionGroup",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    counting_circle: List[CountingCircleType] = field(
        default_factory=list,
        metadata={
            "name": "countingCircle",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_occurs": 1,
        },
    )
    named_element: List[NamedElementType] = field(
        default_factory=list,
        metadata={
            "name": "namedElement",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )

    @dataclass
    class ElectionGroup:
        election_group_identification: Optional[str] = field(
            default=None,
            metadata={
                "name": "electionGroupIdentification",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_length": 1,
                "max_length": 50,
            },
        )
        domain_of_influence: Optional[DomainOfInfluenceType] = field(
            default=None,
            metadata={
                "name": "domainOfInfluence",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
            },
        )
        superior_authority: Optional[DomainOfInfluenceType] = field(
            default=None,
            metadata={
                "name": "superiorAuthority",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )
        election_group_position: Optional[int] = field(
            default=None,
            metadata={
                "name": "electionGroupPosition",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )
        election_information: List[
            "ElectionGroupInfoType.ElectionGroup.ElectionInformation"
        ] = field(
            default_factory=list,
            metadata={
                "name": "electionInformation",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_occurs": 1,
            },
        )
        named_element: List[NamedElementType] = field(
            default_factory=list,
            metadata={
                "name": "namedElement",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )

        @dataclass
        class ElectionInformation:
            election: Optional[ElectionType] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "required": True,
                },
            )
            quorum: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "min_inclusive": Decimal("0.00"),
                    "max_inclusive": Decimal("100.00"),
                    "total_digits": 5,
                    "fraction_digits": 2,
                },
            )
            referenced_election_association_id: Optional[str] = field(
                default=None,
                metadata={
                    "name": "referencedElectionAssociationId",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            candidate: List[CandidateType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            list_value: List[ListType] = field(
                default_factory=list,
                metadata={
                    "name": "list",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            list_union: List[ListUnionType] = field(
                default_factory=list,
                metadata={
                    "name": "listUnion",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            named_element: List[NamedElementType] = field(
                default_factory=list,
                metadata={
                    "name": "namedElement",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )


@dataclass
class ElectionResultType:
    class Meta:
        name = "electionResultType"

    election_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "electionIdentification",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    majoral_election: Optional["ElectionResultType.MajoralElection"] = field(
        default=None,
        metadata={
            "name": "majoralElection",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    proportional_election: Optional[
        "ElectionResultType.ProportionalElection"
    ] = field(
        default=None,
        metadata={
            "name": "proportionalElection",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    named_element: List[NamedElementType] = field(
        default_factory=list,
        metadata={
            "name": "namedElement",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )

    @dataclass
    class MajoralElection:
        """
        :ivar candidate_result: element ist always supplied for all
            candidates that are known now. So candidate and
            candidateResult have always the same number of elements
        :ivar count_of_invalid_votes_total:
        :ivar count_of_blank_votes_total:
        :ivar count_of_individual_votes_total:
        :ivar named_element:
        """

        candidate_result: List[CandidateResultType] = field(
            default_factory=list,
            metadata={
                "name": "candidateResult",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_occurs": 1,
            },
        )
        count_of_invalid_votes_total: Optional[int] = field(
            default=None,
            metadata={
                "name": "countOfInvalidVotesTotal",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        count_of_blank_votes_total: Optional[int] = field(
            default=None,
            metadata={
                "name": "countOfBlankVotesTotal",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        count_of_individual_votes_total: Optional[int] = field(
            default=None,
            metadata={
                "name": "countOfIndividualVotesTotal",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        named_element: List[NamedElementType] = field(
            default_factory=list,
            metadata={
                "name": "namedElement",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )

    @dataclass
    class ProportionalElection:
        count_of_changed_ballots_without_list_designation: Optional[
            int
        ] = field(
            default=None,
            metadata={
                "name": "countOfChangedBallotsWithoutListDesignation",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_inclusive": 0,
                "max_inclusive": 9999999,
            },
        )
        count_of_empty_votes_of_changed_ballots_without_list_designation: \
            Optional[int] = field(
                default=None,
                metadata={
                    "name":
                    "countOfEmptyVotesOfChangedBallotsWithoutListDesignation",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "required": True,
                    "min_inclusive": 0,
                    "max_inclusive": 9999999,
                },
            )
        list_results: List[ListResultType] = field(
            default_factory=list,
            metadata={
                "name": "listResults",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_occurs": 1,
            },
        )
        named_element: List[NamedElementType] = field(
            default_factory=list,
            metadata={
                "name": "namedElement",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )


@dataclass
class ResultDataType:
    class Meta:
        name = "resultDataType"

    count_of_voters_information: Optional[
        CountOfVotersInformationType
    ] = field(
        default=None,
        metadata={
            "name": "countOfVotersInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    voting_card_information: Optional[VotingCardInformationType] = field(
        default=None,
        metadata={
            "name": "votingCardInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    fully_counted_true: Optional[bool] = field(
        default=None,
        metadata={
            "name": "fullyCountedTrue",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    released_timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "releasedTimestamp",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    lockout_timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lockoutTimestamp",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    voter_turnout: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "voterTurnout",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": Decimal("0.00"),
            "max_inclusive": Decimal("100.00"),
            "total_digits": 5,
            "fraction_digits": 2,
        },
    )
    received_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    received_invalid_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedInvalidVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    received_empty_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedEmptyVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    received_valid_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "receivedValidVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_yes_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfYesVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_no_votes: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfNoVotes",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_votes_without_answer: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfVotesWithoutAnswer",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    named_element: List[NamedElementType] = field(
        default_factory=list,
        metadata={
            "name": "namedElement",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )


@dataclass
class CountingCircleInfoType:
    class Meta:
        name = "countingCircleInfoType"

    counting_circle: Optional[CountingCircleType] = field(
        default=None,
        metadata={
            "name": "countingCircle",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    result_data: Optional[ResultDataType] = field(
        default=None,
        metadata={
            "name": "resultData",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )


@dataclass
class CountingCircleResultType:
    class Meta:
        name = "countingCircleResultType"

    counting_circle_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "countingCircleId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        },
    )
    count_of_voters_information: Optional[
        CountOfVotersInformationType
    ] = field(
        default=None,
        metadata={
            "name": "countOfVotersInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    voting_card_information: Optional[VotingCardInformationType] = field(
        default=None,
        metadata={
            "name": "votingCardInformation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    fully_counted_true: Optional[bool] = field(
        default=None,
        metadata={
            "name": "fullyCountedTrue",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    released_timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "releasedTimestamp",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    lockout_timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lockoutTimestamp",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    voter_turnout: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "voterTurnout",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_inclusive": Decimal("0.00"),
            "max_inclusive": Decimal("100.00"),
            "total_digits": 5,
            "fraction_digits": 2,
        },
    )
    count_of_received_ballots: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfReceivedBallots",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_blank_ballots: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfBlankBallots",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_invalid_ballots: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfInvalidBallots",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    count_of_valid_ballots: Optional[int] = field(
        default=None,
        metadata={
            "name": "countOfValidBallots",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    election_result: Optional[ElectionResultType] = field(
        default=None,
        metadata={
            "name": "electionResult",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    named_element: List[NamedElementType] = field(
        default_factory=list,
        metadata={
            "name": "namedElement",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )


@dataclass
class EventElectionInformationDeliveryType:
    """
    :ivar canton_id:
    :ivar polling_day:
    :ivar election_association:
    :ivar election_group_info: There is always an electionGroup, if it
        is not needed to keep several elections together, there is only
        one election under it
    :ivar number_of_entries:
    :ivar extension:
    """

    class Meta:
        name = "eventElectionInformationDeliveryType"

    canton_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "cantonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 26,
        },
    )
    polling_day: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "pollingDay",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    election_association: List[ElectionAssociationType] = field(
        default_factory=list,
        metadata={
            "name": "electionAssociation",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
    election_group_info: List[ElectionGroupInfoType] = field(
        default_factory=list,
        metadata={
            "name": "electionGroupInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_occurs": 1,
        },
    )
    number_of_entries: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfEntries",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 999,
        },
    )
    extension: Optional[ExtensionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )


@dataclass
class EventElectionResultDeliveryType:
    class Meta:
        name = "eventElectionResultDeliveryType"

    canton_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "cantonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 26,
        },
    )
    polling_day: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "pollingDay",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    election_group_result: List[
        "EventElectionResultDeliveryType.ElectionGroupResult"
    ] = field(
        default_factory=list,
        metadata={
            "name": "electionGroupResult",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_occurs": 1,
        },
    )
    number_of_entries: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfEntries",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 999,
        },
    )
    extension: Optional[ExtensionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )

    @dataclass
    class ElectionGroupResult:
        election_group_identification: Optional[str] = field(
            default=None,
            metadata={
                "name": "electionGroupIdentification",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "required": True,
                "min_length": 1,
                "max_length": 50,
            },
        )
        election_result: List[
            "EventElectionResultDeliveryType.ElectionGroupResult."
            "ElectionResult"
        ] = field(
            default_factory=list,
            metadata={
                "name": "electionResult",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                "min_occurs": 1,
            },
        )
        named_element: List[NamedElementType] = field(
            default_factory=list,
            metadata={
                "name": "namedElement",
                "type": "Element",
                "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            },
        )

        @dataclass
        class ElectionResult:
            election_identification: Optional[str] = field(
                default=None,
                metadata={
                    "name": "electionIdentification",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "required": True,
                    "min_length": 1,
                    "max_length": 50,
                },
            )
            candidate: List[CandidateType] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            counting_circle_result: List[CountingCircleResultType] = field(
                default_factory=list,
                metadata={
                    "name": "countingCircleResult",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                    "min_occurs": 1,
                },
            )
            elected: Optional[ElectedType] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )
            named_element: List[NamedElementType] = field(
                default_factory=list,
                metadata={
                    "name": "namedElement",
                    "type": "Element",
                    "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
                },
            )


@dataclass
class VoteInfoType:
    class Meta:
        name = "voteInfoType"

    vote: Optional[VoteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    counting_circle_info: List[CountingCircleInfoType] = field(
        default_factory=list,
        metadata={
            "name": "countingCircleInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_occurs": 1,
        },
    )


@dataclass
class EventVoteBaseDeliveryType:
    class Meta:
        name = "eventVoteBaseDeliveryType"

    canton_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "cantonId",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 26,
        },
    )
    polling_day: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "pollingDay",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
        },
    )
    vote_info: List[VoteInfoType] = field(
        default_factory=list,
        metadata={
            "name": "voteInfo",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "min_occurs": 1,
        },
    )
    number_of_entries: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfEntries",
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 999,
        },
    )
    extension: Optional[ExtensionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )


@dataclass
class Delivery:
    class Meta:
        name = "delivery"
        namespace = "http://www.ech.ch/xmlns/eCH-0252/2"

    delivery_header: Optional[HeaderType] = field(
        default=None,
        metadata={
            "name": "deliveryHeader",
            "type": "Element",
            "required": True,
        },
    )
    vote_base_delivery: Optional[EventVoteBaseDeliveryType] = field(
        default=None,
        metadata={
            "name": "voteBaseDelivery",
            "type": "Element",
        },
    )
    election_information_delivery: Optional[
        EventElectionInformationDeliveryType
    ] = field(
        default=None,
        metadata={
            "name": "electionInformationDelivery",
            "type": "Element",
        },
    )
    election_result_delivery: Optional[
        EventElectionResultDeliveryType
    ] = field(
        default=None,
        metadata={
            "name": "electionResultDelivery",
            "type": "Element",
        },
    )
    minor_version: Optional[int] = field(
        default=None,
        metadata={
            "name": "minorVersion",
            "type": "Attribute",
            "namespace": "http://www.ech.ch/xmlns/eCH-0252/2",
        },
    )
