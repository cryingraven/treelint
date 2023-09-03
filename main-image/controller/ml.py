from app import app,db,storage,mongo
from flask_login import login_required,current_user
from flask import render_template,request,redirect
from model import TApp,UserFile
import pandas as pd
import numpy as np
from mongo_datatables import DataTables
import uuid
import json
import tempfile

@app.route('/new_ml')
@login_required
def new_app():
    return render_template('new_app.html')
@app.route('/detail_ml/<storeid>')
@login_required
def detail_ml(storeid):
    app=TApp.query.filter_by(data_folder=storeid).first()
    if app is not None:
        return render_template('ml_home.html',app=app)
    redirect('/')
@app.route('/ml_process/<storeid>')
@login_required
def ml_process(storeid):
    app=TApp.query.filter_by(data_folder=storeid).first()
    if app is not None:
        return render_template('ml_process.html',app=app)
    redirect('/')
@app.route('/ml_saved/<storeid>')
@login_required
def ml_saved(storeid):
    app=TApp.query.filter_by(data_folder=storeid).first()
    if app is not None:
        return render_template('ml_saved.html',app=app)
    redirect('/')
@app.route('/ml_do_upload/<storeid>',methods=['POST'])
@login_required
def ml_do_upload(storeid):
    app=TApp.query.filter_by(data_folder=storeid.strip()).first()
    if app is not None:
        uuid_name=str(uuid.uuid4())
        csv=request.files['csv']
        bucket=storage.get_bucket("deretdata")
        blob=bucket.blob('!@!'+current_user.username+'!@!'+storeid+'!@!'+csv.filename)
        blob.upload_from_file(csv)
        file_csv=UserFile()
        file_csv.name=csv.filename+' !~! '+uuid_name
        file_csv.uid=uuid_name
        file_csv.app_id=app.id
        file_csv.user_id=current_user.id
        pdata=pd.read_csv('gs://deretdata/'+'!@!'+current_user.username+'!@!'+storeid+'!@!'+csv.filename)
        json_data=pdata.to_json(orient='records')
        mongo_collection=mongo[current_user.username+'_'+app.data_folder+'_'+uuid_name]
        mongo_collection.remove()
        mongo_collection.insert_many(json.loads(json_data),bypass_document_validation=True)
        result={
            "status": True,
            "message": "Upload Success"
        }
        db.session.add(file_csv)
        db.session.commit()
        return json.dumps(result)
    print(storeid)
    result={
        "status": False,
        "message": "Upload Fail "
    }
    return json.dumps(result)
@app.route('/ml_show_feature/<storeid>/<uuid_name>')
@login_required
def ml_show_feature(storeid,uuid_name):
    feature=request.values.get("feature")
    file=UserFile.query.filter_by(uid=uuid_name).first()
    if file is None :
        return '{}'
    bucket=storage.get_bucket("deretdata")
    df=pd.read_csv('gs://deretdata/'+'!@!'+current_user.username+'!@!'+storeid+'!@!'+file.name.split(' !~! ')[0])
    datum={"types": "Not Regression/Classification"}
    r, c = df.shape
    datum["columns"]=int(c)
    datum["rows"]=int(r)
    if feature!='Clustering':
        dfseries=df[feature]
        if  'int64' == dfseries.dtypes or  'float64' == dfseries.dtypes:
            hist,bins=np.histogram(df[dfseries.notnull()][feature].to_numpy(),density=False)
            datum["hist"]=hist.tolist()
            datum["bins"]=bins.tolist()
            datum["dtype"]='Numerical'
            datum["types"]='Regression'
        elif  dfseries.dtypes == 'object' and  dfseries.count()/len(dfseries.unique()) > 1.2:
            datum["types"]='Classification'
            bar=[]
            bar_val=[]
            for un in dfseries.unique().tolist():
                fil=df[feature]
                filtered=fil.where(fil==un)
                bar.append(str(un))
                bar_val.append(int(filtered.count()))
            datum["bar"]=bar
            datum["dtype"]='Categorical'
            datum["bar_val"]=bar_val
    return json.dumps(datum)
@app.route('/ml_get_field/<storeid>/<uuid_name>')
@login_required
def ml_get_field(storeid,uuid_name):
    docid=mongo[current_user.username+'_'+storeid+'_'+uuid_name]
    doc=docid.find_one()
    field=[]
    if doc is not None:
        for key in doc :
            if key != '_id' :
                field.append(key)
    return json.dumps(field)
@app.route('/ml_eda_process/<storeid>/<uuid_name>')
@login_required
def ml_eda_process(storeid,uuid_name):
    request_args = json.loads(request.values.get("args"))
    file=UserFile.query.filter_by(uid=uuid_name).first()
    if file is None :
        return '{}'
    bucket=storage.get_bucket("deretdata")
    df=pd.read_csv('gs://deretdata/'+'!@!'+current_user.username+'!@!'+storeid+'!@!'+file.name.split(' !~! ')[0])
    detail=json.loads(df.describe().to_json(orient='columns'))
    data=[]
    id=0
    for key,obj in detail.items():
        detail[key]["unique"]=len(df[key].unique())
        detail[key]["null"]=int(df[key].isnull().sum())
        hist,bins=np.histogram(df[df[key].notnull()][key].to_numpy(),density=False)
        detail[key]["hist"]=hist.tolist()
        detail[key]["bins"]=bins.tolist()
        detail[key]["types"]='Numerical'
        datum=detail[key]
        datum["name"]=key
        datum["id"]=id
        datum["corr"]=list(df.corr(method='pearson')[key].index)
        datum["corr_val"]=list(df.corr(method='pearson')[key].values)
        id+=1
        data.append(datum)
    for key in df.columns:
        if  'int64' != df[key].dtypes and  'float64' != df[key].dtypes:
            datum={}
            datum["unique"]=len(df[key].unique())
            datum["count"]=int(df[key].count())
            datum["std"]=0
            datum["min"]=0
            datum["max"]=0
            datum["mean"]=0
            datum["null"]=int(df[key].isnull().sum())
            datum["name"]=key
            datum["id"]=id
            if 'datetime64' == df[key].dtypes:
                datum["types"]='Date Time'
            elif  df[key].dtypes == 'object' and  df[key].count()/datum["unique"] > 1.2:
                datum["types"]='Categorical'
                bar=[]
                bar_val=[]
                for un in df[key].unique().tolist():
                    fil=df[key]
                    filtered=fil.where(fil==un)
                    bar.append(str(un))
                    bar_val.append(int(filtered.count()))
                datum["bar"]=bar
                datum["bar_val"]=bar_val
            else:
                datum["types"]='Text'
            id+=1
            data.append(datum)
    return  json.dumps({
        'recordsTotal': len(data),
        'recordsFiltered': len(data),
        'draw': 1,  # cast draw as integer to prevent XSS
        'data': data
    })
@app.route('/ml_get_data/<storeid>/<uuid_name>')
@login_required
def ml_get_data(storeid,uuid_name):
    request_args = json.loads(request.values.get("args"))
    dt = DataTables(mongo, current_user.username+'_'+storeid+'_'+uuid_name, request_args)
    _agg = [
        {'$match': dt.filter},
        {'$sort': {dt.order_column: dt.order_dir}},
        {'$skip': dt.start},
        {'$project': dt.projection}
    ]
    _agg.append({'$limit': dt.limit})

    _results = list(mongo[current_user.username+'_'+storeid+'_'+uuid_name].aggregate(_agg))

    processed_results = []
    for result in _results:
        result = dict(result)
        result["DT_RowId"] = str(result.pop('_id'))  # rename the _id and convert ObjectId to str

        # go through every val in result and try to json.dumps objects and arrays - skip this if strings are okay
        for key, val in result.items():
            if type(val) in [list, dict, float]:
                result[key] = json.dumps(val)

        processed_results.append(result)
    return json.dumps({
        'recordsTotal': str(mongo[current_user.username+'_'+storeid+'_'+uuid_name].count()),
        'recordsFiltered': str(mongo[current_user.username+'_'+storeid+'_'+uuid_name].find(dt.filter).count()),
        'draw': int(str(dt.draw)),  # cast draw as integer to prevent XSS
        'data':processed_results
    })
@app.route('/ml_upload/<storeid>')
@login_required
def ml_upload(storeid):
    app=TApp.query.filter_by(data_folder=storeid).first()
    if app is not None:
        return render_template('ml_upload.html',app=app)
    redirect('/')
@app.route('/process_new_ml',methods=['POST'])
@login_required
def process_new_app():
    uuid_name=str(uuid.uuid4())
    app=TApp()
    app.name=request.form.get('name')
    app.desc=request.form.get('desc')
    app.data_folder=uuid_name
    app.user_id=current_user.id
    app.category_id=1
    db.session.add(app)
    db.session.commit()
    return redirect("/")
@app.route('/get_data/<storeid>/<fileid>')
@login_required
def get_data_ml(storeid,fileid):
    result=[]
    app=TApp.query.filter_by(data_folder=storeid).first()
    if app is not None:
        return render_template('ml_upload.html',app=app)
    return  json.dumps(result)
