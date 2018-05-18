.. QuestionmarkAPIs documentation master file, created by
   sphinx-quickstart on Tue May 10 17:17:06 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Questionmark's Open Assessment Platform
=======================================

Please direct all feedback to developer@questionmark.com or by raising
issues on the `GitHub project
<https://github.com/questionmark/qm-oap-docs>`_  where these pages are
maintained.

Contents:

.. toctree::
    :maxdepth: 2

    overview
    odata
    deliveryodata
    resultsodata
    qmwise
    data_model
    pip


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


About this Documentation
========================

This documentation is being developed to update and (eventually) replace
the information in the following online guides, some of which may be
available only to Questionmark customers:

    *   `Delivery OData API Guide
        <https://www.questionmark.com/content/delivery-odata-api-guide>`_

    *   `Perception 5.7 QMWISe API Guide
        <https://www.questionmark.com/content/questionmark-perception-57-qmwise-api-guide>`_
        
    *   `Database Schema Reference Guide
        <https://www.questionmark.com/content/questionmark-perception-database-schema-reference-guide>`_


Useful links:

    *   `Configuring OnDemand for use with the Blackboard Connector
        <https://www.questionmark.com/content/ondemand-blackboard-connector-configuring-ondemand>`_     
        good exemplar on configuring a suitable role for use with
        service accounts to use with the APIs. 
        

This documentation is automatically generated using Sphinx_ from source
code marked up with reStructuredText_ (see also `Quick reStructuredText
<http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_).  You
can find the full source in our `GitHub Repository
<https://github.com/questionmark/qm-oap-docs>`_.

..  _Sphinx: http://www.sphinx-doc.org/en/stable/

..  _reStructuredText: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html

The items documented use a number of custom domains, the source of which
is included in the above repository too.  The following links have
provided invaluable help in creating these custom domains:

    *   `Sphinx Domain API
        <http://www.sphinx-doc.org/en/stable/extdev/domainapi.html#domain-api>`_
    
    *   `Sphinx Source Documentation
        <http://code.nabla.net/doc/sphinx/api/sphinx.html>`_ used in
        conjunction with the API docs to understand stuff used commonly
        in custom domain code.

    *   `Sphinx Source on GitHub
        <https://github.com/sphinx-doc/sphinx/tree/master/sphinx/domains>`_
        these domains were very useful in understanding how to implement
        the required classes directly (as opposed to having them
        generated automatically as per the GNU Make Domain example
        referenced in many custom domain projects.
    
    *   `sphinx-contrib <https://bitbucket.org/birkenfeld/sphinx-contrib>`_
        source code for a wide variety of custom domains
        
    *   `HTTP Custom Domain
        <https://pythonhosted.org/sphinxcontrib-httpdomain/>`_ An
        interesting project with some more complex layouts, also
        reviewed as a potential model for documenting OData services
        
    *   `The Docutils Document Tree
        <http://docutils.sourceforge.net/docs/ref/doctree.html>`_
        useful reading for doing the hard bits such as linking type
        definitions.
    
    *   `Documenting a language using a custom Sphinx domain...
        <http://samprocter.com/2014/06/documenting-a-language-using-a-custom-sphinx-domain-and-pygments-lexer/>`_
        a useful starting point for showing what is possible though this
        follows the GNU Make Domain pattern which was not ultimately
        adopted in the custom domains used.

