import mysql.connector as conx

class Database():
	def __init__(self):
		self.conn = conx.connect(host='localhost', user='root', password='root')
		self.cur = self.conn.cursor()
		##########################DATABASE##############################################################
		self.cur.execute("CREATE DATABASE IF NOT EXISTS BLOOD_DONORS")
		self.cur.execute("USE BLOOD_DONORS")
		##########################DONOR TABLE#########################################################################
		self.cur.execute("CREATE TABLE IF NOT EXISTS DONOR(Donor_ID int primary key auto_increment, Name varchar(45), Address varchar(100), ContactNumber varchar(10), DateOfBirth date)")
		########################PATIENT TABLE#########################################################################
		self.cur.execute("CREATE TABLE IF NOT EXISTS PATIENT(Patient_ID int primary key auto_increment, Name varchar(45), BloodType varchar(2), ContactNumber varchar(10))")
		##########################BLOODBANK TABLE#####################################################################
		self.cur.execute("CREATE TABLE IF NOT EXISTS BLOODBANK(BloodBank_ID int primary key auto_increment, Name varchar(45), ContactNumber varchar(10), Address varchar(100))")
		########################DONATION TABLE########################################################################
		self.cur.execute("CREATE TABLE IF NOT EXISTS DONATION(Donation_ID int primary key auto_increment, Donor_ID int , BloodBank_ID int, Patient_ID int, BloodType varchar(2), DonationDate date, FOREIGN KEY(Donor_ID) REFERENCES DONOR(Donor_ID), FOREIGN KEY(BloodBank_ID) REFERENCES BLOODBANK(BloodBank_ID), FOREIGN KEY(Patient_ID) REFERENCES PATIENT(Patient_ID))")
		########################BLOODBANK BLOODTYPES##################################################################
		self.cur.execute("CREATE TABLE IF NOT EXISTS BLOODBANK_BLOODTYPE(BloodBank_ID int NOT NULL, BloodBank_BloodType varchar(2), PRIMARY KEY(BloodBank_ID, BloodBank_Bloodtype), FOREIGN KEY(BloodBank_ID) REFERENCES BLOODBANK(BloodBank_ID))")
		########################PATIENT DISEASE#######################################################################
		self.cur.execute("CREATE TABLE IF NOT EXISTS PATIENT_DISEASE(Patient_ID int not null, DiseaseName varchar(45), DateAdmitted Date, HasReceivedBlood binary, PRIMARY KEY(Patient_ID, DiseaseName), FOREIGN KEY(Patient_ID) REFERENCES PATIENT(Patient_ID))")
		#############################################################################################################
		##########-----------------------------end of init-------------------------------------------------##########
		#############################################################################################################
	# GET ALL DONATIONS
	def getDonation(self, flag):
		if flag == 1:
			sql = "SELECT don.donation_id, d.Name, bb.Name, don.BloodType, don.DonationDate FROM DONOR d INNER JOIN DONATION don on don.donor_id = d.donor_id INNER JOIN BLOODBANK bb on don.bloodbank_id = bb.bloodbank_id WHERE don.Patient_ID IS NULL and DATEDIFF(CURDATE(), don.DonationDate) < 40"
		else:
			sql = "SELECT d.Name, don.DonationDate, p.Name, don.BloodType FROM DONOR d INNER JOIN DONATION don on don.donor_id = d.donor_id INNER JOIN PATIENT p on don.Patient_ID = p.Patient_ID WHERE don.Patient_ID IS NOT NULL"
		self.cur.execute(sql)
		result = self.cur.fetchall()
		return result

	# GET ALL DONORS
	def getDonor(self):
		sql = "SELECT Donor_id, Name, Address, concat('+63', ContactNumber), DateOfBirth FROM DONOR"
		self.cur.execute(sql)
		result = self.cur.fetchall()
		return result

	# GET BLOOD BANKS
	def getBloodbank(self):
		sql = "SELECT bb.Bloodbank_id, bb.Name, bb.Address, concat('+63', bb.ContactNumber), GROUP_CONCAT(distinct bt.Bloodbank_BloodType) FROM BLOODBANK bb LEFT JOIN BLOODBANK_BLOODTYPE bt on bt.Bloodbank_ID = bb.Bloodbank_id group by bb.name"
		self.cur.execute(sql)
		result = self.cur.fetchall()
		return result

	# GET PATIENTS
	def getPatient(self):
		sql = "SELECT p.Patient_id, p.Name, p.BloodType, concat('+63', p.ContactNumber), pd.DateAdmitted FROM PATIENT p INNER JOIN PATIENT_DISEASE pd on pd.Patient_ID = p.Patient_ID WHERE pd.DateAdmitted = (SELECT MAX(ppd.DateAdmitted) FROM PATIENT_DISEASE ppd where pd.Patient_ID = ppd.Patient_ID) GROUP BY p.patient_id ORDER BY pd.DateAdmitted"
		self.cur.execute(sql)
		result = self.cur.fetchall()
		return result

	def lookFor(self, keyword, fromList, column, type):
		searchBy = ''
		if fromList == 'Donation':
			if type == 1:
				if keyword == '':
					return self.getDonation(1)
				if column == 'by Donor':
					searchBy = 'd.name'
				elif column == 'by Blood Bank':
					searchBy = 'bb.name'
				elif column == 'by Blood Type':
					searchBy = 'don.BloodType'
				elif column == 'by Donation Date':
					searchBy = 'don.DonationDate'
				sql = "SELECT d.Name, bb.Name, don.BloodType, don.DonationDate FROM DONOR d INNER JOIN DONATION don on don.donor_id = d.donor_id INNER JOIN BLOODBANK bb on don.bloodbank_id = bb.bloodbank_id HAVING {field} LIKE %s".format(field=searchBy)
			else:
				if keyword == '':
					return self.getDonation(0)
				if column == 'by Donor':
					searchBy = 'd.name'
				elif column == 'by Donation Date':
					searchBy = 'don.DonationDate'
				elif column == 'by Recipient':
					searchBy = 'p.Name'
				elif column == 'by Blood Type':
					searchBy = 'don.BloodType'
				sql = "SELECT d.Name, don.DonationDate, p.Name, don.BloodType FROM DONOR d INNER JOIN DONATION don on don.donor_id = d.donor_id INNER JOIN PATIENT p on don.Patient_Id = p.Patient_Id HAVING {field} LIKE %s".format(field=searchBy)


		elif fromList == 'Donor':
			if keyword == '':
				return self.getDonor()
			if column == 'by Name':
				searchBy = 'Name'
			elif column == 'by Address':
				searchBy = 'Address'
			elif column == 'by Contact Number':
				searchBy = 'contact'
			elif column == 'by Birthdate':
				searchBy = 'DateOfBirth'
			sql = "SELECT Name, Address, concat('+63', ContactNumber) as contact, DateOfBirth FROM DONOR HAVING {field} LIKE %s".format(field = searchBy)


		elif fromList == 'Blood Bank':
			if keyword == '':
				return self.getBloodbank()
			if column == 'by Name':
				searchBy = 'bb.name'
			elif column == 'by Address':
				searchBy = 'bb.Address'
			elif column == 'by Contact Number':
				searchBy = 'contact'
			elif column == 'by Blood Type':
				searchBy = 'bloodtypes'
			sql = "SELECT bb.Name, bb.Address, concat('+63', bb.ContactNumber) as contact, GROUP_CONCAT(distinct bt.BloodBank_BloodType) as bloodtypes FROM BLOODBANK bb LEFT JOIN BLOODBANK_BLOODTYPE bt on bt.Bloodbank_ID = bb.Bloodbank_id group by bb.name HAVING {field} LIKE %s".format(field = searchBy)
			
		elif fromList == 'Patient':
			if keyword == '':
				return self.getPatient()
			if column == 'by Name':
				searchBy = 'p.Name'
			elif column == 'by Blood Type':
				searchBy = 'p.BloodType'
			elif column == 'by Contact Number':
				searchBy = 'contact'
			elif column == 'by Admission Date':
				searchBy = 'pd.DateAdmitted'
			sql = "SELECT p.Name, p.BloodType, concat('+63', p.ContactNumber) as contact, pd.DateAdmitted FROM PATIENT p INNER JOIN PATIENT_DISEASE pd on pd.Patient_ID = p.Patient_ID WHERE pd.DateAdmitted = (SELECT MAX(ppd.DateAdmitted) FROM PATIENT_DISEASE ppd where pd.Patient_ID = ppd.Patient_ID) HAVING {field} LIKE %s".format(field = searchBy)

		val = '%' + keyword + '%',
		self.cur.execute(sql, val)
		res = self.cur.fetchall()
		return res

	def getOnePatient(self, id):
		sql = "SELECT pd.DiseaseName, pd.DateAdmitted, CASE pd.hasReceivedBlood WHEN 0 THEN 'No' WHEN 1 THEN 'Yes' END, CASE pd.hasReceivedBlood WHEN 0 THEN null WHEN 1 THEN d.Name END FROM PATIENT_DISEASE pd LEFT JOIN DONATION don ON pd.Patient_ID = don.Patient_ID LEFT JOIN DONOR d ON don.Donor_ID = d.Donor_ID WHERE pd.Patient_ID = %s GROUP BY pd.DiseaseName ORDER BY pd.DateAdmitted"
		val = id,
		self.cur.execute(sql, val)
		res = self.cur.fetchall()
		return res

		# ADD NEW DONOR
	def addDonor(self, name, address, contactNumber, birth):
		sql = "INSERT INTO DONOR (name, Address, ContactNumber, dateofbirth) VALUES (%s, %s, %s, %s)"
		val = (name, address, contactNumber, birth)
		self.cur.execute(sql, val)
		self.conn.commit()

	# ADD NEW PATIENT
	def addPatient(self, Name, bloodtype, contactNumber):
		sql = "INSERT INTO PATIENT (Name, BloodType, ContactNumber) VALUES (%s, %s, %s)"
		val = (Name , bloodtype, contactNumber)
		self.cur.execute(sql, val)
		self.conn.commit()
		
	#ADD PATIENT'S DISEASE
	def addPatientDisease(self, disease, id=None):
		if id is None:
			sql = "INSERT INTO PATIENT_DISEASE SELECT MAX(p.Patient_ID), %s, CURDATE(), 0 FROM Patient p"
			val = (disease,)
		else:
			sql = "INSERT INTO PATIENT_DISEASE VALUES (%s, %s, CURDATE(), 0)"
			val = (id, disease)
		self.cur.execute(sql, val)
		self.conn.commit()

	# ADD NEW BLOODBANK
	def addBloodBank(self, name, contactNumber, address):
		sql = "INSERT INTO BLOODBANK (Name, ContactNumber, Address) VALUES (%s, %s, %s)"
		val = (name, contactNumber, address)
		self.cur.execute(sql, val)
		self.conn.commit()

	# ADD NEW DONATION WITH RECIPIENT
	def addDonationWithRecipient(self, d_id, bb_id, p_id, blood):
		sql = "INSERT INTO DONATION VALUES (null, %s, %s, %s, %s, CURDATE())"
		val = (d_id, bb_id, p_id, blood)
		self.cur.execute(sql, val)
		sql = "INSERT IGNORE INTO BLOODBANK_BLOODTYPE VALUES (%s, %s)"
		val = (bb_id, blood)
		self.cur.execute(sql, val)
		sql = "UPDATE PATIENT_DISEASE set hasReceivedBlood = 1 WHERE Patient_id = %s and hasreceivedblood = 0 limit 1"
		val = p_id,
		self.cur.execute(sql,val)
		self.conn.commit()

	#ADD NEW DONATION WITHOUT RECIPIENT
	def addDonationNoRecipient(self, d_id, bb_id, blood):
		sql = "INSERT INTO DONATION VALUES (null, %s, %s, null, %s, CURDATE())"
		val = (d_id, bb_id, blood)
		self.cur.execute(sql, val)
		self.conn.commit()
	
	#UPDATE DONATION WITHOUT RECIPIENT TO WITH RECIPIENT
	def updateDonation(self, p_id, don_id, diagnosis):
		sql = " UPDATE DONATION SET patient_id = %s, donationdate = CURDATE() where donation_id = %s"
		val = (p_id, don_id)
		self.cur.execute(sql, val)
		sql = "UPDATE PATIENT_DISEASE set hasReceivedBlood = 1 where patient_id = %s and diseasename = %s"
		val = (p_id, diagnosis)
		self.cur.execute(sql,val)
		self.conn.commit()
