from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import community_partner_views
from . import project_views
from . import enrollment_views
from . import course_views
from . import department_views
from . import college_views
from . import user_views
from . import semester_views
from . import record_views

urlpatterns = [
    url(r'^me/$', user_views.MyUser.as_view()),
    url(r'^users/$', user_views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', user_views.UserDetail.as_view()),
    url(r'^courses/$', course_views.CourseList.as_view()),
    url(r'^course/$', course_views.CourseDetail.as_view()),
    url(r'^course/(?P<pk>[A-Z0-9]+)/$', course_views.CourseDetail.as_view()),
    url(r'^course/(?P<course>[A-Z0-9]+)/projects/$', course_views.CourseProjectList.as_view()),
    url(r'^course/(?P<course>[A-Z0-9]+)/sections/$', course_views.CourseSectionsList.as_view()),
    url(r'^course/(?P<course>[A-Z0-9]+)/instructors/$', course_views.CourseInstructorList.as_view()),
    url(r'^course/(?P<course>[A-Z0-9]+)/students/$', course_views.CourseStudentList.as_view()),
    url(r'^course/(?P<pk>[A-Z0-9]+)/projects/$', course_views.CourseProjectList.as_view()),
    url(r'^department/$', department_views.DepartmentDetail.as_view()),
    url(r'^departments/$', department_views.DepartmentList.as_view()),
    url(r'^department/(?P<pk>[a-zA-Z0-9]+)/$', department_views.DepartmentDetail.as_view()),
    url(r'^college/$', college_views.CollegeDetail.as_view()),
    url(r'^colleges/$', college_views.CollegeList.as_view()),
    url(r'^college/(?P<pk>[a-zA-Z0-9][\w|\W]+)/$', college_views.CollegeDetail.as_view()),
    url(r'^enrollments/$', enrollment_views.EnrollmentList.as_view()),
    url(r'^enrollments/(?P<course>[A-Z0-9]+)/$', enrollment_views.EnrollmentCourseList.as_view()),
    url(r'^enrollments/crn/(?P<crn>[0-9]+)/$', enrollment_views.EnrollmentCRNList.as_view()),
    url(r'^enroll/(?P<pk>[0-9]+)/$', enrollment_views.EnrollmentDetail.as_view()),
    url(r'^enroll/$', enrollment_views.EnrollmentDetail.as_view()),
    url(r'semester/$', semester_views.SemesterDetail.as_view()),
    url(r'semester/startnext/$', semester_views.StartSemester.as_view()),
    url(r'semester/(?P<pk>[\w{}.-]{1,40})/$', semester_views.SemesterDetail.as_view()),
    url(r'communityPartner/$', community_partner_views.CommunityPartnerDetail.as_view()),
    url(r'communityPartner/(?P<pk>[0-9]+)/$', community_partner_views.CommunityPartnerDetail.as_view()),
    url(r'communityPartner/(?P<pk>[0-9]+)/projects/$', community_partner_views.CommunityPartnerProjects.as_view()),
    url(r'communityPartner/(?P<pk>[0-9]+)/projects/active/$',
        community_partner_views.CommunityPartnerProjectsActive.as_view()),
    url(r'projects/$', project_views.ProjectsAll.as_view()),
    url(r'project/$', project_views.ProjectDetail.as_view()),
    url(r'project/(?P<pk>[0-9]+)/$', project_views.ProjectDetail.as_view()),
    url(r'project/(?P<pk>[0-9]+)/students/$', project_views.ProjectStudents.as_view()),
    url(r'record/$', record_views.RecordDetail.as_view()),
    url(r'record/(?P<pk>[0-9]+)/$', record_views.RecordDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
