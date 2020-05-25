"""
This module is used to test the routes for the reader on the server.
"""
from flask import url_for
from flask_jwt_extended import create_access_token
from flask_testing import TestCase
import json
from script.create_db_data import populate_db

from visualize import create_app, db
from visualize.models import Reader, Approver, Admin

app = create_app()
app.app_context().push()  # make all test use this context
db.drop_all()
app.config["ENV"] = "testing"

i = 0  # index of test Emails


class BaseTestCase(TestCase):
	""" Base class for unittest. """

	# Oklart ifall vi behöver dessa...
	SQLALCHEMY_DATABASE_URI = "sqlite://"
	TESTING = True

	def get_new_random_email(self):
		global i
		"""creates a new user email"""
		i += 1
		string = "test{}@test.com".format(i)

		return string

	def get_old_email(self):
		string = "test{}@test.com".format(i)
		return string

	def login(self, email, pas="abcABC123"):
		"""logs in a user"""
		with app.test_client() as client:
			sent = json.dumps({"email": email,
							   "password": pas})
			result = client.post(
				'/login',
				data=sent,
				content_type='application/json',
			)
			access_token = json.loads(result.data.decode("utf-8"))["access_token"]

			headers = {
				'Authorization': 'Bearer {}'.format(access_token)
			}
			return headers

	def populate_reader(self, email, pas="abcABC123"):
		"""
		populates the test db with a reader
		:param pas:
		:param email: users email
		:return: tuple with message from create_reader() and the send message
		"""

		admin_headers = self.login("c@c.c")

		with app.test_client() as client:

			sent = json.dumps({"email": email,
							   "password": pas,
							   "name": "test",
							   "surname": "testson"})
			result = client.post(
				'admin/reader',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			access_token = create_access_token(identity=email)
			headers = {
				'Authorization': 'Bearer {}'.format(access_token)
			}

			res = (result, sent, access_token, headers) # skriv om till dict
			return res

	def populate_approver(self, email, pas="abcABC123"):
		"""
		populates the test db with a reader
		:param pas:
		:param email: users email
		:return: tuple with message from create_reader() and the send message
		"""

		admin_headers = self.login("c@c.c")

		with app.test_client() as client:
			sent = json.dumps({"email": email,
							   "password": pas,
							   "name": "test",
							   "surname": "testson"})
			result = client.post(
				'admin/approver',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			access_token = create_access_token(identity=email)
			headers = {
				'Authorization': 'Bearer {}'.format(access_token)
			}

			res = (result, sent, access_token, headers) # skriv om till dict
			return res

	def populate_admin(self, email, pas="abcABC123"):
		"""
		populates the test db with a reader
		:param pas:
		:param email: users email
		:return: tuple with message from create_reader() and the send message
		"""

		admin_headers = self.login("c@c.c")

		with app.test_client() as client:
			sent = json.dumps({"email": email,
							   "password": pas,
							   "name": "test",
							   "surname": "testson"})
			result = client.post(
				'admin/admin',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			access_token = create_access_token(identity=email)
			headers = {
				'Authorization': 'Bearer {}'.format(access_token)
			}

			res = (result, sent, access_token, headers) # skriv om till dict
			return res

	def create_app(self):
		# app.run()
		return create_app()

	def setUp(self):
		db.create_all()
		populate_db()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


class ReaderRouteTest(BaseTestCase):
	"""class for unittests for reader routes."""

	def test_get_empty_reader(self):
		"""testing get_current_reader if there is no user with that email."""
		email = self.get_new_random_email()
		access_token = create_access_token(email)
		headers = {
			'Authorization': 'Bearer {}'.format(access_token)
		}

		response = self.client.get('reader/self', headers=headers)

		self.assert400(response, "400 if there are no readers ")

	def test_get_reader(self):
		"""testing get_current_reader and create_reader()"""
		email = self.get_new_random_email()
		self.populate_reader(email)

		headers = self.login(email)

		response = self.client.get('/reader/self', headers=headers)
		self.assertStatus(response, 200, "check if the reader request is ok ")

		response_data = json.loads(response.data)
		self.assertEqual(response_data['email'], email,
						 "Check if sent email user is created with is the same as returned")

	def test_order_room(self):
		"""test get_reader_rooms with a good request for the room isy1. """
		room = "isy1"

		with app.test_client() as client:
			sent = json.dumps({"room_text_id": room,
							   "justification": "Because i can"})

			email = self.get_new_random_email()
			res = self.populate_reader(email)
			headers = res[3]

			response = client.post('/reader/room', data=sent, headers=headers, content_type='application/json')
			self.assert200(response, "check if the request is ok")

			self.assertEqual(response.data.decode("utf-8"), "Request for room {} has been sent.".format(room),
							 "Check if the right room is returned. ")

	def test_order_bad_room(self):
		"""test get_reader_rooms with bad room requests"""
		room = "isy1"

		with app.test_client() as client:
			sent = json.dumps({"room_text_id": room,
							   "justification": "Because i can"})
			email = self.get_new_random_email()
			res = self.populate_reader(email)
			headers = res[3]

			# test to send duplicate of room
			res = client.post('/reader/room', data=sent, headers=headers, content_type='application/json')
			self.assert200(res, "check if the request is ok")

			response = client.post('/reader/room', data=sent, headers=headers, content_type='application/json')
			self.assert400(response, "Check so we cant create a duplicate request with the same room")

			# test to send room that does not exist
			sent2 = json.dumps({"room_text_id": room + "abcd",
								"justification": "Because i can"})

			response2 = client.post('/reader/room', data=sent2, headers=headers, content_type='application/json')

			self.assert400(response2, "Check so we cant request a room that dont exist")

	def test_order_ag(self):
		"""test order_ag with a good request for the group 1."""
		ag = 1

		with app.test_client() as client:
			sent = json.dumps({"ag_id": ag,
							   "justification": "Because i can"})

			email = self.get_new_random_email()
			res = self.populate_reader(email)
			headers = res[3]

			response = client.post('/reader/ag', data=sent, headers=headers, content_type='application/json')
			self.assert200(response, "check if the request is ok")

			self.assertEqual(response.data.decode("utf-8"), "Request for access group {} has been sent.".format(ag),
							 "Check if the right room is returned. ")

	def test_get_orders(self):
		""" test get_order, needs to add rooms and ag to check returns"""

		room = "isy1"
		with app.test_client() as client:
			email = self.get_new_random_email()
			res = self.populate_reader(email)
			headers = res[3]

			sent = json.dumps({"room_text_id": room,
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=headers, content_type='application/json')

			response = client.get('/reader/orders', headers=headers, content_type='application/json')

			self.assert200(response, "check if the request is ok")

	def test_get_all_access(self):
		""" test get_all_access, needs to add ag the user is in to check returns """
		with app.test_client() as client:
			email = self.get_new_random_email()
			res = self.populate_reader(email)
			headers = res[3]

			response = client.get('/reader/access', headers=headers, content_type='application/json')

			self.assert200(response, "check if the request is ok")


class ApproverRouteTest(BaseTestCase):
	"""class for unittests for approver routes"""

	def test_get_readers_for_room(self):
		"""testing get_readers_for_room if there is no user with that email."""
		room = "isy1"

		with app.test_client() as client:
			sent = json.dumps({"room_text_id": room})
			approver_email = "b@b.b"
			approver_headers = self.login(approver_email)

			response = client.post('/approver/readers_for_room', data=sent,
								   headers=approver_headers,
								   content_type='application/json')
			self.assert200(response, "The request was from an approver/admin")

			self.assert200(response, "We get some data")

	def test_approve_room_request(self):
		""" Test if its possible to approve room request."""
		reader_email = self.get_new_random_email()
		res_r = self.populate_reader(reader_email)
		reader_headers = res_r[3]

		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			sent = json.dumps({"room_text_id": "isy1",
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=reader_headers, content_type='application/json')

			response = client.get('approver/orders', headers=approver_headers)
			self.assert200(response, "The request was from an approver/admin")

			response_data = json.loads(response.data.decode("utf-8"))
			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:
						request_id = y['request_id']
						sent2 = json.dumps({"request_id": request_id, "type": "Room", "is_access_granted": True})
						response2 = client.post('approver/access', data=sent2, headers=approver_headers,
												content_type='application/json')
						self.assert200(response2, "We get some data")

	def test_approve_multiple_room_request(self):
		""" Test if its possible to approve multiple room request."""
		reader_email = self.get_new_random_email()

		res_r = self.populate_reader(reader_email)
		reader_headers = res_r[3]

		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			sent = json.dumps({"room_text_id": "isy1",
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=reader_headers, content_type='application/json')

			sent3 = json.dumps({"room_text_id": "isy2",
								"justification": "Because i can"})

			client.post('/reader/room', data=sent3, headers=reader_headers, content_type='application/json')

			response = client.get('approver/orders', headers=approver_headers)
			self.assert200(response, "The request was from an approver/admin")

			response_data = json.loads(response.data.decode("utf-8"))

			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:
						request_id = y['request_id']
						sent2 = json.dumps({"request_id": request_id, "type": "Room", "is_access_granted": True})
						response2 = client.post('approver/access', data=sent2, headers=approver_headers,
												content_type='application/json')
						self.assert200(response2, "We get some data")

	def test_approve_ag_request(self):
		""" Test if its possible to approve ag request."""
		reader_email = self.get_new_random_email()
		res_r = self.populate_reader(reader_email)
		reader_headers = res_r[3]

		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			sent = json.dumps({"ag_id": 1,
							   "justification": "Because i can"})

			client.post('/reader/ag', data=sent, headers=reader_headers, content_type='application/json')

			response = client.get('approver/orders', headers=approver_headers)
			self.assert200(response, "The request was from an approver/admin")

			response_data = json.loads(response.data.decode("utf-8"))
			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:

						request_id = y['request_id']
						sent2 = json.dumps({"request_id": request_id, "type": "AG", "is_access_granted": True})
						response2 = client.post('approver/access', data=sent2, headers=approver_headers,
												content_type='application/json')
						self.assert200(response2, "We get some data")

	def test_get_all_orders_for_logged_in(self):
		""" Test to see all orders for current approver."""
		reader_email = self.get_new_random_email()
		res_r = self.populate_reader(reader_email)
		reader_headers = res_r[3]

		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			sent = json.dumps({"room_text_id": "isy1",
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=reader_headers, content_type='application/json')

			sent = json.dumps({"room_text_id": "isy2",
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=reader_headers, content_type='application/json')

			sent = json.dumps({"room_text_id": "isy3",
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=reader_headers, content_type='application/json')

			response = client.get('approver/orders', headers=approver_headers)
			self.assert200(response, "The request was from an approver/admin")

			response_data = json.loads(response.data.decode("utf-8"))

			nr = 0
			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:
						nr += 1
			self.assertEqual(nr, 3, "Check that we get 3 request to the email")

	def test_get_responsibilities(self):
		""" Tests the route to get all responsibilities, might need to att check for return value"""
		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			response = client.get('/approver/responsibilities', headers=approver_headers,
								  content_type='application/json')

			self.assert200(response, "The request was from an approver/admin")

	def test_get_all_readers(self):
		""" Test to get all readers for a room"""
		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		sent = json.dumps({"room_text_id": "isy2"})

		with app.test_client() as client:
			response = client.post('/approver/readers_for_room', headers=approver_headers, data=sent,
									content_type='application/json')

			self.assert200(response, "The request was from an approver/admin")

	def test_reject_room_request(self):
		""" Test if its possible to reject room request."""
		reader_email = self.get_new_random_email()
		res_r = self.populate_reader(reader_email)
		reader_headers = res_r[3]

		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			sent = json.dumps({"room_text_id": "isy1",
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=reader_headers, content_type='application/json')

			response = client.get('approver/orders', headers=approver_headers)
			self.assert200(response, "The request was from an approver/admin")

			response_data = json.loads(response.data.decode("utf-8"))
			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:
						request_id = y['request_id']
						sent2 = json.dumps({"request_id": request_id, "type": "Room", "is_access_granted": False})
						response2 = client.post('approver/access', data=sent2, headers=approver_headers,
												content_type='application/json')
						self.assert200(response2, "We get some data")

	def test_reject_ag_request(self):
		""" Test if its possible to reject ag request."""
		reader_email = self.get_new_random_email()
		res_r = self.populate_reader(reader_email)
		reader_headers = res_r[3]

		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			sent = json.dumps({"ag_id": 1,
							   "justification": "Because i can"})

			client.post('/reader/ag', data=sent, headers=reader_headers, content_type='application/json')

			response = client.get('approver/orders', headers=approver_headers)
			self.assert200(response, "The request was from an approver/admin")

			response_data = json.loads(response.data.decode("utf-8"))
			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:
						request_id = y['request_id']
						sent2 = json.dumps({"request_id": request_id, "type": "AG", "is_access_granted": False})
						response2 = client.post('approver/access', data=sent2, headers=approver_headers,
												content_type='application/json')
						self.assert200(response2, "We get some data")

	def test_revoke_ag_access(self):
		"""tests to remove a ag from reader"""
		# skapa läsare
		reader_email = self.get_new_random_email()
		self.populate_reader(reader_email)
		ag_id = 2

		reder_header = self.login(reader_email)

		# skapa ag req
		with app.test_client() as client:
			sent = json.dumps({"ag_id": ag_id,
							   "justification": "Because i can"})

			client.post('/reader/ag', data=sent, headers=reder_header, content_type='application/json')

		# approva ag req med approver
		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			response = client.get('approver/orders', headers=approver_headers)
			response_data = json.loads(response.data.decode("utf-8"))
			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:
						request_id = y['request_id']
						sent2 = json.dumps({"request_id": request_id, "type": "AG", "is_access_granted": True})
						client.post('approver/access', data=sent2, headers=approver_headers,
												content_type='application/json')

		with app.test_client() as client:
			url = url_for("approver.get_all_access_for_reader", email=reader_email)
			response = client.get(url, headers=approver_headers)
			x = json.loads(response.data.decode("utf-8"))
			i = 0
			for y in x:
				try:
					self.assertEqual(x[y]['ag_id'], ag_id, "check that we have rooms with the ag we requested")
					self.assertEqual(x[y]['access'], True, "check that we access to that room")
					i += 1
				except KeyError:
					pass

			self.assertNotEqual(i, 0, "check so we got some access")

		# skapa ag req
		with app.test_client() as client:
			sent = json.dumps({"ag_id": ag_id,
							   "email": reader_email})

			respone = client.post('approver/revoke/ag', data=sent, headers=approver_headers, content_type='application/json')
			self.assert200(response, "check that request for revoke ag is ok")
			response = client.get('approver/access_for_reader/{}'.format(reader_email), headers=approver_headers)
			x = json.loads(response.data.decode("utf-8"))
			i = 0
			for y in x:
				try:
					self.assertEqual(x[y]['ag_id'], ag_id, "check that we have rooms with the ag we requested")
					self.assertEqual(x[y]['access'], True, "check that we access to that room")
					i += 1
				except KeyError:
					pass

			self.assertEqual(i, 0, "check so dont have any access any more")

	def test_revoke_room_access(self):
		"""tests to remove a room from a reader"""
		# skapa läsare
		reader_email = self.get_new_random_email()
		self.populate_reader(reader_email)
		room_id = "ing27"

		reader_header = self.login(reader_email)

		# skapa ag req
		with app.test_client() as client:
			sent = json.dumps({"room_text_id": room_id,
							   "justification": "Because i can"})

			client.post('/reader/room', data=sent, headers=reader_header, content_type='application/json')

		# approva ag req med approver
		approver_email = "b@b.b"
		approver_headers = self.login(approver_email)

		with app.test_client() as client:
			response = client.get('approver/orders', headers=approver_headers)
			response_data = json.loads(response.data.decode("utf-8"))
			for x in response_data:
				res_data = response_data[x]
				for y in res_data:
					if y['reader']['email'] == reader_email:
						request_id = y['request_id']
						sent2 = json.dumps({"request_id": request_id, "type": "Room", "is_access_granted": True})
						res = client.post('approver/access', data=sent2, headers=approver_headers,
												content_type='application/json')

		with app.test_client() as client:
			url = url_for("approver.get_all_access_for_reader", email=reader_email)
			response = client.get(url, headers=approver_headers)
			x = json.loads(response.data.decode("utf-8"))
			i = 0
			for y in x:
				print(x[y])
				try:
					if x[y]['name'] == "Korridor":
						self.assertEqual(x[y]['access'], True, "check if we have access to that room")
						i += 1
				except KeyError:
					pass

			self.assertNotEqual(i, 0, "check so we got some access")

		# skapa ag req
		with app.test_client() as client:
			sent = json.dumps({"room_text_id": room_id,
							   "email": reader_email})

			respone = client.post('approver/revoke/room', data=sent, headers=approver_headers, content_type='application/json')
			self.assert200(response, "check that request for revoke room is ok")
			response = client.get('approver/access_for_reader/{}'.format(reader_email), headers=approver_headers)
			x = json.loads(response.data.decode("utf-8"))
			for y in x:
				try:
					if x[y]['name'] == "Korridor":
						self.assertEqual(x[y]['access'], False, "check if we dont got access to that room")
				except KeyError:
					pass


class AdminRouteTest(BaseTestCase):
	"""class for unittests for approver routes"""

	def test_get_all_readers_roles(self):
		"""get all reader and their roles"""
		admin_headers = self.login("c@c.c")

		known_users = ["a@a.a", "b@b.b", "c@c.c"]

		with app.test_client() as client:
			result = client.get(
				'admin/readers',
				headers=admin_headers,
				content_type='application/json',
			)
			lenght_of_expected_list = 0
			for x in json.loads(result.data.decode("utf-8")):
				for y in json.loads(result.data.decode("utf-8"))[x]:
					if y['email'] in known_users:
						lenght_of_expected_list += 1

			self.assertEqual(len(known_users), lenght_of_expected_list,
							 "Checks that we find the 3 users always expected")

	def test_upgrade_to_approver(self):
		""" tests uppgrade to approver with a new reader"""
		admin_headers = self.login("c@c.c")

		reader_email = self.get_new_random_email()
		self.populate_reader(reader_email)

		reader_header = self.login(reader_email)

		reader = Reader.query.filter_by(email=reader_email).first()
		self.assertNotEqual(reader, None, "check that reader exist")

		reader = Approver.query.filter_by(email=reader_email).first()
		self.assertEqual(reader, None, "check that reader is not an approver yet")

		with app.test_client() as client:
			sent = json.dumps({ "email": reader_email})
			request = client.post(
				'admin/upgrade_to_approver',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

		reader = Approver.query.filter_by(email=reader_email).first()
		self.assertNotEqual(reader, None, "check that reader now is approver")

	def test_upgrade_to_admin(self):
		"""tests upgrade to admin with a reader and a approver."""
		admin_headers = self.login("c@c.c")

		# Reader -> admin
		reader_email = self.get_new_random_email()
		self.populate_reader(reader_email)

		reader_header = self.login(reader_email)

		reader = Reader.query.filter_by(email=reader_email).first()
		self.assertNotEqual(reader, None, "check that reader exist")

		reader = Admin.query.filter_by(email=reader_email).first()
		self.assertEqual(reader, None, "check that reader is not an admin yet")

		with app.test_client() as client:
			sent = json.dumps({"email": reader_email})
			request = client.post(
				'admin/upgrade_to_admin',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

		reader = Admin.query.filter_by(email=reader_email).first()
		self.assertNotEqual(reader, None, "check that reader now is admin")

		# approver -> admin
		approver_email = self.get_new_random_email()
		self.populate_approver(approver_email)


		approver_header = self.login(approver_email)

		approver = Reader.query.filter_by(email=approver_email).first()
		self.assertNotEqual(approver, None, "check that reader exist")

		approver = Admin.query.filter_by(email=approver_email).first()
		self.assertEqual(approver, None, "check that reader is not an admin yet")

		with app.test_client() as client:
			sent = json.dumps({"email": approver_email})
			request = client.post(
				'admin/upgrade_to_admin',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

		approver = Admin.query.filter_by(email=approver_email).first()
		self.assertNotEqual(approver, None, "check that reader now is admin")

	def test_create_ag(self):
		"""test to create an ag."""
		# utökning:
		# requesta den nya innan och efter
		# testa skicka in dålig data
		# testa skapa dubblett av rum


		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			sent = json.dumps({"ag_name": "test_ag",
							   "approvers": ["b@b.b"],
							   "room_text_ids": ["isy1", "isy2", "isy"]
							   })
			request = client.post(
				'admin/ag',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

	def test_get_reader(self):
		"""test to get a reader with get_reader"""
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			url = url_for("admin.get_reader", reader_id=46) #46 is a@a.a
			request = client.get(
				url,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")
			print(request.data)

	def test_get_all_approvers(self):
		"""test to get all approvers with get_all_approvers"""
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			request = client.get(
				"admin/approvers/",
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

	def test_get_all_admins(self):
		"""test to get all admins with get_all_admins"""
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			request = client.get(
				"admin/admins/",
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

	def test_get_all_rooms(self):
		"""test to get all rooms with get_all_rooms"""
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			request = client.get(
				"admin/rooms",
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

	def test_delete_user(self):
		"""test to remove a user"""
		# create and get new user
		reader_email = self.get_new_random_email()
		self.populate_reader(reader_email)
		reader_header = self.login(reader_email)

		reader = Reader.query.filter_by(email=reader_email).first()
		self.assertNotEqual(reader, None, "check that reader email is a user")

		# remove user
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			url = url_for("admin.delete_user", reader_email=reader_email)
			request = client.delete(
				url,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

		# try to get user again
		reader = Reader.query.filter_by(email=reader_email).first()
		self.assertEqual(reader, None, "check that reader email is a user")

	def test_remove_card(self):
		"""test to block card"""
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			url = url_for("admin.remove_card", email="a@a.a")
			request = client.delete(
				url,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

	def test_create_reader_approver_admin(self):
		"""test to create reader"""
		# reader
		email = self.get_new_random_email()
		res = self.populate_reader(email)
		result = res[0]

		self.assertStatus(result, 201)
		self.assertEqual(result.data, b'Reader successfully created!', "check that we created a reader")

		# approver
		email = self.get_new_random_email()
		res = self.populate_approver(email)
		result = res[0]

		self.assertStatus(result, 201)
		self.assertEqual(result.data, b'Approver successfully created!', "check that we created a Approver")

		# admin
		email = self.get_new_random_email()
		res = self.populate_admin(email)
		result = res[0]

		self.assertStatus(result, 201)
		self.assertEqual(result.data, b'Admin successfully created!', "check that we created a Admin")

	def test_create_duplicate_reader_approver_admin(self):
		"""testing create_reader() with already existing email"""
		# reader
		email = self.get_new_random_email()
		res = self.populate_reader(email)
		result = res[0]

		self.assertStatus(result, 201)
		self.assertEqual(result.data, b'Reader successfully created!', "check that we created a reader")

		res2 = self.populate_reader(email)
		result2 = res2[0]
		self.assert400(result2, "Check so we cant create a duplicate reader with the same email as another one")

		# approver
		email = self.get_new_random_email()
		res = self.populate_approver(email)
		result = res[0]

		self.assertStatus(result, 201)
		self.assertEqual(result.data, b'Approver successfully created!', "check that we created a Approver")

		res2 = self.populate_approver(email)
		result2 = res2[0]
		self.assert400(result2, "Check so we cant create a duplicate reader with the same email as another one")

		# admin
		email = self.get_new_random_email()
		res = self.populate_admin(email)
		result = res[0]

		self.assertStatus(result, 201)
		self.assertEqual(result.data, b'Admin successfully created!', "check that we created a Admin")

		res2 = self.populate_admin(email)
		result2 = res2[0]
		self.assert400(result2, "Check so we cant create a duplicate reader with the same email as another one")

	def test_create_reader_approver_admin_with_bad_pass(self):
		""" testing create_reader() with bad passwords """
		pas_lst = ["", "ABab1", "abcd1234", "ABCD123", "ABCDabcd", "aBDcµ123"]
		# reader
		for pas in pas_lst:
			email = self.get_new_random_email()
			res = self.populate_reader(email, pas)
			result = res[0]

			self.assertStatus(result, 400)

		# approver
		for pas in pas_lst:
			email = self.get_new_random_email()
			res = self.populate_approver(email, pas)
			result = res[0]

			self.assertStatus(result, 400)

		# admin
		for pas in pas_lst:
			email = self.get_new_random_email()
			res = self.populate_admin(email, pas)
			result = res[0]

			self.assertStatus(result, 400)

	def test_get_all_orders(self):
		"""test to get all orders with test_get_all_orders"""
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			request = client.get(
				"admin/orders",
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

	def test_remove_ag(self):
		""" test to remove ag from approvers approval area with ermove_ag"""
		# utökning: kolla approvers yta innan och efter
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			sent = json.dumps({"ag": 1,
								"approver": 47 # 47 is b@b.b
								})
			request = client.post(
				'admin/remove_for_approver/ag',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")

	def test_remove_room(self):
		""" test to remove ag from approvers approval area with ermove_ag"""
		# utökning: kolla approvers yta innan och efter
		admin_headers = self.login("c@c.c")
		with app.test_client() as client:
			sent = json.dumps({"room": "isy1",
								"approver": 47 # 47 is b@b.b
								})
			request = client.post(
				'admin/remove_for_approver/room',
				data=sent,
				headers=admin_headers,
				content_type='application/json',
			)
			self.assert200(request, "check that request returns ok")
