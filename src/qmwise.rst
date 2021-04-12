QMWISe
------

QMWISe stands for Questionmark Web Integration Services environment.  It
is a SOAP-based web services API that provides an alternative method of
accessing the underlying data model of the qm:db:`Delivery` database.

QMWISe is available in all current versions of Questionmark software.

This part of the guide is in preparation and is not yet complete.  For
more general information on configuring QMWISe please refer to the older
`Perception 5.7 QMWISe API Guide
<https://support.questionmark.com/content/questionmark-perception-57-qmwise-api-guide>`_ 

QMWISe is based on `SOAP`_ and defines a wide range of operations (also
referred to as *methods*) covering the underlying data model.

..  _SOAP:  https://www.w3.org/TR/soap/


.. toctree::
    :maxdepth: 2

    qmwise/methods


..  _qmwise_string:

String Parameters
~~~~~~~~~~~~~~~~~

..  qm:xtype::  string
    :simple:
    
    Due to a limitation of the technology used in the original design of
    QMWISe all parameters of type string are marked as being *nillable*
    in the WSDL.  This means that messages in which these values have
    been omitted will validate against the WSDL, however, it does *not*
    indicate that they are valid QMWISe messages.

    QMWISe imposes additional rules over and above those expressed in
    the WSDL, in particular, where input parameters are of type string
    they may be required and omitting their values will result in a SOAP
    fault.

    As a general rule of thumb, if a string parameter maps to a required
    field in the data model then it will be required.  There are some
    exceptions, check the documentation for the method or type you are
    using for further restrictions.


..  _qmwise_optional:

Optional Parameters
~~~~~~~~~~~~~~~~~~~

For XML validation purposes it is important to realise that, if an
element is present in a SOAP request then the content of the element
must be a valid value for that element.  In the vast majority of cases,
optional elements are defined to be of type :qm:xtype:`string` so an
empty element is interpreted as an empty string and in many cases is
treated indistinguishably from an omitted element (which is interpreted
as null). 

In cases where the element type is something other than string you must
either omit the element (interpreted as null or as the default value
given in the WSDL, see :ref:`qmwise_defaults`) or provide a valid value.
For example, the :qm:xfield:`Participant.Use_Correspondence` field is
declared as follows::

    <element minOccurs="0" maxOccurs="1" default="0"
        name="Use_Correspondence" type="int"/>

therefore, if you include this element in a request to create a
participant it must contain a valid integer.  In this case the integer
is used as a flag and only the values 0 and 1 are permitted.  You *may*
omit the element completely which is equivalent to passing the value 0.
A empty element will cause an error as the XML of the SOAP request will
not be valid.

..  _assessmentid:

Assessment IDs
~~~~~~~~~~~~~~

In QMWISe, Assessment IDs are represented using :qm:xtype:`string`.
These strings should always be padded with leading 0s to create a string
of exactly 16 characters.  In the underlying data model assessment IDs
are represented using two 32-bit integers (see :ref:`midlid`).

For example, suppose an assessment has the following ID in the database::

    MID = 38074658
    LID = 94065740

According to the rules for combining MID and LID this results in a
64-bit assessment ID of::

    ID = MID * 100000000 + LID = 3807465894065740

In QMWISe you'll pass this 64-bit integer as a 16-character string::

    "3807465894065740"

Things are more complicated when the MID and LID have leading zeros,
especially as some IDs follow the pattern MID = LID * 10 such as those
in the following example::

    MID = 320750
    LID = 32075
    ID = MID * 100000000 + LID = 32075000032075

In QMWISe you must pass this 64-bit integer as a 16-character string
with 0-padding on the left::

    "0032075000032075"

..  warning::   if you are also using the newer OData APIs note that
                they use a true 64-bit representation in the metadata
                but that, when serialised to JSON format, these values
                are represented as strings *without* the 0-padding on
                the left.  The only safe ways to compare two assessment
                IDs are:

                1.  convert both values to strings, left padding to 16
                    characters
                2.  convert both values to 64-bit integers


..  _extension_types:

Extension Types
~~~~~~~~~~~~~~~

QMWISe uses the XML schema technique of deriving types by extension. 
For example, the :qm:xtype:`Result` type is extended by the
:qm:xtype:`Result2` type.  These extensions sometimes represent the
development of the API from an earlier, smaller, set of return fields to
a later revision returning more information (possibly reflecting changes
to the underlying data model itself).  For example::

    <s:complexType name="Result2">
        <s:complexContent mixed="false">
            <s:extension base="tns:Result">
                <s:sequence>
                    <s:element minOccurs="0" maxOccurs="1"
                        name="FirstName" type="s:string" />
                    <s:element minOccurs="0" maxOccurs="1"
                        name="LastName" type="s:string" />
                    <s:element minOccurs="0" maxOccurs="1"
                        name="PrimaryEmailAddress" type="s:string" />
                    <s:element minOccurs="0" maxOccurs="1"
                        name="SubgroupPath" type="s:string" />
                    <s:element minOccurs="0" maxOccurs="1"
                        name="CourseProperty" type="s:string" />
                    <s:element minOccurs="1" maxOccurs="1"
                        name="ScoreBandIDProperty" type="s:int" />
                </s:sequence>
            </s:extension>
        </s:complexContent>
    </s:complexType>

Although marked as returning type :qm:xtype:`Result` the method
:qm:meth:`GetResult` actually returns an element of type
:qm:xtype:`Result2` containing these additional fields.

Backwards compatibility remains an important goal of QMWISe but
implementers using frameworks that take a snapshot of the WSDL (for
example, to auto-generate code stubs in languages such as Java and C#)
should be aware that additional, unexpected, elements may be returned in
SOAP responses as a result of changes to the schema.  This should not
cause failures as this is precisely what the XML schema extension
element was designed to achieve.  That said, this type of change is kept
to a minimum in QMWISe and the current pattern of development is to add
new methods rather than extending the types returned by existing ones.

..  _qmwise_defaults:

Default Values
~~~~~~~~~~~~~~

In some cases the WSDL for QMWISe defines structures with default
values, for example, see :qm:xfield:`Schedule.Monitored`::

    <s:element minOccurs="0" maxOccurs="1" default="0" name="Monitored" type="s:int" />

A definition like this means that a missing Monitored element in a
request *or response* should be inferred to mean "0", the default value.
Due to the nature of the technology used to implement QMWISe when
serialising responses to XML elements with default values are typically
omitted.  This may be confusing at first, especially to tools that do
not read and interpret the WSDL correctly.

Basic Types
~~~~~~~~~~~

..  _XMLSchema: https://www.w3.org/TR/xmlschema-2/

QMWISe makes extensive use of the following basic types from XMLSchema_.

..  qm:xtype::  boolean
    :simple:
    
    Values "true", "false", "1" or "0".  See boolean_.
    
    ..  _boolean: https://www.w3.org/TR/xmlschema-2/#boolean


..  qm:xtype::  double
    :simple:

    See double_.
    
    ..  _double: https://www.w3.org/TR/xmlschema-2/#double

..  qm:xtype::  short
    :simple:

    See short_.
    
    ..  _short: https://www.w3.org/TR/xmlschema-2/#short

..  qm:xtype::  int
    :simple:

    See int_.
    
    ..  _int: https://www.w3.org/TR/xmlschema-2/#int

..  _soap_tls:


TLS and SoapUI
~~~~~~~~~~~~~~

In accordance with the end of support for TLS 1.0 on Questionmark
OnDemand you will need to follow the following instructions to use
the popular SoapUI tool with QMWISe.

1.  Open SOAP UI vmoptions, you can find this file under SoapUI
    installation folder::

        C:\Program Files\SmartBear\SoapUI-5.3.0\bin\SoapUI-5.3.0.vmoptions

2.  Add this line in vmoptions::

        -Dsoapui.https.protocols=TLSv1.2

3.  Close SOAP UI and try again accessing the QMWISe methods
 