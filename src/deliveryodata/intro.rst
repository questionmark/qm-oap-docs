Introduction
------------

..  _OData: http://www.odata.org/

Based on the Open Data (OData_) protocol, the Delivery OData API is a
RESTful data service that can be used to retrieve data from a
Questionmark repository.

The data in a repository is divided into three main databases covering
the three main functions of Questionmark's assessment management system:
content creation, delivery, and result reporting. The Delivery OData API
focuses on the data in the qm:db:`Delivery` database.  For information
about using OData to access data from the qm:db:`Analytics` database see
:od:svc:`resultsodata`.

Although you can still interact with this API using OData-aware tools
such PowerPivot for Excel and Tableau it is not designed to be used for
reporting and there are significant limits placed on the exposed data
and supported filters.  Although this API has been optimised for
performance to reduce the impact of API calls on running assessments you
should be mindful of the fact that some of the feeds defined here share
access to tables that are used by the participant-facing delivery of the
tests themselves.

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


