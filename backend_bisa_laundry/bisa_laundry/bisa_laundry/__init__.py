# -*- coding: utf-8 -*-
import sys
from flask import Flask, jsonify, request, make_response, render_template, redirect
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from time import gmtime, strftime
import json
import datetime
import os
import base64
import random
import hashlib
import warnings

from . data import Data
from . import config as CFG


## IMPORT BLUEPRINT
# from .contoh_blueprint.controllers import contoh_blueprint
from .user.controllers import user
from .lokasi.controllers import lokasi
from .dapur.controllers import dapur
from .utensil.controllers import utensil
from .transaksi.controllers import transaksi
from .brosur.controllers import brosur
from .pos.controllers import pos
from .daerah.controllers import daerah

#region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONFIGURATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
app = Flask(__name__, static_url_path=None) #panggil modul flask

# CORS Configuration
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS']							= 'Content-Type'

# Flask JWT Extended Configuration
app.config['SECRET_KEY'] 							= CFG.JWT_SECRET_KEY
app.config['JWT_HEADER_TYPE']						= CFG.JWT_HEADER_TYPE
app.config['JWT_ACCESS_TOKEN_EXPIRES'] 				= datetime.timedelta(days=30) #30 hari token JWT expired
jwt = JWTManager(app)

# Application Configuration
app.config['PRODUCT_ENVIRONMENT']					= CFG.PRODUCT_ENVIRONMENT
app.config['BACKEND_BASE_URL']						= CFG.BACKEND_BASE_URL

app.config['BISAAI_MAIL_SERVER']					= CFG.BISAAI_MAIL_SERVER
app.config['BISAAI_MAIL_SENDER']					= CFG.BISAAI_MAIL_SENDER
app.config['BISAAI_MAIL_API_KEY']					= CFG.BISAAI_MAIL_API_KEY

app.config['BISAAIPAYMENT_BASE_URL']				= CFG.BISAAIPAYMENT_BASE_URL
app.config['BISAAIPAYMENT_KEY']						= CFG.BISAAIPAYMENT_KEY

# LOGS FOLDER PATH
app.config['LOGS'] 									= CFG.LOGS_FOLDER_PATH

# UPLOAD FOLDER PATH
UPLOAD_FOLDER_PATH									= CFG.UPLOAD_FOLDER_PATH

# Cek apakah Upload Folder Path sudah diakhiri dengan slash atau belum
if UPLOAD_FOLDER_PATH[-1] != "/":
	UPLOAD_FOLDER_PATH							= UPLOAD_FOLDER_PATH + "/"

app.config['UPLOAD_FOLDER_FOTO_USER'] 						= UPLOAD_FOLDER_PATH+"foto_user/"
app.config['UPLOAD_FOLDER_FOTO_LOKASI_KITCHEN'] 			= UPLOAD_FOLDER_PATH+"lokasi/foto_lokasi/"
app.config['UPLOAD_FOLDER_FOTO_DAPUR'] 						= UPLOAD_FOLDER_PATH+"dapur/foto_dapur/"
app.config['UPLOAD_FOLDER_FOTO_BUKTI_BAYAR'] 				= UPLOAD_FOLDER_PATH+"dapur/foto_bukti_bayar"
app.config['UPLOAD_FOLDER_FOTO_UTENSIL'] 					= UPLOAD_FOLDER_PATH+"utensil/foto_utensil/"
app.config['UPLOAD_FOLDER_LOGO_METODE_PEMBAYARAN'] 			= UPLOAD_FOLDER_PATH+"transaksi/logo_metode_pembayaran"
app.config['UPLOAD_FOLDER_FOTO_BRAND'] 						= UPLOAD_FOLDER_PATH+"pos/foto_brand/"
app.config['UPLOAD_FOLDER_FOTO_PRODUK'] 					= UPLOAD_FOLDER_PATH+"pos/foto_produk/"
app.config['UPLOAD_FOLDER_FOTO_PEMBAYARAN'] 				= UPLOAD_FOLDER_PATH+"pos/foto_pembayaran/"
app.config['UPLOAD_FOLDER_FOTO_QRSCAN'] 					= UPLOAD_FOLDER_PATH+"pos/foto_qrscan/"

#Create folder if doesn't exist
list_folder_to_create = [
	app.config['LOGS'],
	app.config['UPLOAD_FOLDER_FOTO_USER'],
	app.config['UPLOAD_FOLDER_FOTO_LOKASI_KITCHEN'],
	app.config['UPLOAD_FOLDER_FOTO_DAPUR'],
	app.config['UPLOAD_FOLDER_FOTO_BUKTI_BAYAR'],
	app.config['UPLOAD_FOLDER_FOTO_UTENSIL'],
	app.config['UPLOAD_FOLDER_LOGO_METODE_PEMBAYARAN'],
	app.config['UPLOAD_FOLDER_FOTO_BRAND'],
	app.config['UPLOAD_FOLDER_FOTO_PRODUK'],
	app.config['UPLOAD_FOLDER_FOTO_PEMBAYARAN'],
	app.config['UPLOAD_FOLDER_FOTO_QRSCAN']
]
for x in list_folder_to_create:
	if os.path.exists(x) == False:
		os.makedirs(x)

#endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONFIGURATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCTION AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

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

def tambahLogs(logs):
	f = open(app.config['LOGS'] + "/" + secure_filename(strftime("%Y-%m-%d"))+ ".txt", "a")
	f.write(logs)
	f.close()

def get_timestamp():
	return datetime.datetime.utcnow() + datetime.timedelta(hours=7)

def get_timestamp_str(timestamp=(datetime.datetime.utcnow() + datetime.timedelta(hours=7))):
	return timestamp.strftime("%Y-%m-%d %H:%M:%S")

#endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCTION AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> INDEX ROUTE AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@app.route("/")
def homeee():
	return "Home Backend BISA LAUNDRY"

#endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> INDEX ROUTE AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AUTH AREA (JWT) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@app.route("/login_admin", methods=["POST"])
@cross_origin()
def login_admin():
	ROUTE_NAME = request.path

	data = request.json
	if "email" not in data:
		return parameter_error("Missing email in Request Body")
	if "password" not in data:
		return parameter_error("Missing password in Request Body")

	email = data["email"]
	password = data["password"]

	email = email.lower()
	password_enc = hashlib.md5(password.encode('utf-8')).hexdigest() # Convert password to md5

	# Check credential in database
	dt = Data()
	query = """ SELECT a.id_admin, b.id_user, b.email, b.password
				FROM admin AS a LEFT JOIN user AS b
				WHERE a.status_admin=1 AND a.is_delete!=1 AND b.status_user=1 AND b.is_delete!=1 AND
				b.email=%s """
	values = (email, )
	data_user = dt.get_data(query, values)
	if len(data_user) == 0:
		return defined_error("Email tidak terdaftar atau Akun tidak aktif", "Invalid Credential", 401)

	data_user = data_user[0]
	db_id_user = data_user["id_user"]
	db_id_admin = data_user["id_admin"]
	db_password = data_user["password"]

	if password_enc != db_password:
		return defined_error("Password Salah", "Invalid Credential", 401)

	role = 11
	role_desc = "ADMIN"

	jwt_payload = {
		"id_user" : db_id_user,
		"id_admin" : db_id_admin,
		"role" : role,
		"role_desc" : role_desc,
		"email" : email
	}

	access_token = create_access_token(email, additional_claims=jwt_payload)

	# Update waktu terakhir login
	query_temp = "UPDATE admin SET waktu_terakhir_login_admin = %s WHERE id_admin = %s"
	values_temp = (get_timestamp(), db_id_admin, )
	dt.insert_data(query_temp, values_temp)

	try:
		logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = "+str(db_id_user)+" - roles = "+str(role)+"\n"
	except Exception as e:
		logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
	tambahLogs(logs)

	return jsonify(access_token=access_token)

@app.route("/login_customer", methods=["POST"])
@cross_origin()
def login_customer():
	ROUTE_NAME = request.path

	data = request.json
	if "email" not in data:
		return parameter_error("Missing email in Request Body")
	if "password" not in data:
		return parameter_error("Missing password in Request Body")

	email = data["email"]
	password = data["password"]

	email = email.lower()
	password_enc = hashlib.md5(password.encode('utf-8')).hexdigest() # Convert password to md5

	# Check credential in database
	dt = Data()
	query = """ SELECT a.id_customer, a.id_user,  b.email, b.password
			FROM customer AS a LEFT JOIN user AS b
			WHERE a.status_customer=1 AND a.is_delete != 1 AND b.is_delete !=1 AND
			b.email = %s """
	values = (email, )
	data_user = dt.get_data(query, values)
	if len(data_user) == 0:
		return defined_error("Email tidak terdaftar atau Akun tidak aktif", "Invalid Credential", 401)

	data_user = data_user[0]
	db_id_user = data_user["id_user"]
	db_id_customer = data_user["id_customer"]
	db_password = data_user["password"]

	if password_enc != db_password:
		return defined_error("Password Salah", "Invalid Credential", 401)

	role = 21
	role_desc = "CUSTOMER"

	jwt_payload = {
		"id_user" : db_id_user,
		"id_customer" : db_id_customer,
		"role" : role,
		"role_desc" : role_desc,
		"email" : email
	}

	access_token = create_access_token(email, additional_claims=jwt_payload)

	# Update waktu terakhir login customer
	query_temp = "UPDATE customer SET waktu_terakhir_login_customer = %s WHERE id_customer = %s"
	values_temp = (get_timestamp(), db_id_customer, )
	dt.insert_data(query_temp, values_temp)

	try:
		logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = "+str(db_id_user)+" - roles = "+str(role)+"\n"
	except Exception as e:
		logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
	tambahLogs(logs)

	return jsonify(access_token=access_token)

@app.route('/cek_credential', methods=['GET', 'OPTIONS'])
@jwt_required() #Need JWT Token
@cross_origin()
def cek_credential():
	dt = Data()

	id_customer = str(get_jwt()["id_customer"])
	role 	= str(get_jwt()["role"])

	dt = Data()
	query = "SELECT * FROM user WHERE id_customer = %s AND is_delete = 0"
	values = (id_customer, )
	hasil = dt.get_user(query, values)


	# Get role description
	query_temp = "SELECT role_description FROM static_role_description WHERE id_role = %s"
	values_temp = (role, )
	data_role = dt.get_data(query_temp, values_temp)
	if len(data_role) == 0:
		role_description = "UNDEFINED"
	else:
		role_description = data_role[0]["role_description"]

	# Add role and role_description to json payload
	hasil[0]["role"] = role
	hasil[0]["role_description"] = role_description

	if len(hasil) == 0:
		return defined_error("User Not Found", "Data not found", 404)

	return jsonify(hasil)

#endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AUTH AREA (JWT) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ERROR HANDLER AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# fungsi error handle Halaman Tidak Ditemukan
@app.errorhandler(404)
@cross_origin()
def not_found(error):
	return make_response(jsonify({'error': 'Tidak Ditemukan','status_code':404}), 404)

#fungsi error handle Halaman internal server error
@app.errorhandler(500)
@cross_origin()
def not_found(error):
	return make_response(jsonify({'error': 'Error Server','status_code':500}), 500)

#endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ERROR HANDLER AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#--------------------- REGISTER BLUEPRINT ------------------------

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(lokasi, url_prefix='/lokasi')
app.register_blueprint(dapur, url_prefix='/dapur')
app.register_blueprint(utensil, url_prefix='/utensil')
app.register_blueprint(transaksi, url_prefix='/transaksi')
app.register_blueprint(brosur, url_prefix='/brosur')
app.register_blueprint(pos, url_prefix='/pos')
app.register_blueprint(daerah, url_prefix='/daerah')
#--------------------- END REGISTER BLUEPRINT ------------------------

