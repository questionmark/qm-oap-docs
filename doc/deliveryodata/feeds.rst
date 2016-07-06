Delivery OData Feeds
--------------------

The Delivery OData API implements version 3 of the OData standard which
is generally compatible with both version 3 and version 2 clients.


Features
~~~~~~~~

$filter
    Supported.  Filtering is only allowed on certain property values.
    The restrictions have been put in place to ensure that API requests
    do not have a negative effect on the delivery of assessments.
    
$format
    Not supported.  The service returns responses using JSON format by
    default.  To obtain XML responses you need to pass a suitably
    restrictive Accept: header as the $format query option is not
    supported.


Feeds
~~~~~


..  od:feed::   Results Result

    The Results feed contains data about assessment results.  Entries
    are defined by the :od:type:`Result` type.


Entity Type Reference
~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    result



    
