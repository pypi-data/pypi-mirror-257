import os,sys,types,importlib.machinery,shutil,mystring
if sys.version_info[0] < 3: 
	from StringIO import StringIO
else:
	from io import StringIO
from canvasapi import Canvas
from canvasapi.requester import Requester
from canvasapi.upload import Uploader
from canvasapi.util import combine_kwargs
from tqdm import tqdm

def flatten(column_header):
	if isinstance(column_header, list) or isinstance(column_header, tuple):
		return ' '.join([str(ch) for ch in column_header]).strip()
	return column_header

class course(object):
	def __init__(self, apikey, course_number=None, assignment_number=None, canvas_url="https://canvas.vt.edu"):
		self.apikey = apikey
		self.__course_number = course_number
		self.__assignment_number = assignment_number
		self.canvas_url = canvas_url

		self.canvas = Canvas(canvas_url, self.apikey)
		self.__course = None
		self.__assignment = None

	def set_course_assignment(self, course_number=None, assignment_number=None, force_set=False):
		self.set_course(course_number, force_set)
		self.set_assignment(assignment_number, force_set)

	def set_course(self, course_number=None, force_set=False):
		if course_number:
			if self.__course_number is None or force_set:
				self.__course_number = course_number

	@property
	def course(self):
		if self.__course is None:
			if self.__course_number is None:
				print("Please set the course number")
			else:
				self.__course = self.canvas.get_course(int(self.__course_number))
		return self.__course

	def set_assignment(self, assignment_number=None, force_set=False):
		if assignment_number:
			if self.__assignment_number is None or force_set:
				self.__assignment_number = assignment_number

	@property
	def assignment(self):
		if self.__assignment is None:
			if self.__assignment_number is None:
				print("Please set the assignment number")
			else:
				self.__assignment = self.course.get_assignment(int(self.__assignment_number))
		return self.__assignment

	def user_name(self,user_id):
		return self.course.get_user(user_id).name

	def user_id(self,user_id):
		return self.course.get_user(user_id).name

	def course_students(self, search_term:str=None, course_number=None):
		self.set_course(course_number)
		if search_term:
			return self.course.get_users(enrollment_type=['student'],search_term=search_term)
		return self.course.get_users(enrollment_type=['student'])

	def user_id_from_name(self, users_pid:str, course_number=None):
		self.set_course(course_number)
		return self.course_students(search_term=users_pid)

	def add_comment(self, submission, comment):
		return  submission.edit(comment={"text_comment":comment})

	def get_user_submission_comments(self, course_id, assignment_id, user_id, requestor):
		"""
		https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.create_file
		https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
		https://community.canvaslms.com/t5/Canvas-Question-Forum/Is-there-an-API-for-grade-comments/td-p/107787
		https://github.com/ucfopen/canvasapi/blob/02d42cba3b0fd22e780ac0a5e904ea84fbc0b58d/canvasapi/submission.py#L158
		"""
		####A GENERAL GET COMMENTS IS NOT SUPPORTED VIA CANVAS API
		from canvasapi.upload import Uploader
		kwargs = {}
		response = requestor.request(
			"GET",
			"courses/{}/assignments/{}/submissions/{}/comments/".format(
			course_id, assignment_id, user_id
			),
			**kwargs,
		)
		return response

	def delete_specific_comment(self, course_id, assignment_id, user_id, comment_id, requestor):
		"""
		https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.create_file
		https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
		https://community.canvaslms.com/t5/Canvas-Question-Forum/Is-there-an-API-for-grade-comments/td-p/107787
		https://github.com/ucfopen/canvasapi/blob/02d42cba3b0fd22e780ac0a5e904ea84fbc0b58d/canvasapi/submission.py#L158
		"""
		from canvasapi.upload import Uploader
		kwargs = {}
		response = requestor.request(
			"DELETE",
			"courses/{}/assignments/{}/submissions/{}/comments/{}".format(
			course_id, assignment_id, user_id, comment_id
			),
			**kwargs,
		)
		return response

	def assign_grades(self, frame:mystring.frame, student_pid_column:str, student_id_column:str=None, proceed=True,debug=False, course_number=None, assignment_number=None, ignore_comment_lambda=lambda x:x):
		self.set_course(course_number)
		self.set_assignment(assignment_number)

		differences = []

		comment_colum = None
		for kol in frame.kolz:
			if "Comments ({0})".format(str(self.__assignment_number)) in str(kol):
				comment_colum = kol
				break
		
		grade_colum = None
		for kol in frame.kolz:
			if "({0})".format(str(self.__assignment_number)) in str(kol) and "Comments" not in str(kol):
				grade_colum = kol
				break

		if not student_id_column:
			student_list = {}
			for student in self.course_students():
				student_list[student.login_id] = student.id

		for row in tqdm(frame.roll):
			student_id = None
			if student_id_column:
				student_id = row[student_id_column]
			else:
				student_id = student_list[row[student_pid_column]]

			if student_id and str(student_id).strip() != '':
				info = {
					"StudentID":student_id,
					"Exception": None,
				}

				try:
					student_latest_submission = self.assignment.get_submission(student_id)

					info["OldGrade"]=student_latest_submission.grade
					info["NewGrade"]=row[grade_colum]

					nu_comment = ignore_comment_lambda(row[comment_colum])
					if nu_comment and mystring.string(nu_comment).notempty and nu_comment != row[comment_colum]:
						info["OldComment"] = row[comment_colum]
						info["NewComment"] = nu_comment

					if debug:
						print(info)
					
					if proceed:
						if debug:
							print("Proceeding")

						grade_edit_response = student_latest_submission.edit(
							grade=info["NewGrade"]
						)
						if debug:
							print("Post Grade Update: {0}".format(grade_edit_response))

						if nu_comment:
							comment_edit_response=student_latest_submission.edit(
								comment={
									"text_comment":nu_comment
								}
							)
							if debug:
								print("Post comment Update: {0}".format(comment_edit_response))

					info["Change"] = info["OldGrade"] != info["NewGrade"]

				except Exception as e:
					info["Exception"] = e
					print("Issue with student [{0}] := {1}".format(row[frame.kolz[0]], str(e)))

				differences += [info]

		return mystring.frame.from_arr(differences)

"""
	def assign_grades_old(self, info:mystring.frame, student_pid_column:str, debug=False, course_number=None, assignment_number=None):
		self.set_course(course_number)
		self.set_assignment(assignment_number)

		student_pid_column = student_pid_column

		for sub in self.assignment.get_submissions():
			if debug:
				print(sub.body)
				print(sub.grade)

			comment = None
			comment_row = -1
			student_name = None
			student_id = str(sub.user_id).strip()

			for row_itr, row in enumerate(info.roll):
				if row_itr == 0 and comment_row == -1:
					comment_row = col_num(assignment_num+":", row.values)
				elif row_itr > 1 and comment_row != -1:
					student_name = str(row.values[0])
					user_id = str(row.values[1]).strip()

					if debug:
						print({
							"A": student_id,
							"B": user_id,
							"A==B": student_id == user_id
						})

					if user_id is not None and user_id == student_id:
						comment = row.values[comment_row]
						if debug:
							print(f"{student_name} ==== {comment}")
						break

			if debug:
				print(";",flush=True)

			if comment is not None:
				print(f"{student_name} := [{sub.grade}]({comment})", flush=True)

				if proceed:
					sub.edit(
						comment={
							"text_comment":comment
						}
					)
			else:
				print(f"!!!!! {student_name}|{student_id}| := [{sub.grade}]({comment})", flush=True)
"""