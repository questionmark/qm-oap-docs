Introduction
------------

..  _OData: http://www.odata.org/

Based on the Open Data (OData_) protocol, the Delivery OData API is a
RESTful data service that can be used to retrieve data from a
Questionmark repository.

The data in a repository is divided into three main databases covering
the three main functions of Questionmark's assessment management system:
content creation, delivery, and result reporting. The Delivery OData API
focuses on the data in the Delivery database.  For information about
using OData to access data from the Results Warehouse see
:od:svc:`resultsodata`.

Although you can still interact with this API using OData-aware tools
such as PowerPivot for Excel and Tableau it is not designed to be used
for reporting and there are significant limits placed on the exposed
data and supported filters.  This API has been optimised for performance
to reduce the impact of API calls on running assessments as some of the
feeds defined here share access to tables that are used by the
participant-facing delivery of the tests themselves.

The main purpose of this API is to support the creation of third-party
integrations created in programming languages such as C# and Java. Refer
to the OData_ website for a complete list of tools and libraries that
have support for the OData protocol.  You don't necessarily need a
dedicated OData client library to use the Delivery OData API; you can
use just about any tool that can make HTTP requests and parse JSON or
XML responses.

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
                JavaScript.


Service Root
~~~~~~~~~~~~

To access an OData service you need to determine the service root of the
service.  The service root is a base URL which returns an overview
document linking to all the feeds exposed by the API.  It can also be used
to calculate the location of a metadata document that provides detailed
type information about the entity types supported by the API.

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
