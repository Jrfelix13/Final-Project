from flask import Flask, render_template, redirect, jsonify, request

import numpy as np
import pandas as pd
import requests
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.orm import aliased

from pyspark.ml.fpm import FPGrowth

#################################################
# Database Setup
#################################################
POSTGRES = {
    'user': 'root',
    'pw': 'FinalProject_2020',
    'db': 'final_project_db',
    'host': 'finalprojectdb.cyj4dabyex0o.us-east-2.rds.amazonaws.com',
    'port': '5432',
}
engine = create_engine('postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Aisle = Base.classes.aisle_tbl
Product = Base.classes.product_tbl
Department = Base.classes.department_tbl
Orders = Base.classes.orders_tbl
OrdersP = Base.classes.orders_product_prior
OrdersT = Base.classes.orders_product_train

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/graph/aisle")
def aisle():
    session = Session(engine)
    query = f"select aisle_tbl.aisle, count(orders_product_prior.order_id) from aisle_tbl 
                inner join product_tbl on product_tbl.aisle_id = aisle_tbl.aisle_id 
                inner join orders_product_prior on orders_product_prior.product_id=product_tbl.product_id 
                group by aisle_tbl.aisle"
    results = engine.execute(query).fetchall()
    aisle = []
    order_count = []
    for result in results:
        aisle.append(result[0])
        order_count.append(result[1])

    pie_aisle_df= pd.DataFrame({"aisle":aisle,"Total_aisle":order_count})
    pie_aisle_df.sort_values(by=["Total_aisle"],inplace=True,ascending=False)
    pie_aisle_df1 = pie_aisle_df.iloc[0:10,:]
    aisle_other= pie_aisle_df.Total_aisle.iloc[10:].sum()
    df_append = pd.DataFrame({"aisle":["Other"],"Total_aisle":[aisle_other]})
    pie_aisle_df1 = pie_aisle_df1.append(df_append,ignore_index=True)
    session.close()
    return jsonify(pie_aisle_df1)

@app.route("/graph/department")
def department():
    session = Session(engine)
    query = f"select department_tbl.department, count(orders_product_prior.order_id) from department_tbl 
                inner join product_tbl on product_tbl.department_id = department_tbl.deparment_id 
                inner join orders_product_prior on orders_product_prior.product_id=product_tbl.product_id 
                group by department_tbl.department"
    results = engine.execute(query).fetchall()
    department = []
    order_count = []
    for result in results:
        department.append(result[0])
        order_count.append(result[1])

    pie_department_df= pd.DataFrame({"department":department,"Total_department":order_count})
    pie_department_df.sort_values(by=["Total_department"],inplace=True,ascending=False)
    pie_department_df1 = pie_department_df.iloc[0:10,:]
    department_other= pie_department_df.Total_department.iloc[10:].sum()
    df_append = pd.DataFrame({"department":["Other"],"Total_department":[deparment_other]})
    pie_department_df1 = pie_department_df1.append(df_append,ignore_index=True)
    session.close()
    return jsonify(pie_department_df1)

@app.route("/graph/product")
def product():
    session = Session(engine)
    query = f"select product_tbl.product_name, count(orders_product_prior.order_id) from product_tbl 
                inner join orders_product_prior on orders_product_prior.product_id=product_tbl.product_id 
                group by product_tbl.product_name"
    results = engine.execute(query).fetchall()
    product = []
    order_count = []
    for result in results:
        product.append(result[0])
        order_count.append(result[1])

    product_df= pd.DataFrame({"product_name":department,"Total_product":order_count})
    product_df.sort_values(by=["Total_product"],inplace=True,ascending=False)
    product_df1 = product_df.iloc[0:10,:]
    session.close()
    return jsonify(product_df1)

@app.route("/graph/heat_map")
def heat():
    session = Session(engine)
    query = f"select order_dow,order_hour_of_day,count(order_id) from orders_tbl
                group by order_dow,order_hour_of_day"
    results = engine.execute(query).fetchall()
    order_dow = []
    order_hour = []
    order_count = []
    for result in results:
        order_dow.append(result[0])
        order_hour.append(result[1])
        order_count.append(result[2])

    heat_df= pd.DataFrame({"order_dow":order_dow,"order_hour_of_day":order_hour,"order_id":order_count})
    heat_df.order_dow=heat_df.order_dow.replace(0,"Monday")
    heat_df.order_dow=heat_df.order_dow.replace(1,"Tuesday")
    heat_df.order_dow=heat_df.order_dow.replace(2,"Wednesday")
    heat_df.order_dow=heat_df.order_dow.replace(3,"Thursday")
    heat_df.order_dow=heat_df.order_dow.replace(4,"Friday")
    heat_df.order_dow=heat_df.order_dow.replace(5,"Saturday")
    heat_df.order_dow=heat_df.order_dow.replace(6,"Sunday")
    session.close()
    return jsonify(heat_df)


if __name__ == "__main__":
    app.run(debug=True)
