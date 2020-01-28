# -------------------------------------------------------------------------------
# DbHandler
# -------------------------------------------------------------------------------
# A class to interact with the database
#-------------------------------------------------------------------------
# Author:       Tomer Lev (Credit where credit's due)
#-------------------------------------------------------------------------


# import logging so we can write messages to the log
import logging
# import operating system library
import os
#import DB library
import MySQLdb

# Database connection parameters 
DB_USER_NAME='db_team24'
DB_PASSWORD='deyoncdt'
DB_DEFALUT_DB='db_team24'

# ---------------------------------------------------------
# Handles connections to DB
# --------------------------------------------------------
class DbHandler():
	def __init__(self):
		logging.info('Initializing DbHandler new')
		self.m_user=DB_USER_NAME
		self.m_password=DB_PASSWORD
		self.m_default_db=DB_DEFALUT_DB
		self.m_unixSocket='/cloudsql/dbcourse2015:mysql'
		self.m_charset='utf8'
		self.m_host='173.194.110.126'
		self.m_port=3306
		self.m_DbConnection=None

# ---------------------------------------------------------
# Connecting to DB
# --------------------------------------------------------
	def connectToDb(self):
		logging.info('In ConnectToDb')
		# we will connect to the DB only once
		if self.m_DbConnection is None:
			env = os.getenv('SERVER_SOFTWARE')
			if (env and env.startswith('Google App Engine/')):
				#Running from Google App Engine
				logging.info('In env - Google App Engine')
				# connect to the DB
				self.m_DbConnection = MySQLdb.connect(
				unix_socket=self.m_unixSocket,
				user=self.m_user,
				passwd=self.m_password,
				charset=self.m_charset,
				db=self.m_default_db)
			else:
				#Connecting from an external network.
				logging.info('In env - Launcher')
				# connect to the DB
				self.m_DbConnection = MySQLdb.connect(
				host=self.m_host,
				db=self.m_default_db,
				port=self.m_port,
				user= self.m_user,
				passwd=self.m_password,
				charset=self.m_charset)
    
# ---------------------------------------------------------
# Disconnecting from DB
# --------------------------------------------------------
	def disconnectFromDb(self):
		logging.info('In DisconnectFromDb')
		if self.m_DbConnection:
			self.m_DbConnection.close()

# ---------------------------------------------------------
# performing a commit action on db
# --------------------------------------------------------		
	def commit(self):
		logging.info('In commit')
		if self.m_DbConnection:
			self.m_DbConnection.commit()			

# ---------------------------------------------------------
# returning a cursor object to perform db actions
# --------------------------------------------------------			
	def getCursor(self):
		logging.info('In DbHandler.getCursor')
		self.connectToDb()
		return (self.m_DbConnection.cursor())