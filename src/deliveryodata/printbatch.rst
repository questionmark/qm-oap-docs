PrintBatch
----------

..  od:service::    deliveryodata


..  od:feed::   PrintBatches PrintBatch

    :method GET: read only
    :filter ID: primary key
    :filter GroupID: the ID of the group associated with this batch

    $orderby is *not* supported.

    The PrintBatches feed contains information about a group of users
    who have been assigned a particular snapshot of an assessment to
    take externally, typically through printing and scanning.


..  od:type::   PrintBatch
