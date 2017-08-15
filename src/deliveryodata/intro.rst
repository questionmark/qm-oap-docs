Introduction
------------

..  _OData: http://www.odata.org/

Based on the Open Data (OData_) protocol (version 3), the Delivery OData
API is a RESTful data service that can be used to retrieve data from a
Questionmark repository.

The data in a repository is divided into three main databases covering
the three main functions of Questionmark's assessment management system:
content creation, delivery, and result reporting. The Delivery OData API
focuses on the data in the Delivery database.  For information about
using OData to access data from the Results Warehouse see
:od:svc:`resultsodata`.

..  image:: ../overview.png

Although you can still interact with this API using OData-aware tools
such as PowerPivot for Excel and Tableau it is not designed to be used
for reporting and there are significant limits placed on the exposed
data and supported filters.  This API has been optimised for performance
to reduce the impact of API calls on running assessments as some of the
feeds (EntitySets) defined here share access to tables that are used by
the participant-facing delivery of the tests themselves.

The main purpose of this API is to support the creation of third-party
integrations created in programming languages such as C# and Java. Refer
to the OData_ website for a complete list of tools and libraries that
have support for the OData protocol.  You don't necessarily need a
dedicated OData client library to use the Delivery OData API; you can
use just about any tool that can make HTTP requests and parse JSON or
XML responses.  The documentation contains many example requests
captured using a simple REST-client browser plugin.


..  warning::   If you are using the WCF OData client, you must set the
                IgnoreMissingProperties setting to true for the
                DataServiceContext.

..  seealso::   For an overview of the way Questionmark has implemented OData
                please see :ref:`odata`.


Security
~~~~~~~~

Access to the Delivery OData API is protected using HTTP's basic
authentication. This requires the client to pass the username and
password of a specially created service account.  The service account
must be either:

    *   a user that has been assigned the Admin role in OnDemand, or
    
    *   a user that has a custom role with the Access Server
        Configuration permission.

    ..note::    For more information about roles and permissions, please
                refer to `Roles and permissions
                <https://www.questionmark.com/content/how-can-i-manage-administrator-permissions>`_
                section of the OnDemand User Guide.

When accessed without credentials, requests will generate a 401
unauthorized response indicating that basic credentials are required. It
is often convenient to use a web browser when testing OData URLs, the
401 response will trigger the browser to prompt the user for a username
and password and then retry the request.

    ..warning:: the credentials required to access the OData APIs have
                powerful permissions and should be stored appropriately
                when configuring your application.  They are not
                suitable for passing to the client browser, these APIs
                are not intended to be used directly from client-side
                JavaScript.  Where examples have been generated in a
                browser-based too this is for illustrative purposes
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

For users of Questionmark OnDemand the service root is::

    https://ondemand.questionmark.com/deliveryodata/<customer ID>/

...or for customers using the Europe-based service::

    https://ondemand.questionmark.eu/deliveryodata/<customer ID>/

You replaced <customer ID> with the area number assigned to the
repository, for example a US-based repository with customer (area)
number 123456 would have the following service root::

    https://ondemand.questionmark.com/deliveryodata/123456/

Individual feeds can be accessed by appending the name of the feed
to the service root::

    https://ondemand.questionmark.com/deliveryodata/123456/Results

would return information about Results in the specified repository.


OData Features
~~~~~~~~~~~~~~

The Delivery OData API implements version 3 of the OData standard which
is generally compatible with both version 3 and version 2 clients.

$top and $skip
    If a feed request would cause too many entities to be returned the
    collection returned will be truncated.

    For example::
    
        <service root>/Results
    
    There are likely to be lots of results in the repository. The
    returned collection contains the first *page* of results and a
    continuation link that can be used to retrieve the next *page*, and
    so on.

    This technique was not possible with previous APIs (compare
    :qm:meth:`GetResultList`), but it does require some special handling
    on the client side. Questionmark's OData feeds make extensive use of
    paging and also impose an upper limit on the number of records that
    will be returned for each request to improve performance of both the
    service and the client itself.  The limit is currently set to 100.

    You can individually control how many results you retrieve (if you
    want fewer than 100) using the $top and $skip options::
    
            <service root>/Results?$top=10&$orderby=WhenFinished desc
        
    This query retrieves the 10 most recent results.  To get the next
    10 just add $skip::
    
            <service root>/Results?$top=10&$skip=10&$orderby=WhenFinished desc
    
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
    
        <service root>/Results?$filter=ParticipantName eq 'user123'
    
    Although spaces are shown in the above URL parameter values should
    be appropriately escaped for use in HTTP.
    
    The representation of values (such as 'user123' above) is defined by
    the OData specification.  Take care to match the type of any values
    provided in filters with the type of the corresponding property.
    In particular, note that 64-bit integers use an 'L' suffix::
    
        <service root>/Results?$filter=AssessmentID eq 9962000009962L

    More complex examples::
    
        <service root>/ScoringTasks?$filter=Group/Name eq 'CS101' and Status lt 3

    ...returns all ScoringTask entities relating to the Group with name
    CS101 that have a status less then 3 (Scored).
    
    ::

        <service root>/ScoringTasks/$count?$filter=Group/Name eq 'CS101' and Status eq 2

    ...returns the count of all ScoringTask entities relating to the
    Group with name CS101 that have a status of 2 (Saved).
    
    ::

        <service root>/ScoringTasks?$filter=Group/Name eq 'CS101' and Assessment/ID eq 1234567890L

    ...returns all ScoringTask entities relating to the Group with name
    CS101 and the assessment with ID 1234567890.
    
    ::

        <service root>/Results?$filter=GroupName eq 'CS101' and Assessment/ID eq 1234567890L&$orderby=WhenFinished desc

    ...returns all result entities relating to the group with name CS101
    and the assessment with ID 1234567890 ordered by the most recently
    submitted first.
    
    ::

        <service root>/Results?$filter=Assessment/ID eq 1234567890L and ParticipantName eq 'JaneSmith'&$orderby=WhenFinished

    ...returns all result entities relating to JaneSmith's attempts at
    the specific assessment with ID 1234567890 ordered from the first to
    the last attempt.
        
$orderby
    Supported.  Ordering can usually be used on any field marked as
    being suported in $filter.  Exceptions are noted in the feed
    descriptions.

    Example::
    
        <service root>/Results?$orderby=WhenFinished desc
        
$expand
    The expansion of navigation properties is supported though some
    special rules apply.  See each feed for details.  There is a limit
    on the depth of expansion that is allowed to ensure result sets are
    manageable.  Example expansion::
    
        <service root>/Results?$expand=Answers
    
    A deeper expansion::
    
        <service root>/Results(12345678)?$expand=Answers/Question
    
    The above not only lists all answers for the result but, within each
    answer entity, the Question itself is also expanded.  Bear in mind
    that use of expansion can dramatically increase the complexity of
    the query used to retrieve the data and the number of entities
    returned.  A maximum depth of 2 expansions is supported (as above).
    
    If an expansion results in too many child entities being returned
    for a single entity then the expansion itself will be truncated. 
    The limit is set to 100, the same as for base feeds.
    
    If this is a problem then you can usually transform the query into a
    filtered request on the target feed instead.  If an OData response
    exceeds 100 entities a continuation link is provided that can be
    used to retrieve the next 100 results, and so on.
    
    For example, if there are too many answers associated with a result
    then a query such as::
    
        Results(12345678)?$expand=Answers
    
    can instead be retrieved as separate queries::
    
        <service root>/Results(12345678)
        <service root>/Answers?$filter=ResultID eq 12345678
        <service root>/Answers?$filter=ResultID eq 12345678&$skip=100
        <service root>/Answers?$filter=ResultID eq 12345678&$skip=200
        ...
            
    If a feed's entity type is related to another type via a navigation
    property with a *target* multiplicity of 0..1 and $expand is
    supported for that property then it is possible to use the expansion
    directly in filters and orderings.
    
    For example, to view Answers to a specific question ordered by
    the date when the corresponding result was submitted (most recent
    first) you could use a query like this::
    
        <service root>/Answers?$filter=QuestionID eq 100000000373L&$orderby=Result/WhenFinished desc

    This query shows an orderby query with an implicit expansion of
    depth 1.  In the feed descriptions, allowed filters are described in
    terms of their immediate parent entity (depth 0), however, if a
    filter is supported at depth 0 you may assume that it will also be
    supported at depth 1 when filtering or ordering related entities.
            
$count
    Supported on base feeds only.  Cannot be used in combination with
    navigation properties.  This is OK::

        <service root>/Results/$count
        
    This is not::
    
        <service root>/Results(12345678)/Answers/$count
        
$format
    Not supported.  The service returns responses using JSON format by
    default.  To obtain XML responses you need to pass a suitably
    restrictive Accept: header as the $format query option is not
    supported.

$value
    For feeds labelled *Media Link Entry* the $value path component can
    be used to obtain the full media resource for an entity.  Access to
    simple property values is not supported. 

$select
    This query option is not currently supported by the Delivery OData
    API.
