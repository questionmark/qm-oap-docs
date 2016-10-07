QMWISe
------

QMWISe stands for Questionmark Web Integration Services environment.  It
is a SOAP-based web services API that provides an alternative method of
accessing the underlying data model of the qm:db:`Delivery` database.

QMWISe is available in all current versions of Questionmark software.

This part of the guide is in preparation and is not yet complete.  For
more general information on configuring QMWISe please refer to the older
`Perception 5.7 QMWISe API Guide
<https://www.questionmark.com/content/questionmark-perception-57-qmwise-api-guide>`_ 

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


 