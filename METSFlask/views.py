import datetime
import fnmatch
import math
import os
import sys

from collections import Counter
from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from lxml import etree, objectify
from werkzeug.utils import secure_filename

from METSFlask import app, db
from .models import METS
from .parsemets import METSFile, convert_size


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    mets_instances = METS.query.all()
    return render_template('index.html', mets_instances=mets_instances)


@app.route("/upload", methods=['GET', 'POST'])
def render_page():
    return render_template('upload.html')


@app.route('/uploadsuccess', methods=['GET', 'POST'])
def upload_file():
    error = None
    if request.method == 'POST':
        nickname = request.form.get("nickname")
        # check if the post request has the file part
        if 'file' not in request.files:
            error = 'No file'
            return render_template('upload.html', error=error)
        file = request.files['file']
        if file.filename == '':
            error = 'No file'
            return render_template('upload.html', error=error)
        if file and allowed_file(file.filename):
            # Upload and parse file
            try:
                filename = secure_filename(file.filename)
                upload_dir = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                # Save file
                mets_path = os.path.join(upload_dir, filename)
                aip_name = os.path.basename(filename)
                file.save(mets_path)
                # Parse METS file to database
                mets = METSFile(mets_path, aip_name, nickname)
                mets.parse_mets()
                # Delete file from uploads folder
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                # Render index page
                mets_instances = METS.query.all()
                return render_template('index.html', mets_instances=mets_instances)
            except Exception:
                pass
        error = 'Unable to process uploaded file'
        return render_template('upload.html', error=error)
    return render_template('upload.html', error=error)


@app.route('/aip/<mets_file>')
def show_aip(mets_file):
    try:
        mets_instance = METS.query.filter_by(metsfile='%s' % (mets_file)).first()
        original_files = mets_instance.metslist
        dcmetadata = mets_instance.dcmetadata
        filecount = mets_instance.originalfilecount
        formatLabels = []
        for original_file in original_files:
            formatLabels.append(original_file['format'])
        formatCounts = Counter(formatLabels)
        labels = list(formatCounts.keys())
        values = list(formatCounts.values())
        aip_uuid = mets_file[5:41]
        return render_template('aip.html', 
            labels=labels, values=values, original_files=original_files,
            mets_file=mets_file, dcmetadata=dcmetadata, filecount=filecount,
            aip_uuid=aip_uuid)
    except Exception:
        return render_template('404.html'), 404


@app.route('/delete/<mets_file>')
def confirm_delete_aip(mets_file):
    return render_template('delete.html', mets_file=mets_file)


@app.route('/deletesuccess/<mets_file>')
def delete_aip(mets_file):
    try:
        # Delete db instance
        mets_instance = METS.query.filter_by(metsfile='%s' % (mets_file)).first()
        db.session.delete(mets_instance)
        db.session.commit()
        # Render index page
        return redirect("/")
    except Exception:
        pass
    return redirect("/")
    


@app.route('/aip/<mets_file>/file/<UUID>')
def show_file(mets_file, UUID):
    mets_instances = METS.query.filter_by(metsfile='%s' % (mets_file)).first()
    original_files = mets_instances.metslist
    for original_file in original_files:
        if original_file["uuid"] == UUID:
            target_original_file = original_file
            break
    return render_template('detail.html', original_file=target_original_file, mets_file=mets_file)
