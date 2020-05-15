Introduction
------------

        .. versionadded::   20209.02

..  _OData: http://www.odata.org/

Based on *version 4* of the Open Data (OData_) protocol, the Authoring
OData API is a RESTful data service that can be used to retrieve data
from a Questionmark repository.

The data in a repository is divided into three main databases covering
the three main functions of Questionmark's assessment management system:
content creation, delivery, and result reporting. The Authoring OData
API focuses on the data in the *content creation* database.  For
information about using OData to access data from the Delivery database
see :od:svc:`deliveryodata` and for the Results Warehouse see
:od:svc:`resultsodata`.

..  image:: ../overview.png

The main purpose of this API is to provide access to content during the
content creation process.  Although some data is available about
questions and assessments in the other API feeds these focus on the
published catalog of content in active use in delivery or as information
to provide additional context to the interpretation of results.

The entities exposed by this API contain a small amount of metadata to
enable discovering and tracking of the content creation lifecycle.  The
detailed information about the content is made available in the form of
XML documents marked up according to the Questionmark's QML (Question
Markup Language) and AML (Assessment Markup Language).  These formats
are documented here.

Refer to the OData_ website for a complete list of tools and libraries
that have support for version 4 of the OData protocol.  You don't
necessarily need a dedicated OData client library to use the Delivery
OData API; you can use just about any tool that can make HTTP requests
and parse JSON and XML responses.  The documentation contains many
example requests captured using a simple REST-client.


Security
~~~~~~~~

Access to the Authoring OData API is protected using HTTP's basic
authentication. This requires the client to pass the username and
password of a specially created service account.  The service account
must be either:

    *   a user that has been assigned the Admin role in the portal, or
    
    *   a user that has a custom role with the Access Server
        Configuration permission.

It is recommended that you create a dedicated role for API access and
set an appropriate password policy that enforces a password of an
appropriate length for an API key.

..  note::      For more information about roles and permissions, please
                refer to `Roles and permissions
                <https://www.questionmark.com/content/how-can-i-manage-administrator-permissions>`_
                section of the OnDemand User Guide.

When accessed without credentials, requests will generate a 401
unauthorized response indicating that basic credentials are required. It
is often convenient to use a web browser when testing OData URLs, the
401 response will trigger the browser to prompt the user for a username
and password and then retry the request.

..  warning::   the credentials required to access the OData APIs have
                powerful permissions and should be stored appropriately
                when configuring your application.  They are not
                suitable for passing to the client browser, these APIs
                are not intended to be used directly from client-side
                JavaScript.  Where examples have been generated in a
                browser-based tool this is for illustrative purposes
                only, your application should run in an appropriately
                secured environment.


Service Root
~~~~~~~~~~~~

To access an OData service you need to determine the service root of the
service.  The service root is a base URL which returns an overview
document linking to all the feeds (EntitySets) exposed by the API.  It
can also be used to calculate the location of a metadata document that
provides detailed type information about the entity types supported by
the API.

..  warning::   the URL patterns used in this section are currently
                subject to change.
                
For users of Questionmark OnDemand the service root is::

    https://ondemand.questionmark.com/authoringapi/<customer ID>/odata/

...or for customers using the Europe-based service::

    https://ondemand.questionmark.eu/authoringapi/<customer ID>/odata/

You replace <customer ID> with the area number assigned to the
repository, for example a US-based repository with customer (area)
number 123456 would have the following service root::

    https://ondemand.questionmark.com/authoringapi/123456/odata/

Individual feeds can be accessed by appending the name of the feed
to the service root::

    https://ondemand.questionmark.eu/authoringapi/123456/odata/QuestionRevisions

would return information about Questions (including revisions) in the
specified repository.


OData Features
~~~~~~~~~~~~~~

The Authoring OData API implements version 4 of the OData standard which
requires a specific OData 4 compatible client.  Version 4 is not
generally backwards compatible with earlier versions due to changes in
the underlying schemas and communication protocol, however, the
conventions for accessing data are very similar to earlier OData
versions and for most simple use cases the differences are noticed in
small changes to the syntax used in the URLs and query parameters.

$top and $skip
    If a feed request would cause too many entities to be returned the
    collection returned will be truncated.

    For example::
    
        <service root>/QuestionRevisions

    There are likely to be lots of Questions in the repository but even
    if you fewer than 100 Questions the individual revisions may well
    exceed the maximum number of records that the API is configured to
    return in a single request (100 entities). In that case, the
    returned collection contains the first *page* of results and a
    continuation link that can be used to retrieve the next *page*, and
    so on.

    You can individually control how many results you retrieve (if you
    want fewer than 100) using the $top and $skip options::
    
            <service root>/QuestionRevisions?$top=1&$orderby=ModifiedDateTime desc
        
    This query retrieves a single entity representing the most recent question
    modified in the repository.  To get the next
    one you can just add $skip::
    
            <service root>/QuestionRevisions?$top=1&$skip=1&$orderby=ModifiedDateTime desc
    
    The format of the continuation links may vary depending on the type
    of index used to satisfy the query internally.  When paging through
    a large feed it is better to use the continuation links provided in
    the previous response than to manually set $top and $skip.
    
$filter
    Supported.  Filtering is only allowed on certain property values,
    see the feed descriptions below for details. The restrictions have
    been put in place to ensure that API requests do not have a negative
    effect on the delivery of assessments.
    
    Example filter::
    
        <service root>/QuestionRevisions?$filter=CreatedDateTime gt 2019-11-14T11:25:00Z
        
    Although spaces are shown in the above URLs parameter values should
    be appropriately escaped for use in HTTP.
    
    The representation of values (such as the date time value above) is
    defined by the OData specification.  Take care to match the type of
    any values provided in filters with the type of the corresponding
    property. In particular, note that date-time values should always be
    given in UTC indicated by the Z suffix.
    
    Question and Assessment IDs are 64bit integers, unlike earlier OData
    standards 64bit integers /must not/ have a trailing L in OData version
    4.
    
        <service root>/QuestionRevisions?$filter=QuestionI eq 100000000692
        
$orderby
    Supported.  Ordering can usually be used on any field marked as
    being suported in $filter.  Exceptions are noted in the feed
    descriptions.

    Example::
    
        <service root>//QuestionRevisions?$orderby=ModifiedDateTime desc
        
$expand
    The expansion of navigation properties is supported.  See each feed
    for details.
    
        <service root>/QuestionRevisions(870)?$expand=QuestionQMLs
    
    The above query returns the entity for QuestionRevision 870 and
    returns metadata for each of the Question translations.
            
$count
    Supported on base feeds, for example::

        <service root>/QuestionRevisions/$count?$filter=QuestionId eq 100000000692
        
    Returns the number of revisions of the question with the given Question ID.
            
$format
    The service returns responses using JSON format.  The $format parameter
    can be used to force the returned entities to include additional metadata.
    This can be useful when traversing the data with a tool is not able
    to calculate entity URLs directly.  For example:
    
        <service root>/QuestionRevisions?$format=application/json;odata.metadata=full
    
    Will return additional metadata for each entity including links that
    can be used to traverse associated entities::
    
        {
            "@odata.type": "#QM.AuthoringApi.OData.Entity.QuestionRevision",
            "@odata.id": "https://ondemand.questionmark.com/AuthoringAPI/70018/odata/QuestionRevisions(870)",
            "@odata.editLink": "https://ondemand.questionmark.com/AuthoringAPI/70018/odata/QuestionRevisions(870)",
            "Id": 870,
            "QuestionId@odata.type": "#Int64",
            "QuestionId": 100000000684,
            "Language": "-",
            "CreatedDateTime@odata.type": "#DateTimeOffset",
            "CreatedDateTime": "2019-11-14T10:00:04.12Z",
            "Author": "70018",
            "ModifiedDateTime@odata.type": "#DateTimeOffset",
            "ModifiedDateTime": "2019-11-14T10:00:04.12Z",
            "Editor": "70018",
            "Status": "Normal",
            "ReviewStatus": null,
            "TopicPath": "SteveTesting/QuestionTypes",
            "IsDeleted": false,
            "QuestionQMLs@odata.associationLink": "https://ondemand.questionmark.com/AuthoringAPI/70018/odata/QuestionRevisions(870)/QuestionQMLs/$ref",
            "QuestionQMLs@odata.navigationLink": "https://ondemand.questionmark.com/AuthoringAPI/70018/odata/QuestionRevisions(870)/QuestionQMLs"
        }    

$value
    To retrieve the XML document associated with an entity append the
    $value path component to the entity's URL.

        <service root>/QuestionQMLs(Language='-',QuestionRevisionId=870)/$value

$select
    This query option is not currently supported by the Authoring OData
    API.

$search
    Not supported


