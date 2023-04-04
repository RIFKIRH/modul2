from flask import Blueprint, jsonify, request, make_response, render_template
from flask import current_app as app
from flask_jwt_extended import get_jwt, jwt_required
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from time import gmtime, strftime
import hashlib
import datetime
import requests
import cv2
import os
import numpy as np
import base64
import random
import json
import warnings
import string

from . models import Data

#11 superadmin, 21 Customer
role_group_super_admin = ["11"]
role_group_customer = ["21"]
role_group_all = ["11", "21"]

#now = datetime.datetime.now()

laundry = Blueprint('laundry', __name__, static_folder = '../../upload/laundry', static_url_path="/media")

#region ================================= FUNGSI-FUNGSI AREA ==========================================================================

def tambahLogs(logs):
	f = open(app.config['LOGS'] + "/" + secure_filename(strftime("%Y-%m-%d"))+ ".txt", "a")
	f.write(logs)
	f.close()

def save(encoded_data, filename):
	arr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
	img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
	return cv2.imwrite(filename, img)

def permission_failed():
    return make_response(jsonify({'error': 'Permission Failed','status_code':403}), 403)

def request_failed():
    return make_response(jsonify({'error': 'Request Failed','status_code':403}), 403)

def defined_error(description, error="Defined Error", status_code=499):
	return make_response(jsonify({'description':description,'error': error,'status_code':status_code}), status_code)

def parameter_error(description, error= "Parameter Error", status_code=400):
	if app.config['PRODUCT_ENVIRONMENT'] == "DEV":
		return make_response(jsonify({'description':description,'error': error,'status_code':status_code}), status_code)
	else:
		return make_response(jsonify({'description':"Terjadi Kesalahan Sistem",'error': error,'status_code':status_code}), status_code)

def bad_request(description):
	if app.config['PRODUCT_ENVIRONMENT'] == "DEV":
		return make_response(jsonify({'description':description,'error': 'Bad Request','status_code':400}), 400) #Development
	else:
		return make_response(jsonify({'description':"Terjadi Kesalahan Sistem",'error': 'Bad Request','status_code':400}), 400) #Production

def randomString(stringLength):
	"""Generate a random string of fixed length """
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def random_string_number_only(stringLength):
	letters = string.digits
	return ''.join(random.choice(letters) for i in range(stringLength))

def get_timestamp():
	return datetime.datetime.utcnow() + datetime.timedelta(hours=7)

def get_timestamp_str(timestamp=(datetime.datetime.utcnow() + datetime.timedelta(hours=7))):
	return timestamp.strftime("%Y-%m-%d %H:%M:%S")

#endregion ================================= FUNGSI-FUNGSI AREA ===============================================================


#region ================================= ITEM LAUNDRY AREA ==========================================================================

@laundry.route('/get_item', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_item():
	try:
		ROUTE_NAME = str(request.path)

		dt = Data()

		query = """ SELECT a.*
					FROM lndr_item AS a
					WHERE a.is_delete!=1 """
		values = ()

		page = request.args.get("page")
		id_item = request.args.get("id_item")
		search = request.args.get("search")
		order_by = request.args.get("order_by")

		if (page == None):
			page = 1
		if id_item:
			query += " AND a.id_item = %s "
			values += (id_item, )
		if search:
			query += """ AND CONCAT_WS("|", a.nama_item) LIKE %s """
			values += ("%"+search+"%", )

		if order_by:
			if order_by == "id_asc":
				query += " ORDER BY a.id_item ASC "
			elif order_by == "id_desc":
				query += " ORDER BY a.id_item DESC "

			elif order_by == "nama_asc":
				query += " ORDER BY a.nama_item ASC "
			elif order_by == "nama_desc":
				query += " ORDER BY a.nama_item DESC "

			else:
				query += " ORDER BY a.id_item DESC "
		else:
			query += " ORDER BY a.id_item DESC "

		rowCount = dt.row_count(query, values)
		hasil = dt.get_data_lim(query, values, page)
		hasil = {'data': hasil , 'status_code': 200, 'page': page, 'offset': '10', 'row_count': rowCount}
		########## INSERT LOG ##############
		imd = ImmutableMultiDict(request.args)
		imd = imd.to_dict()
		param_logs = "[" + str(imd) + "]"
		try:
			logs = secure_filename(get_timestamp_str())+" - "+ROUTE_NAME+" - id_user = "+str(id_user)+" - roles = "+str(role)+" - param_logs = "+param_logs+"\n"
		except Exception as e:
			logs = secure_filename(get_timestamp_str())+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL - param_logs = "+param_logs+"\n"
		tambahLogs(logs)
		####################################
		return make_response(jsonify(hasil),200)
	except Exception as e:
		return bad_request(str(e))

@laundry.route('/insert_item', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def insert_item():
	try:
		ROUTE_NAME = str(request.path)

		role 	= str(get_jwt()["role"])
		id_user = str(get_jwt()["id_user"])

		if role not in role_group_all:
			return permission_failed()

		dt = Data()
		data = request.json

		# Check mandatory data
		if "nama_item" not in data:
			return parameter_error("Missing nama_item in Request Body")
		if "harga" not in data:
			return parameter_error("Missing harga in Request Body")
		if "harga_diskon" not in data:
			return parameter_error("Missing harga_diskon in Request Body")
		if "is_diskon" not in data:
			return parameter_error("Missing is_diskon in Request Body")


		nama_item 		= data["nama_item"]
		harga 			= data["harga"]

		# Cek data-data opsional

		if "harga_diskon" in data:
			harga_diskon = data["harga_diskon"]
		else:
			harga_diskon = harga

		if "is_diskon" in data:
			is_diskon = data["is_diskon"]
		else:
			is_diskon = 0

		# Insert ke tabel db
		query = "INSERT INTO lndr_item (nama_item, harga, harga_diskon, is_diskon) VALUES (%s, %s, %s, %s)"
		values = (nama_item, harga, harga_diskon, is_diskon)
		id_item = dt.insert_data_last_row(query, values)

		hasil = "Berhasil menambahkan item laundry"
		hasil_data = {
			"id_item" : id_item
		}
		try:
			logs = secure_filename(get_timestamp_str())+" - "+ROUTE_NAME+" - id_user = "+str(id_user)+" - roles = "+str(role)+"\n"
		except Exception as e:
			logs = secure_filename(get_timestamp_str())+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
		tambahLogs(logs)
		return make_response(jsonify({'status_code':200, 'description': hasil, 'data' : hasil_data} ), 200)
	except Exception as e:
		return bad_request(str(e))

@laundry.route('/update_item', methods=['PUT', 'OPTIONS'])
@jwt_required()
@cross_origin()
def update_item():
	try:
		ROUTE_NAME = str(request.path)

		role 	= str(get_jwt()["role"])
		id_user = str(get_jwt()["id_user"])

		if role not in role_group_all:
			return permission_failed()


		dt = Data()
		data = request.json

		if "id_item" not in data:
			return parameter_error("Missing id_item in Request Body")

		id_item = data["id_item"]

		# Cek apakah data lokasi ada
		query_temp = "SELECT a.id_item FROM lndr_item a WHERE a.is_delete != 1 AND a.id_item = %s"
		values_temp = (id_item, )
		data_temp = dt.get_data(query_temp, values_temp)
		if len(data_temp) == 0:
			return defined_error("Gagal, Data item laundry tidak ditemukan")

		query = """ UPDATE lndr_item SET id_item=id_item """
		values = ()

		if "nama_item" in data:
			nama_item = data["nama_item"]
			query += """ ,nama_item = %s """
			values += (nama_item, )

		if "harga" in data:
			harga = data["harga"]
			query += """ ,harga = %s """
			values += (harga, )

		if "harga_diskon" in data:
			harga_diskon = data["harga_diskon"]
			query += """ ,harga_diskon = %s """
			values += (harga_diskon, )

		if "is_diskon" in data:
			is_diskon = data["is_diskon"]
			# validasi data is_delete
			if str(is_diskon) not in ["0", "1"]:
				return parameter_error("Invalid id_diskon Value")
			query += """ ,is_diskon = %s """
			values += (is_diskon, )

		if "is_delete" in data:
			is_delete = data["is_delete"]
			# validasi data is_delete
			if str(is_delete) not in ["1"]:
				return parameter_error("Invalid is_delete Value")
			query += """ ,is_delete = %s """
			values += (is_delete, )

		query += """ WHERE id_item = %s """
		values += (id_item, )
		dt.insert_data(query, values)

		hasil = "Berhasil mengubah data item laundry"
		try:
			logs = secure_filename(get_timestamp_str())+" - "+ROUTE_NAME+" - id_user = "+str(id_user)+" - roles = "+str(role)+"\n"
		except Exception as e:
			logs = secure_filename(get_timestamp_str())+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
		tambahLogs(logs)
		return make_response(jsonify({'status_code':200, 'description': hasil} ), 200)
	except Exception as e:
		return bad_request(str(e))

#endregion ================================= ITEM LAUNDRY AREA ==========================================================================

