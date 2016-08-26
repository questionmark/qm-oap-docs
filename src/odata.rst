OData
-----

..  _odata:

OData Primer
~~~~~~~~~~~~

TBC


Frequently Asked Questions
~~~~~~~~~~~~~~~~~~~~~~~~~~

Why am I getting the error *Unrecognized 'Edm.Int32' literal*?

The following URL path returns an error like this::

    /deliveryodata/12345/Results?$filter=AssessmentID eq 1234567890123

The reason is that the integer 1234567890123 is too large to be
represented as a 32-bit integer.  The largest 32-bit integer is
2147483647.  The real issue is that the AssessmentID property is of type
Edm.Int64, a 64-bit integer, and values of this type require the 'L'
suffix as follows::

    /deliveryodata/12345/Results?$filter=AssessmentID eq 1234567890123L

