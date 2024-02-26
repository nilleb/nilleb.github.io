---
title: "Run a Google Cloud Datalab instance on your computer"
date: "2017-08-11"
---

On the official Google Cloud Datalab [quickstart](https://cloud.google.com/datalab/docs/quickstarts), Google gives you the detailed steps about how to start a GCP instance running the Jupyter notebook, where you'll experiment all the functionalities of the Datalab.

But, perhaps you don't want to pay the price of the instance. You don't need to use the cloud for that, since you have your own computer. In this case, to get a Datalab instance on your computer, you just need docker.

`docker run -it -p "127.0.0.1:8081:8080" -v $PWD:"/content" gcr.io/cloud-datalab/datalab:local`

But let's admit that you have a BigQuery dataset, with which you want to play. To access easily that data from the Datalab notebook as if you were on a dedicated instance, you'll have to:

1. stop the running Datalab instance
2. read https://developers.google.com/identity/protocols/application-default-credentials#howtheywork and get a credentials.json
3. if you have started the Datalab instance at least once, you'll have a datalab folder. Copy the `credentials.json` to the `datalab/.config` folder
4. `export GOOGLE_APPLICATION_CREDENTIALS=/content/datalab/.config/credentials.json`
5. once again, `docker run -it -p "127.0.0.1:8081:8080" -v $PWD:"/content" gcr.io/cloud-datalab/datalab:local`
6. open your favourite browser to the address that has been printed to the console
7. In the first code cell, type `%projects set yourproject`

Now you're ready to play with your dataset. For example:

1. add a code cell
2. `%%sql --module records SELECT field1, field2, field3, field4 FROM dataset.table`
3. add another code cell
4. `import datalab.bigquery as bq df = bq.Query(records).to_dataframe()`

Congratulations! You have now a working pandas dataset ;-)
