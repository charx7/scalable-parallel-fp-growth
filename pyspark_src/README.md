# Example Package

To install under your local system use: 

```
pip install -e .
```

the ".e" tag enables your source to be editable once you installed.

To generate a zipfile to be distributed to spark cluster use:

```
python setup.py sdist_egg
```

You need to have set up your env variable $SPARK_HOME

To run the sample Job while in this folder just type into the terminal:

```
$SPARK_HOME/bin/spark-submit --master 'local[*]'  --py-files dist/pyspark_recom_engine-0.1-py3.6.egg pyspark_recom_engine/jobs/sampleJob.py

```
