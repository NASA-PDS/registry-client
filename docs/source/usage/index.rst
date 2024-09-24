Usage
===============

This section describes a few ways to use the `registry-client` application for accessing data
within your PDS Registry.


Getting Started
--------------------------
The `registry-client` is a very simple application that enables access to OpenSearch in
AWS.

Search Examples
++++++++++++++++
A few simple search examples are noted below. If you would like to perform more complex queries, see the
OpenSearch API documentation: https://opensearch.org/docs/latest/api-reference/

*Note: The following instructions require* `wget <https://www.gnu.org/software/wget/>`_ *to be
installed. For Windows users, you will also need to replace the $REGISTRY variable in the commands
below, versus trying to set an environment variable.*

**Search for all bundles in your index**::

    # Download the bundles.json example query
    wget https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/bundles.json

    # Set your registry and execute registry-client
    export REGISTRY=geo-registry
    pds-registry-client --data @bundles.json /${REGISTRY}/_search –pretty

**Search for all collections in your index**::

    # Download the collections.json example query
    wget https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/collections.json

    # Set your registry and execute registry-client
    export REGISTRY=geo-registry
    pds-registry-client --data @collections.json /${REGISTRY}/_search –pretty

**Search for a specific product LIDVID**::

    # Download the single_product.json example query
    wget https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/single_product.json

    # Open the single_product.json file and update the LIDVID with the value
    # you would like to search for.

    # Set your registry and execute registry-client
    export REGISTRY=geo-registry
    pds-registry-client --data @single_product.json /${REGISTRY}/_search –pretty

For more examples, checkout the `Registry Discussion Board <https://github.com/NASA-PDS/registry/discussions>`_
