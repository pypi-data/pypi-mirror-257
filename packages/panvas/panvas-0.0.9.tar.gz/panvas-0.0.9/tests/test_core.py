#!/usr/bin/env python3
import os,sys,json,unittest

proj_path = os.path.dirname(os.path.abspath(__file__)).replace('/tests','')

class SimplisticTest(unittest.TestCase):
    def setUp(self):
        self.__key = None
        self.__course = None
        self.__assignment = None
        if os.path.exists("props.json"):
            with open("props.json") as f:
                props = json.load(f)
                self.__key = props["key"]
                self.__course = props["course"]
                self.__assignment = props["assignment"]
        #import os,sys;sys.path.insert(1,"./");from panvas import course;canvas_runner = course(__key, __course, __assignment)

        sys.path.insert(0, proj_path);from panvas import course
        self.canvas_runner = course(self.__key)

    def tearDown(self):
        del self.canvas_runner

    def test_view_assignment(self):
        self.assertIsNotNone(self.canvas_runner)
        self.canvas_runner.set_course_assignment(self.__course, self.__assignment)
        self.assertIsNotNone(self.canvas_runner.course)
        self.assertIsNotNone(self.canvas_runner.assignment)

if __name__ == '__main__':
    unittest.main()