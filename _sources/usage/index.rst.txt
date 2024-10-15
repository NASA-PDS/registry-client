===========
🏃‍♀️ Usage
===========

.. toctree::


Overview
--------

This package provides one command line tool used to query the Registry OpenSearch Database in AWS.

This utility takes care of the authentication and signing procedures needed to access the `OpenSearch API <https://opensearch.org/docs/latest/api-reference/>`_.
It is then providing access to the full OpenSearch API syntax within the limit of your access authorizations.

This section describes how to use the `registry-client` application for accessing data
within your PDS Registry.


Pre-requisites
--------------


For this reason, there are 3 pre-requisites to use the tool:

1. Have authentication and authorization to access the Registry OpenSearch Database, see Prerequisites in :doc:`/installation/index`.
2. Knowledge of the OpenSearch indexes used by the registry. Details are given below.
3. Knowledge of the OpenSearch API syntax. However, we provide in the manual the most useful queries.


Registry indexes
~~~~~~~~~~~~~~~~

For each discipline node, the following indexes exist:

.. list-table:: Indexes
    :header-rows: 1

    * - Index Name
      - Description
    * - <node_code>-registry
      - One record per PDS4 label
    * - <node_code>-registry-refs
      - Records linking batches of observational_products with their collections
    * - <node_code>-registry-dd
      - Type of all the properties used in the PDS4 labels.


The node_code values can be: atm, en, geo, img, naif, ppi, psa, rms, sbnpsi, sbnumd

As a node operator, you only have access, with registry-client to your own indexes.


Usage Information
-----------------

Run ``pds-registry-client --help``  to
get summaries of the command-line invocations, required arguments, and any
options that refine the behavior.

The following section gives examples of query, gradually more complex. You can go through them.

*Note:: all the examples queries hereafter are accessible for download in this directory _`Query Examples<https://github.com/NASA-PDS/registry-client/tree/main/conf/examples>*

*Note: The following instructions use* `wget <https://www.gnu.org/software/wget/>`_ *to be
installed. For Windows users, you will also need to replace the $REGISTRY variable in the commands
below, versus trying to set an environment variable.*

For more examples, checkout the `Registry Discussion Board <https://github.com/NASA-PDS/registry/discussions>`_


Get The First 10 Products of Your Discipline Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here for Engineering Node, code `en`, try this command::

    pds-registry-client '/en-registry/_search'

You are getting a json response with a summary of the response and the 10 products retrieved by querying the OpenSearch API end-point `_search` on your index `registry` without filters.

The pagination configuration of OpenSearch return by default only 10 results per query. We'll see later how to get more.

You can also "pretty" print the response by adding an option::

    pds-registry-client '/en-registry/_search' --pretty

And store the response in a file::

    pds-registry-client '/en-registry/_search' --pretty > result.json


Simple Filter, Get The First 10 Bundles of Your Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Try this command::

    pds-registry-client '/en-registry/_search' --data '{"query":{"match":{"product_class":"Product_Bundle"}}}' --pretty


The `--data` argument value, contains the filter which selects the bundles.

You can see more clearly what the filter does by pasting the content in a json formatter, for example https://jsonformatter.org/ ::

    {
      "query": {
        "match": {
          "product_class": "Product_Bundle"
        }
      }
    }

You are filtering all the products which property `product_class` is equal to "Product_Bundle".

However the handling of the query string in the --data is tedious and uneasy to read.

You can instead manage the query in a file, for example `bundles.json <https://github.com/NASA-PDS/registry-client/blob/main/conf/examples/bundles.json>`_ containing the indented code above.

You can call the command line as follow, with the same result::

    pds-registry-client '/en-registry/_search' --data @bundles.json --pretty

You can download our bundles.json file are follow::

    wget https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/bundles.json

The same process applies to select the collections, see query `collections.json <https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/collections.json>`_


Get A Single Product
~~~~~~~~~~~~~~~~~~~~~

Consider the query in file `single_product.json <https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/single_product.json>`_ ::

    {
      "query": {
        "match": {
          "lid": "urn:nasa:pds:insight_documents:document_hp3rad"
        }
      },
      "fields": [
        "lidvid",
        "ops:Label_File_Info/ops:file_ref",
        "ops:Tracking_Meta/ops:archive_status",
        "ops:Provenance/ops:parent_bundle_identifier"
      ],
      "_source": false
    }

You can download the query file with command::

    wget https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/single_product.json

This query will select products matching the given `lid` and return the lidvid, and a few other properties for each of them.

Run the query as follow::

    # Set your registry and execute registry-client
    export REGISTRY=geo-registry
    pds-registry-client --data @single_product.json /${REGISTRY}/_search –pretty


Get All the Properties Available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can get the list of the properties you can filter on by querying the `_mapping` end-point. For example::

    pds-registry-client '/en-registry/_mapping' --pretty


Get All the Distinct Values for One Property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider the following query available a file, `archive_status_values.json  <https://raw.githubusercontent.com/NASA-PDS/registry-client/main/conf/examples/archive_status_values.json>`_ ::

    {
      "size": 0,
      "aggs": {
        "response_codes": {
          "terms": {
            "field": "ops:Tracking_Meta/ops:archive_status",
            "size": 99
          }
        }
      }
    }

The first `size` property means you don't want any products in your response, but only the distinct values of the property archive_status. For details on this type of query go to _`Aggregations <https://opensearch.org/docs/latest/aggregations/>`

You can get the archive_status existing, distinct values in your node by running::

    pds-registry-client --data @conf/examples/archive_status_values.json /en-registry/_search --pretty


Get Results Beyond Limit of 10 Products
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For details on pagination in OpenSearch see `pagination <https://opensearch.org/docs/latest/search-plugins/searching-data/paginate/>`_

Up to 500 or 1000 products
--------------------------

By default, OpenSearch returns 10 results per page, you can increase this value up to 500 or 1000.
You can do this by adding the property `size` to you query. As follow::


    {
      "size": 500,
      "query": {
        "match": {
          "product_class": "Product_Bundle"
        }
      }
    }

From 1000 to 10,000 products
---------------------------

If your query returns more than 1000 products, but less than 10,000 and you want to see them all, then you need to do multiple requests using the pagination feature of OpenSearch.

The most simple way of using pagination is to iterate over pages using the `from` property. The `from` property defines the sequence number of the first product in the response.

You can get the second page with query::


    {
      "from": 500,
      "size": 500,
      "query": {
        "match": {
          "product_class": "Product_Bundle"
        }
      }
    }

And iterate with from values 1000, 1500, ... until the number of product returned is less than the `size` value.


Beyond 10,000 products:
-----------------------

At last if your query returns more that 10,000 products, you'll have to use the `search-after` property. The initial page need to be sorted by one of the product's properties. We advise to use `ops:Harvest_Info/ops:harvest_date_time` which defines the time when the product has been loaded in the registry.

The first page's query is going to look like::

    {
      "sort": ["ops:Harvest_Info/ops:harvest_date_time"],
      "size": 500,
      "query": {
        "match": {
          "product_class": "Product_Bundle"
        }
      }
    }

Then, you should get the "ops:Harvest_Info/ops:harvest_date_time" value for the last product returned by this query, for example "2023-09-25T15:40:54.993Z" and will query a new page for products which harvest_time is greater than this value, as follow::

    {
      "sort": ["ops:Harvest_Info/ops:harvest_date_time"],
      "search_after": ["2023-09-25T15:40:54.993Z"],
      "size": 500,
      "query": {
        "match": {
          "product_class": "Product_Bundle"
        }
      }
    }


And so forth, until the page returned contains less than 500 products.









