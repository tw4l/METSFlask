from flask import render_template, flash
from lxml import etree, objectify
from METSFlask import db
from sqlalchemy import exc
from .models import METSFile, FSFile, ADMID, \
                    PREMISObject, PREMISEvent, \
                    DublinCore
import math
import metsrw
import os


def convert_size(size):
    # convert size ffrom bytes to human-readable form
    size_name = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size/p)
    s = str(s)
    s = s.replace('.0', '')
    return '{} {}'.format(s, size_name[i])


class METS(object):
    """
    Class for METS file parsing methods
    """

    def __init__(self, path, filename, nickname, metsfile_id=None):
        self.path = os.path.abspath(path)
        self.filename = filename
        self.nickname = nickname
        self.metsfile_id = metsfile_id

    def __str__(self):
        return self.path

    def _strip_namespaces(self, root):
        """
        Strip namespaces from XML
        """
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'):
                continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i+1:]
        objectify.deannotate(root, cleanup_namespaces=True)

    def _parse_dc(self):
        """
        Parse SIP-level Dublin Core metadata into dc_model dictionary.
        Based on parse_dc function from Archivematica parse_mets_to_db.py
        script:

        https://github.com/artefactual/archivematica/blob/
        92d7abd238585e64e6064bc3f1ddfc663c4d3ace/src/MCPClient/
        lib/clientScripts/parse_mets_to_db.py
        """
        # Open XML file and strip namespaces
        tree = etree.parse(self.path)
        root = tree.getroot()
        self._strip_namespaces(root)

        # Parse dmdsecs
        dmds = root.xpath('dmdSec/mdWrap[@MDTYPE="DC"]/parent::*')
        if len(dmds) > 0:
            # Want most recently updated
            dmds = sorted(dmds, key=lambda e: e.get('CREATED'))
            # Only want SIP DC, not file DC
            div = root.find(
                'structMap/div/div[@TYPE="Directory"][@LABEL="objects"]'
            )
            dmdids = div.get('DMDID')
            # No SIP DC
            if dmdids is None:
                print("No dmdsec with LABEL='objects' found.")
                return
            dmdids = dmdids.split()
            for dmd in dmds[::-1]:  # Reversed
                if dmd.get('ID') in dmdids:
                    dc_xml = dmd.find('mdWrap/xmlData/dublincore')
                    break
            # Save entries to datababase
            for elem in dc_xml:
                dublincore_instance = DublinCore(
                    elem.tag,
                    elem.text,
                    self.metsfile_id
                )
                db.session.add(dublincore_instance)
                db.session.commit()

    def _parse_premis_objects(self, premis_objects, fsfile_id):
        """
        For item in premis_objects list, parse data about
        the PREMIS Object and save to database.
        """
        for premis_object in premis_objects:
            msg_digest = premis_object.object_characteristics__fixity__message_digest
            msg_digest_algorithm = premis_object.object_characteristics__fixity__message_digest_algorithm
            size = premis_object.size
            size_hr = convert_size(int(size))
            format_name = premis_object.object_characteristics__format__format_designation__format_name
            format_version = premis_object.object_characteristics__format__format_designation__format_version
            if not isinstance(format_version, str):
                format_version = ''
            registry_key = premis_object.object_characteristics__format__format_registry__format_registry_key
            if not isinstance(registry_key, str):
                registry_key = ''
            registry_name = premis_object.object_characteristics__format__format_registry__format_registry_name
            if not isinstance(registry_name, str):
                registry_name = ''
            original_name = premis_object.findtext('original_name')
            # TODO - get modified date!
            # Try to convert PREMIS Object to XML
            # try:
            # raw_output = premis_object.tostring()
            # except ValueError:
            #     print('Unable to convert PREMIS Object to XML. Reverting to string conversion.')
            #     raw_output = str(premis_object)
            premis_obj_instance = PREMISObject(
                str(premis_object),
                msg_digest,
                msg_digest_algorithm,
                size,
                size_hr,
                format_name,
                format_version,
                registry_key,
                registry_name,
                original_name,
                fsfile_id
            )
            db.session.add(premis_obj_instance)
            db.session.commit()

    def _parse_premis_events(self, premis_events, fsfile_id):
        """
        For item in premis_events list, parse data about
        the PREMIS Event and save to database.
        """
        for premis_event in premis_events:
            # Try to save data as string of XML
            raw_output = premis_event.tostring(pretty_print=True)\
                .decode('utf8')
            root = etree.fromstring(raw_output)
            self._strip_namespaces(root)
            event_uuid = root.find('.//eventIdentifierValue').text
            event_type = root.find('.//eventType').text
            event_datetime = root.find('.//eventDateTime').text
            event_detail = root.find('.//eventDetail').text
            event_outcome = root.find('.//eventOutcome').text
            event_detail_note = root.find('.//eventOutcomeDetailNote').text
            # Save to db
            premis_event_instance = PREMISEvent(
                raw_output,
                event_uuid,
                event_type,
                event_datetime,
                event_detail,
                event_outcome,
                event_detail_note,
                fsfile_id
            )
            db.session.add(premis_event_instance)
            db.session.commit()

    def parse_mets(self):
        """
        Parse METS file and save relevant info to db
        """

        # Save METSFile moodel to db and save ID to self
        mets_instance = METSFile(self.filename, self.nickname)
        try:
            db.session.add(mets_instance)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            flash('Error: This METS file has already been uploaded.')
            return render_template('upload.html')
        self.metsfile_id = METSFile.query.filter_by(metsfile=self.filename)\
            .one().id
        # Parse FSEntries and write to db
        mets = metsrw.METSDocument.fromfile(self.path)
        fs_entries = mets.all_files()
        for f in fs_entries:
            # Iterate over files (skip directories)
            if f.type == 'Item':
                # Get file_id
                file_id = str(f.file_id())
                # Write to db
                fs_file = FSFile(
                    f.path,
                    f.use,
                    f.file_uuid,
                    file_id,
                    self.metsfile_id
                )
                db.session.add(fs_file)
                db.session.commit()
                # Get FSFile ID
                fsfile_id = FSFile.query.filter_by(path=f.path).one().id
                # Save associated ADMIDs to db
                admids = f.admids
                for admid in admids:
                    admid_instance = ADMID(admid, fsfile_id)
                    db.session.add(admid_instance)
                    db.session.commit()
                # Save associated PREMIS Objects to db
                premis_objects = f.get_premis_objects()
                self._parse_premis_objects(premis_objects, fsfile_id)
                # TODO - write some static info from first PREMIS Object to FSFile
                # Save associated PREMIS Events to db
                premis_events = f.get_premis_events()
                self._parse_premis_events(premis_events, fsfile_id)
        # Find and parse most recent dmdsec with @LABEL='objects'
        self._parse_dc()
