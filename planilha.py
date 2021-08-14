#link for the spreadsheet: https://docs.google.com/spreadsheets/d/1-zbC2Uh2BE5MgtCc9cG2qEVJ1PWjx2ZJA-A7VCDu_xA/edit#gid=0

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#conection with the server via API
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)#use the credentials in the json file to acess it
wks = gc.open_by_key('1-zbC2Uh2BE5MgtCc9cG2qEVJ1PWjx2ZJA-A7VCDu_xA')#Open the spreadsheet with this key
worksheet = wks.get_worksheet(0)#get the first pagee


#functions used
def search_student(reg_number):
	lista = worksheet.findall(reg_number)#search for the number on the spreadsheet
	elemento=0
	for i in lista:
		if i.col ==1:
			elemento=i#grab only the number on the column 1( the regstration n)
	return elemento

def write_spreadsheet(situation,final_note):
	"""
	This function write the student average score and situation in the spreadsheet
	"""
	worksheet.update_cell(result.row,result.col+6,situation)
	worksheet.update_cell(result.row,result.col+7,final_note)

###############################################################################################################################

## program execution:
execution = True
while execution ==True:
	student = input(" Type the student's registration number \n ->  ")
	result = search_student(student)

	if result ==0:
		print(' student not found \n')
	else:
		maximum_absences = 15
		student_data = worksheet.row_values(result.row)#catch all the elements of that line in a list:
		number_absent_days = student_data[2]
		scores = [int(i) for i in student_data[3:6]]#all student's results in the tests
		avg_score = round(sum(scores)/3,2)

		#output for the user
		print('\n ________________________________________________________________________________________________________________\n')
		print(' reg number: {}  |  name: {}  |  absenses: {}  |  P1: {}  P2: {}  P3: {}  |  average: {} '.format(student_data[0],student_data[1],student_data[2],student_data[3],student_data[4],student_data[5],avg_score))
		
		#verifying student situation

		if int(number_absent_days) > maximum_absences:
			situation =' reprovado por falta '
			naf = 0
		else:	
			if avg_score <50:
				situation = 'Reprovado por Nota'
				naf = 0
			elif avg_score >= 50 and avg_score <70:
				situation = 'Exame Final'
				naf = 100 - avg_score
			else: 
				situation = 'Aprovado'
				naf = 0
		print('\n status: {}  | final test score: {}'.format(situation, naf))
		print('\n ________________________________________________________________________________________________________________')
		write_on_spreadsheet = input('Do you want to update the spreadsheet with the situation,average and final test score? [y,n] \n -> ')
		if write_on_spreadsheet=="y":
			write_spreadsheet(situation,naf)
			print('\n ________________________________________________________________________________________________________________')
			print('\n spreadsheet updated')
		else: 
			print('\n spreadsheet not updated')
			print('\n ________________________________________________________________________________________________________________')
			
	procede = input(' Continue with the query? [y/n]\n ->')
	if procede == 'n': execution = False