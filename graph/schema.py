from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Date, Integer, \
        Float, Long, Text, Keyword, analyzer, Object


class Authors(DocType):
    AuthorId = Long(required = True)
    Rank = Integer(required = True)
    NormalizedName = Text(required = True, analyzer = "standard")
    DisplayName = Text(required = True, analyzer = "standard")
    LastKnownAffiliationId  = Long()
    PaperCount = Long()
    CitationCount = Long()
    CreatedDate = Date(required = True)

    class Meta:
        index = 'Authors'.lower() # index name should be lowercase


class Affiliations(DocType):
    AffiliationId = Long(required = True)
    Rank = Integer(required = True)
    NormalizedName = Text(required = True, analyzer = "standard")
    DisplayName = Text(required = True, analyzer = "standard")
    GridId = Text(required = True)
    OfficialPage = Text(required = True)
    WikiPage = Text(required = True)
    PaperCount = Long()
    CitationCount = Long()
    CreatedDate = Date(required = True)

    class Meta:
        index = 'Affiliations'.lower()


class Papers(DocType):
    PaperId = Long(required = True)
    Rank = Integer(required = True)
    Doi = Text(required = True)
    DocType = Text(required = True)
    PaperTitle = Text(required = True, analyzer = "standard")
    OriginalTitle = Text(required = True, analyzer = "standard")
    BookTitle = Text()
    Year = Integer()
    date = Date()   # Date --> date (type conflict)
    Publisher = Text()

    JournalId = Long()
    ConferenceSeriesId = Long()
    ConferenceInstanceId = Long()
    Volume = Text()
    Issue = Text()
    FirstPage = Text()
    LastPage = Text()
    ReferenceCount = Long()
    CitationCount = Long()
    EstimatedCitation = Integer()
    OriginalVenue = Text() # new attribute ver.2019-01-01
    CreatedDate = Date(required = True)

    LanguageCode = Keyword() # from PaperLanguages
    FieldOfStudy = Object( # from PaperFieldsOfStudy
        multi = True,
        properties = {
            "FieldOfStudyId": Long(required = True),
            "Similarity": Float()
        }
    )
    SourceType = Integer() # from PaperUrls
    SourceUrl = Text() # from PaperUrls

    class Meta:
        index = 'Papers'.lower()


class PaperReferences(DocType):
    PaperId = Long(required = True)
    PaperReferenceId = Long(required = True)

    class Meta:
        index = 'PaperReferences'.lower()


class PaperAuthorAffiliations(DocType):
    PaperId = Long(required = True)
    AuthorId = Long(required = True)
    AffiliationId = Long()
    AuthorSequenceNumber = Integer(required = True)
    OriginalAffiliation = Text() # new attribute ver.2019-01-01

    class Meta:
        index = 'PaperAuthorAffiliations'.lower()


class ConferenceInstances(DocType):
    ConferenceInstanceId = Long(required = True)
    # Rank = Integer(required = True) # removed attr ver.2019-01-01
    NormalizedName = Text(required = True, analyzer = "standard")
    DisplayName = Text(required = True, analyzer = "standard")
    ConferenceSeriesId = Long()
    Location = Text()
    OfficialUrl = Text()
    StartDate = Date()
    EndDate = Date()
    AbstractRegistrationDate = Date()
    SubmissionDeadlineDate = Date()
    NotificationDueDate = Date()
    FinalVersionDueDate = Date()
    PaperCount = Long()
    CitationCount = Long()
    CreatedDate = Date(required  = True)

    class Meta:
        index = 'ConferenceInstances'.lower()


class ConferenceSeries(DocType):
    ConferenceSeriesId = Long(required = True)
    Rank = Integer(required = True)
    NormalizedName = Text(required = True, analyzer = "standard")
    DisplayName = Text(required = True, analyzer = "standard")
    PaperCount = Long()
    CitationCount = Long()
    CreatedDate = Date(required  = True)

    class Meta:
        index = 'ConferenceSeries'.lower()


class Journals(DocType):
    JournalId = Long(required = True)
    Rank = Integer(required = True)
    NormalizedName = Text(required = True, analyzer = "standard")
    DisplayName = Text(required = True, analyzer = "standard")
    Issn = Text()
    Publisher = Text()
    Webpage = Text()
    PaperCount = Long()
    CitationCount = Long()
    CreatedDate = Date(required  = True)

    class Meta:
        index = 'Journals'.lower()

class PaperFieldsOfStudy(DocType):
    PaperId = Long(required = True)
    FieldOfStudyId = Long(required = True)
    Similarity = Float()

    class Meta:
        index = 'PaperFieldsOfStudy'.lower()


class FieldsOfStudy(DocType):
    FieldOfStudyId = Long(required = True)
    Rank = Integer(required = True)
    NormalizedName = Text(required = True, analyzer = "standard")
    DisplayName = Text(required = True, analyzer = "standard")
    MainType = Text(analyzer = "standard")
    Level = Integer(required = True)
    PaperCount = Long()
    CitationCount = Long()
    CreatedDate = Date(required  = True)

    class Meta:
        index = 'FieldsOfStudy'.lower()


class FieldOfStudyChildren(DocType):
    FieldOfStudyId = Long(required = True)
    ChildFieldOfStudyId = Long(required = True)

    class Meta:
        index = 'FieldOfStudyChildren'.lower()
