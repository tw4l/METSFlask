from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from lxml import etree
from sqlalchemy import exc
from werkzeug.utils import secure_filename
from METSFlask import app, db
from .models import METSFile, FSFile, ADMID, \
                    PREMISObject, PREMISEvent, \
                    DublinCore
from .parsemets import METS
import os


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() \
        in app.config['ALLOWED_EXTENSIONS']


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    mets_instances = METSFile.query.all()
    return render_template('index.html', mets_instances=mets_instances)


@app.route("/upload", methods=['GET', 'POST'])
def render_page():
    return render_template('upload.html')


@app.route('/uploadsuccess', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        nickname = request.form.get("nickname")
        # Check if the post request includes file
        if 'file' not in request.files:
            flash('Error: No file selected')
            return render_template('upload.html')
        file = request.files['file']
        if file.filename == '':
            flash('Error: No file selected')
            return render_template('upload.html')
        # If file is present, save and parse file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mets_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            mets_filename = os.path.basename(filename)
            # Parse METSFile to database
            mets_instance = METS(mets_path, mets_filename, nickname)
            mets_instance.parse_mets()
            # Delete file from uploads folder
            # TODO: maybe not necessary? if kept, could enable download
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Return success template - TODO: instead, go to AIP page?
            return render_template('uploadsuccess.html')


@app.route('/aip/<mets_file>')
def show_aip(mets_file):
    mets_instance = METSFile.query.filter_by(metsfile='%s' % (mets_file))\
        .first()
    mets_id = mets_instance.id
    mets_file = mets_instance.metsfile
    all_files = FSFile.query.filter_by(metsfile_id=mets_id)
    filecount = all_files.count()
    original_files = all_files.filter_by(use='original')
    original_filecount = original_files.count()
    preservation_files = all_files.filter_by(use='preservation')
    preservation_filecount = preservation_files.count()
    dcmetadata = DublinCore.query.filter_by(metsfile_id=mets_id)
    aip_uuid = mets_file[5:41]
    return render_template(
        'aip.html',
        all_files=all_files,
        filecount=filecount,
        original_files=original_files,
        original_filecount=original_filecount,
        preservation_filecount=preservation_filecount,
        mets_file=mets_file,
        aip_uuid=aip_uuid,
        dcmetadata=dcmetadata
    )


@app.route('/delete/<mets_file>')
def confirm_delete_aip(mets_file):
    return render_template('delete.html', mets_file=mets_file)


@app.route('/deletesuccess/<mets_file>')
def delete_aip(mets_file):
    mets_instance = METSFile.query.filter_by(metsfile='%s' % (mets_file))\
        .first()
    try:
        db.session.delete(mets_instance)
        db.session.commit()
        return render_template('deletesuccess.html')
    except Exception:
        flash('Unable to delete')
        return render_template('delete.html', mets_file=mets_file)


@app.route('/aip/<mets_file>/file/<UUID>')
def show_file(mets_file, UUID):
    file_instance = FSFile.query.filter_by(file_uuid=UUID).first()
    admids = ADMID.query.filter_by(fsfile_id=file_instance.id)
    premis_objects = PREMISObject.query.filter_by(fsfile_id=file_instance.id)
    premis_events = PREMISEvent.query.filter_by(fsfile_id=file_instance.id)
    return render_template(
        'detail.html',
        file_details=file_instance,
        admids=admids,
        premis_objects=premis_objects,
        premis_events=premis_events,
        mets_file=mets_file
    )
