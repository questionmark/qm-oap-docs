OData
-----

..  _odata:

OData Primer
~~~~~~~~~~~~

OData is a standard for constructing APIs that follow a RESTful pattern.
In this pattern data (resources) are identified by URLs.  When resources
are retrieved they may contain links to other resources which are
explicitly represented by the URLs of those resources.  New resources
can be created by POSTing information and existing resources can be
updated using the HTTP methods PUT and PATCH.

This standard was chosen as the basis of these APIs as it provides a
simple way to map database tables and the records they contain into a
web-service.  In fact, OData is sometimes referred to as 'SQL over the
web'.  Database tables map on to the OData concept of a feed (inherited
from the Atom standard), records map on to entities  and the values
within the records map on to the property values of the entities.  Each
record in the database that is exposed through OData therefore has a
corresponding entity in the OData API with a corresponding URL that can
be used to retrieve it.

For more information about how to construct OData URLs see `OData: URI
Conventions
<http://www.odata.org/documentation/odata-version-3-0/url-conventions/>`_


Frequently Asked Questions
~~~~~~~~~~~~~~~~~~~~~~~~~~

Why am I getting the error *Unrecognized 'Edm.Int32' literal*?
    The following URL path returns an error like this::

        /deliveryodata/12345/Results?$filter=AssessmentID eq 1234567890123

    The reason is that the integer 1234567890123 is too large to be
    represented as a 32-bit integer.  The largest 32-bit integer is
    2147483647.  The real issue is that the AssessmentID property is of
    type Edm.Int64, a 64-bit integer, and values of this type require
    the 'L' suffix as follows::

        /deliveryodata/12345/Results?$filter=AssessmentID eq 1234567890123L

Why is my WCF DataService not loading expanded properties?
    Users of the WCF client will need to set the MergeOption to
    OverwriteChanges as per the reply to this question on StackOverflow.
    See `Why is my WCF DataService not loading expanded properties?
    <http://stackoverflow.com/questions/14956172/why-is-my-wcf-dataservice-not-loading-expanded-properties>`_

    Failure to do this may cause unexpected failures when loading
    entities from the OData service.