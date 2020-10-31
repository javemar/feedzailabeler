
"""
Allows you to change status in CM
You must use a csv file to upload all the cases
Please see the documentation
get geckodriver in  https://github.com/mozilla/geckodriver/releases/tag/v0.27.0
"""

__author__ = "Javier Martinez"
__version__ = "0.0.1"
__email__ = "javemartinezc@gmail"


import pandas as pd 
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import sys
import datetime
import time
import logging
import Tkinter as tk
import tkFileDialog


FILE_INPUT = None
PATH = os.path.dirname(os.path.abspath(__file__))
#PATH_DRIVER = r"E:\Program Files (x86)\Mozilla Firefox\firefox.exe"
platform = sys.platform
PATH_GECKODRIVER = os.path.join(PATH , 
                    "geckodriver_" + ("windows" if platform.find("win")>=0 
                    else ("linux" if platform.find("linux")>=0 else 'mac'   ) ) )
print PATH_GECKODRIVER
os.environ["PATH"] +=   ("\\" if platform.find("win")>=0  else ":" )     + PATH_GECKODRIVER

print os.environ["PATH"]

TODAY = str(datetime.datetime.today())[0:10]
logging.basicConfig(format='%(asctime)s %(message)s', filename = os.path.join(PATH, "feedzai_labeler_log_{}.txt".format(TODAY)   ), level=logging.INFO)

def find_object_label(type_label, driver):
	toplevel = driver.find_element_by_class_name("fdz-js-details-template-actions.fdz-css-details-template__toplevel-actions")
	#driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()
	"""
	waiting_3_party =  toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--info.fdz-js-button.fdz-css-button")
	reject =  toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--warning.fdz-js-button.fdz-css-button")
	fraud =  toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--danger.fdz-js-button.fdz-css-button")
	nofraud =  toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--success.fdz-js-button.fdz-css-button")
	"""
	if type_label == "waiting_3_party":
		return toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--info.fdz-js-button.fdz-css-button")
	elif type_label == "reject":
		return toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--warning.fdz-js-button.fdz-css-button")
	elif type_label == "fraud":
		return toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--danger.fdz-js-button.fdz-css-button")
	elif type_label == "nofraud":
		return toplevel.find_element_by_class_name("fdz-js-table-visible-button.fdz-css-table__action-button.fdz-css-button--success.fdz-js-button.fdz-css-button")
	else:
		return None

options_reason = {"fraud":["Suspicion", 
					"CHB", "Reported"], 
					"nofraud":["False", "Not"], 
					"waiting_3_party":[""],
							"reject":[""]}
		
#warming up

def test2():
	path_driver = r"E:\Program Files (x86)\Mozilla Firefox\firefox.exe"
	driver = webdriver.Firefox( firefox_binary=path_driver)

	pagina_web = "https://payu.okta-emea.com/app/UserHome"
	driver.get(pagina_web)

	### wait for loging

	## go to search page
	pagina_web_search = "https://payu-cm.feedzai.com/search"
	driver.get(pagina_web_search)
	#search_button = driver.find_element_by_class_name("fdz-css-search-form-button.fdz-css-button--blue.fdz-js-search-button.fdz-css-search__button.fdz-js-button.fdz-css-button")
	#time.sleep(4)
	search_button = wait("fdz-css-search-form-button.fdz-css-button--blue.fdz-js-search-button.fdz-css-search__button.fdz-js-button.fdz-css-button"
							,By.CLASS_NAME, driver, 60)
	
	



##process

def change_status(date,external_id, type_label,reason, notes,driver,
			     logging= logging,		options_reason = options_reason , time_sleeps= (2, 2,0.5)):
	string_log = external_id + ":"
	
	try:
		assert reason in options_reason[type_label], "reason no belong to type_label"
	except:
		string_log += "reason no belong to type_label"
		logging.info(string_log)
		#goback.click()
		return None
	
	try:
		#searching the external_id
		initial_time = pd.to_datetime(date) - datetime.timedelta(days=1)
		end_time = pd.to_datetime(date) + datetime.timedelta(days=1)



		# external_box = driver.find_element_by_id("0")
		external_box = wait("0"
							,By.ID, driver, 30)
		external_box.clear()
		external_box.send_keys(external_id)
		search_button = driver.find_element_by_class_name("fdz-css-search-form-button.fdz-css-button--blue.fdz-js-search-button.fdz-css-search__button.fdz-js-button.fdz-css-button")
		dates_button = driver.find_elements_by_class_name("rdt.fdz-js-kitte-datepicker.fdz-css-kitte-datepicker")
		for index,date in enumerate([initial_time, end_time]):
			subdate = dates_button[index].find_element_by_class_name("fdz-js-input.fdz-css-input")
			subdate.clear()
			subdate.click()
			subdate.send_keys(str(date)[0:10])

		search_button.click()
		#time.sleep(time_sleeps[0])

		# tx = driver.find_element_by_class_name("fdz-js-column.fdz-css-table__column.fdz-css-color--black")
		tx = wait("fdz-js-column.fdz-css-table__column.fdz-css-color--black"
							,By.CLASS_NAME, driver, 3)
							
							
		## get value tx
		tx_value = driver.find_elements_by_class_name("fdz-js-column.fdz-css-table__column.fdz-css-color--black")[2].text
		tx.click()

		
		
	except Exception as error:
		string_log += "tx wasn't found," + str(error).replace("\n" ,"")
		logging.info(string_log)
		#goback.click()
		return None
	try:
		##modifying transaction
		#goback = driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button")
		#close_box = wait("fdz-js-modalbox-header fdz-css-modalbox__header"
		#					,By.CLASS_NAME, driver, 10, EC.invisibility_of_element)
		goback = wait("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button"
							,By.CLASS_NAME, driver, 10, EC.element_to_be_clickable)
		
		test_tx_value = WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element(
										(By.CSS_SELECTOR,".fdz-css-color--black > div:nth-child(2) > span:nth-child(1)"), tx_value))
		
		#time.sleep(0.)
		#print type(goback)
		# current_status = driver.find_elements_by_class_name("fdz-js-box-value-container.fdz-css-box__value-container")[2].text
		current_status = wait("fdz-js-box-value-container.fdz-css-box__value-container"
								,By.CLASS_NAME, driver, 10, EC.presence_of_all_elements_located)[2].text
		#print type(goback)
		
		object_label = find_object_label(type_label, driver)
		driver.execute_script("window.scrollTo(0, 10)") 
		object_label.click()
		# dropdown = driver.find_element_by_css_selector(".fdz-js-state-select > div:nth-child(1)")
		dropdown = wait(".fdz-js-state-select > div:nth-child(1)"
							,By.CSS_SELECTOR, driver, 1)
		dropdown.click()
		
		
		
	except Exception as error:
		#print str(error)
		string_log += "It's not possible to change from {} to {}".format(current_status ,type_label )
		logging.info(string_log)
		
		goback.click()
		#time.sleep(time_sleeps[2])
		return None
	try:

		actions  = ActionChains(driver)
		actions.move_to_element(dropdown).send_keys(reason+Keys.TAB).perform()
		note = driver.find_element_by_id("setStateTextarea")
		note.send_keys(notes)
		
		##send data
		button = driver.find_element_by_class_name("fdz-js-set-state-submit.fdz-css-modal-button.fdz-css-button--primary.fdz-js-button.fdz-css-button")
		button.click()
		#time.sleep(time_sleeps[2])
		string_log += "change from {} to {}".format(current_status,type_label )

		close_box = wait("fdz-js-modalbox-header fdz-css-modalbox__header"
							,By.CLASS_NAME, driver, 30, EC.invisibility_of_element)
		
		close_box = True
		
		while close_box:
			try:
				goback = wait("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button"
									,By.CLASS_NAME, driver, 10, EC.element_to_be_clickable)
				time.sleep(1)
				goback.click()
				logging.info(string_log)
				close_box = False
			except:
				pass
		#time.sleep(time_sleeps[2])
		return None
	
	except Exception as error:
		string_log += str(error).replace("\n", "")
		logging.info(string_log)
		goback.click()
		#time.sleep(time_sleeps[2])
		return None
	
	##go to search page
	
	
# actions.move_to_element(dropdown).send_keys(Keys.TAB).perform()

def test():
	#test1
	external_id  = "LATAM-PSP_519601883"
	date = "2020-08-30"
	type_label = "fraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "CHB"  #
	notes = "reporte fraude ticket"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()
	#test2
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "fraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "Suspicion"  #
	notes = "reporte fraude ticket"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()
	#test3
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "fraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "Reported"  #
	notes = "reporte fraude ticket"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()

	#test4
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "fraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "other"  #
	notes = "reporte fraude ticket"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()

	#test5
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "nofraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "False"  #
	notes = "no fraud"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()


	#test6
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "nofraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "Not"  #
	notes = "no fraud"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()

	#test7
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "nofraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "other"  #
	notes = "no fraud"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()


	#test8
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "reject"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = ""  #
	notes = "reject"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()

	#test9
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "reject"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "other"  #
	notes = "no fraud"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()



	#test10
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "waiting_3_party"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = ""  #
	notes = "no fraud"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()

	#test11
	external_id  = "LATAM-PSP_521242814"
	date = "2020-09-01"
	type_label = "waiting_3_party"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
	reason = "other"  #
	notes = "no fraud"
	change_status(date,external_id, type_label,reason, notes , driver)
	driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()

def wait(tag, by, driver, seconds, condition = EC.presence_of_element_located):	
	wt = WebDriverWait(driver, seconds)
	elmt = wt.until(condition((by, tag)))
	#print(elmt)
	return elmt
	
	
def update_labels(file_input,driver, logging=logging):

	columns_test = ["orden_id",	"date_creation","type_label","reason","notes"]
	datos = pd.read_csv(file_input, sep=";") 
	
	test = filter(lambda x: not x,   map( lambda x: x in datos.columns, columns_test ) )
	
	assert len(test) == 0, 'You need to include all of the following columns: {}'.format(columns_test)
	
	(datos["orden_id"]+ 1).head()
	(pd.to_datetime(datos["date_creation"])).head()
		
	logging.info("Start process with {} rows".format(datos.shape[0]) )
	datos["external_id"] = "LATAM-PSP_" + datos["orden_id"].astype(str).str.replace("\..+", "")
	pagina_web_search = "https://payu-cm.feedzai.com/search"
	
	
	driver.get(pagina_web_search)
	#time.sleep(4)
	
	for index in datos.index:
		print index
		change_status(datos.loc[index,"date_creation"],datos.loc[index,"external_id"], 
								datos.loc[index,"type_label"],datos.loc[index,"reason"], 
								datos.loc[index,"notes"],driver)
        if (index % 100.0) == 100:
            print "sleeping 10 senconds..."    
        time.sleep(10)
"""	
external_id  = "LATAM-PSP_519625363"
date = "2020/08/30  06:36:05"
type_label = "fraud"  ## one of ["waiting_3_party", "reject", "fraud", "nofraud"]
reason = "CHB"  #
notes = "reporte fraude ticket"
change_status(date,external_id, type_label,reason, notes , driver)

"""

#file_input = r"d:\javier.martinez\Documents\feedzai_labeler\format_feedzai_labeler.csv"


##go to search page
#driver.find_element_by_class_name("fdz-js-header-back-button.fdz-css-button--link.fdz-js-button.fdz-css-button").click()


class FeedzaiLabeler(tk.Tk, object):
	def __init__(self,*args,**kwargs ):
		super(FeedzaiLabeler, self).__init__(*args, **kwargs)
		#self.main_window = tk.Tk()
		self.driver = None 
		self.title("FeedzaiLabeler         Javier Martinez -- javemartinezc@gmail.com")
		self.session = tk.StringVar()
		self.session.set("Inactive Session")
		self.fileName = ""
		self.geometry("600x300")
		self.main_frame = tk.Frame(self)
		#self.main_frame.pack(side="top", fill="both", expand = True)
		self.main_frame.pack()
		
		self.frame_buttons = tk.Frame(self.main_frame)
		self.frame_buttons.grid(column  = 1, row=1, padx=30, pady=10)
		
		self.frame_strings = tk.Frame(self.main_frame)
		self.frame_strings.grid(column  = 2, row=1, padx=10, pady=10)
		
		self.frame_action = tk.Frame(self.main_frame)
		self.frame_action.grid(column  = 1, row=2,  pady=10, columnspan=2)
		
		
		self.button_charge_session = tk.Button(self.frame_buttons, text="Load Firefox", 
													command= lambda: self.create_conection(self.label_charge_session), width=20)
		self.button_charge_session.grid(column  = 1, row=1, padx=10, pady=10) # sticky="nsew"
		
		self.label_charge_session = tk.Label(self.frame_strings, textvariable=self.session)
		self.label_charge_session.grid(column  = 1, row=1, padx=10, pady=10)
		#self.button_charge_session.grid()
		


		self.label_file = tk.Label(self.frame_strings, text=self.fileName)
		self.label_file.grid(row= 2, column=1, padx=10, pady=10)	
		
		self.button_file = tk.Button(self.frame_buttons, text="Select File", command = lambda: self.archivo(self.label_file), width = 20)
		self.button_file.grid(row= 2, column=1, padx=10, pady=10)		
	
		##
		self.button_action = tk.Button(self.frame_action, text="Update Status", command = lambda: self.update_status(), width = 20)
		self.button_action.grid(row= 1, column=0, padx=40,  pady=10)	
	
	def archivo(self, label):
		self.fileName = tkFileDialog.askopenfilename(initialdir = PATH , title= "Seleccione archivo xls", 
													filetypes = (('csv', '*.csv'),
															     ))

	
		label["text"] = self.fileName.split(r"/")[-1]		
	
	def update_status(self):
		try:
			self.driver.title
			update_labels(self.fileName,self.driver, logging=logging)
		except Exception as error:
			print str(error)
			#self.session.set("Inactive Session")

	def create_conection(self, label):
		try:
			print type(self.driver.title)
			#label["text"] = "Session Active: {}".format(self.driver.title.encode("latin", errors="ignore"))
			self.session.set("Active Session: {}".format(self.driver.title.encode("latin", errors="ignore")))
		except Exception as error:
			print str(error)
			#path_driver = PATH_DRIVER
			#self.driver = webdriver.Firefox( firefox_binary=path_driver)
			self.driver = webdriver.Firefox()
			
			pagina_web = "https://payu.okta-emea.com/app/UserHome"
			self.driver.get(pagina_web)
			time.sleep(2)
			#label["text"] = "Session Active: {}".format(self.driver.title.encode("latin", errors="ignore"))
			self.session.set( "Active Session: {}".format(self.driver.title.encode("latin", errors="ignore")))
			#print self.session.get()
			
if __name__ == "__main__":
	app = FeedzaiLabeler()
	app.mainloop()