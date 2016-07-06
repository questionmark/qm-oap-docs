
Data Model
----------

Underlying the Questionmark system is a data model that describes the
data stored about quizzes, tests and exams (content); about the delivery
of the content and about results.

Internally, that data is organized into a number of databases containing
tables.  Users of Questionmark OnDemand access these tables indirectly
through API calls.  Users of Questionmark OnPremise (or Perception 5)
are encouraged to use APIs too but, in some cases, they may wish to
access the database tables directly.  In either case, the tables define
the underlying data model for all Questionmark data.

In many cases the same data fields are exposed through multiple APIs. 
The data model is documented to provide a convenient central point for
the detailed explanation of these data elements.

You might want to look in :qm:table:`a_Result`

.. toctree::
    :maxdepth: 2

    model/answer


Misc Topics
~~~~~~~~~~~

..  _varchar:

Fields defined with varchar
+++++++++++++++++++++++++++

Users are strongly advised to use API calls where possible.  OnPremise
or Perception users who must manipulate data in the database tables
directly should be aware of the way text fields are encoded.
 
For legacy reasons, many fields in the data model are defined to have
the SQL server type *varchar*.  This represents a non-Unicode string of
data in the database but in the Questionmark data model these fields are
frequently used to contain Unicode data by applying a special
transformation to the data when reading and writing to the underlying
database field.

It is important to understand that varchar fields in the database are
strings of characters drawn from the character set defined by the
collation in operation.  For Questionmark databases this collation will
always be one of: SQL_Latin1_General_CP1_CI_AS or Latin1_General_CI_AS.
In both cases, the character set is the same and is the 'Latin1'
character set defined by Microsoft.  This should not be confused with
the ISO Latin-1 character set defined by ISO-8859-1 as it is different.
Microsoft's Latin1 character set is also often referred to as CP1252_.

..  _CP1252: https://en.wikipedia.org/wiki/Windows-1252

To interpret data drawn directly from a Questionmark database it is
necessary to understand the transformation applied to enable Unicode
data to be stored in varchar fields.

varchar encoding:

    1.  Convert a string of Unicode characters into bytes by applying
        the UTF-8 encoding.

    2.  Transform this string of bytes back into a string of characters
        by replacing each byte with its corresponding character in
        CP1252.  
    
    3.  Store the resulting string of characters in the varchar data
        field.

varchar decoding:

    1.  Retrieve the string of characters from the varchar data field
    
    2.  Encode these characters into a string of bytes by replacing each
        character with the byte that represents it in CP1252.
    
    3.  Decode the resulting string of bytes using UTF-8 to obtain the
        original Unicode data.

The following example may help.  Suppose we have the Unicode string:

    |copy| 2016

.. |copy| unicode:: 0xA9 .. copyright sign

To convert this into its varchar representation for storage in a varchar
data field we follow the encoding procedure defined above.

    1.  Encode with UTF-8 to obtain (in hex):
    
        C2 A9 20 32 30 31 36
    
    2.  Replace bytes with their CP1252 characters:

        |c2| |a9| 2016

..  |c2| unicode:: 0xC2  ..  byte c2
    :trim:

..  |a9| unicode:: 0xA9  ..  byte a9

The above string is then saved to the varchar field.  It may appear odd
at first that the copyright sign is itself part of the encoded string
but this is just a quirk of the encoding algorithm (and similar
behaviour is observed for all the characters with Unicode code points
0x80 through to 0xBF).

..  warning::
    The UTF-8 encoding may create a sequence of bytes that is longer
    than the corresponding sequence of characters.  Non-ASCII characters
    will result in 2 or 3 bytes each.  As a result, the length of a
    varchar field given in the data model represents a restriction on
    the length of the UTF-8 byte sequence and not the maximum number of
    characters.
    
    In some cases, APIs are conservative in their implementation and may
    truncate or reject character strings that might exceed the
    underlying data model storage.
    
..  note::
    Due to the nature of UTF-8 and the way the western European
    characters are encoded you are highly likely to see byte values
    C0-C5 in the encoded string.  These bytes are all represented as
    upper-case 'A' (with various accents) in CP1252 and if unexpectedly
    seen in Unicode data are diagnostic of a failure to decode data
    correctly (or evidence of earlier double-encoding).

..  warning::
    Unfortunately, the use of control characters can cause problems as
    CP1252 does not define mappings for all bytes. The values 0x81,
    0x8D, 0x8F, 0x90 and 0x9D are left undefined.  As a result, these
    values can cause issues during step 2 of the encoding/decoding
    algorithm described above if they appear in the UTF-8 encoded byte
    sequence. Windows-based technologies tend to ignore this
    inconsistency and allow such sequences to be decoded using CP1252 as
    if it contained the corresponding C1 control at that point (i.e.,
    byte 0x81 decodes to the Unicode character with codepoint 0x81 when
    using CP1252).  Other technologies may not be so generous and may
    decode such sequences as the replacement character (Unicode 0xFFFD)
    or simply raise exceptions.

    This is only a problem if you are attempting to read/write directly
    from/to a Questionmark database as API calls always manage the
    encoding for you.

    Most low-level database drivers will have a 'raw' mode in which
    varchar data can be read as a string of bytes (instead of
    characters) and it may be necessary to use this mode, in which case,
    you can ignore CP1252 completely and treat the raw data as if it
    were the UTF-8 encoded version of the original Unicode data string.

        
..  _timezones:

Timezones
+++++++++

Datetime values in the data model may be stored in one of three timezones.

    UTC
        Typically indicated by a _UTC suffix to the name of the field in
        the data model.

    Repository Time
        In Questionmark's OnDemand platform repositories have their own
        default timezone.  This is set when the repository is first
        created and does not usually change.  Historically this was the
        main timezone used for datetime values and is the timezone
        likely to be experienced in the user interface.
        
        For Perception users the repository time cannot be set and is
        treated as the same as the platform time.

    Platform Time
        In some cases, datetime values are stored using the timezone of
        the platform.  This is the default timezone of the server
        running the database.  In Questionmark OnDemand this will vary
        depending on the region in which the repository is hosted.
       

..  _midlid:

MID and LID
+++++++++++

For legacy reasons, some 64-bit integer IDs are split into two values in
the data model.  The two values are typically indicated with a \_MID and
\_LID suffix.

Calculation of the 64-bit ID from a MID and LID uses a *decimal* algorithm::

    ID = MID * 100000000 + LID

Likewise, you need to use *decimal* arithmetic to split an ID into the
two separate parts::

    MID = ID / 100000000
    LID = ID % 100000000

For example::
    
    MID = 80317034
    LID = 6550612
    ID = 8031703406550612

Values of MID and LID are limited to the range [1, 99999999].  If you
are creating 64-bit ID values yourself you must ensure that they satisfy
the following constraints::

    ID % 10 != 0
    ID > 100000000
    ID <= 9999999999999999

As a result, IDs contains approximately 50 bits of information.